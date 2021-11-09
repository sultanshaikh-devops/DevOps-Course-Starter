import os
from todo_app.models.view import ViewModel
from todo_app.models.card import Card
from todo_app.models.user import User

from flask import Flask, render_template, request, redirect, url_for, session
from todo_app.adapters.mongodb_todo import *
from todo_app.adapters.mongodb_user import *

#Login
from flask_dance.contrib.github import make_github_blueprint, github
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer import oauth_authorized

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


class UserToLogin (UserMixin):
    def __init__(self, id):
        self.id = id

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    #os.environ['OAUTHLIB_INSECURE_TRANSPORT']
    gh_blueprint = make_github_blueprint(client_id=os.environ['GITHUB_CLIENT_ID'], client_secret=os.environ['GITHUB_CLIENT_SECRET'])
    app.register_blueprint(gh_blueprint, url_prefix='/github_login')

    todo = mongodb_todo()
    usermanager = mongodb_user()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):        
        return UserToLogin(user_id)
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(url_for('github_login'))
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.clear()
        
        github.blueprint.teardown_session
        #return redirect(url_for('github.login'))
        return render_template("close.html")
    
    @app.route('/', methods=['GET'])
    def github_login():
        if not github.authorized:
            return redirect(url_for('github.login')) 
        account_info = github.get('/user')   
        if account_info.ok:
            account_info_json = account_info.json()
            currentUserName = str(account_info_json['login'])                
            login_user(UserToLogin(currentUserName))
            
            if usermanager.get_totalusercount() == 0:
                usermanager.create_user(username=currentUserName,role="admin")
            
            if (usermanager.get_totalusercount() > 0) and (usermanager.get_findusercount(qry={"username": currentUserName}) == 0):
                usermanager.create_user(username=currentUserName,role="read")

        return redirect(url_for('get_index'))


    ##### Core TODO_Tasks#####
    #error handling for 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error='resource not found!')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/home', methods=['GET'])
    @login_required
    def get_index():
        cardslist = []
        items = todo.get_AllItems()
        if (app.config['LOGIN_DISABLED']):
            userRole = False
        else:
            userRole = usermanager.IsDisable(current_user.id)

        for item in items:
            cardslist.append(Card(item))
        item_view_model = ViewModel(cardslist)
        return render_template('index.html', view_model=item_view_model, strRole=userRole)

  
    @app.route('/new', methods=['GET'])   # New Task
    @login_required
    def getnew_post():
        if (app.config['LOGIN_DISABLED']) or (usermanager.IsRoleAdmin(current_user.id)) or (usermanager.IsRoleWriter(current_user.id)):
            return render_template('new_task.html')
        return render_template("access_error.html",error="insufficient privileges!")


    @app.route('/home', methods=['POST'])   # New Task
    @login_required
    def post_index():
        if (app.config['LOGIN_DISABLED']) or (usermanager.IsRoleAdmin(current_user.id)) or (usermanager.IsRoleWriter(current_user.id)):
            response = todo.create_task(
                name = request.form['title'],
                due = request.form['duedate'],
                desc = request.form['descarea']
            )        
            if (str(response) != ""):
                return redirect('/home')
            else:
                return render_template("error.html",error="failed to create task!")
        
        return render_template("access_error.html",error="insufficient privileges!")

    
    @app.route('/edit/<id>', methods=['GET']) #Edit task
    @login_required
    def get_edit(id):
        if (app.config['LOGIN_DISABLED']) or (usermanager.IsRoleAdmin(current_user.id)) or (usermanager.IsRoleWriter(current_user.id)):
            item = todo.get_task(id=id)
            if (str(item) != ""):
                item_info = Card(item)
                return render_template('edit.html', task=item_info)
            else:
                return render_template("error.html", error="failed to obtain task info!")
        return render_template("access_error.html",error="insufficient privileges!")

    @app.route('/edit/<id>', methods=['POST']) #Edit task
    @login_required
    def post_edit(id):
        if (app.config['LOGIN_DISABLED']) or (usermanager.IsRoleAdmin(current_user.id)) or (usermanager.IsRoleWriter(current_user.id)):
            response= todo.update_task(
                id = id,
                name = request.form['title'],
                desc = request.form['descarea'],
                due = request.form['duedate'],
                status = request.form['status']
            )
            if (str(response) != ""):
                return redirect('/home')
            else:
                return render_template("error.html", error="failed to update task!")
        return render_template("access_error.html",error="insufficient privileges!")
    
    @app.route('/delete/<id>') # delete task
    @login_required
    def delete(id):
        if (app.config['LOGIN_DISABLED']) or (usermanager.IsRoleAdmin(current_user.id)) or (usermanager.IsRoleWriter(current_user.id)):
            response = todo.delete_task(id=id)
            if str(response) != "":
                return redirect('/home')
            else:
                return render_template("error.html",error="failed to delete task!") 
        return render_template("access_error.html",error="insufficient privileges!")
    
    ### Additional views ###
    @app.route('/getpreviousdonetasks', methods=['GET'])
    @login_required
    def get_previous_done_tasks():
        cardslist = []
        qry = {
            "status": "Done",
            "dateLastActivity": {"$lt": datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d')}    
        }
        items = todo.get_qryItems(qry)
        for item in items:
            cardslist.append(Card(item))
        item_view_model = ViewModel(cardslist)
        userRole = usermanager.IsDisable(current_user.id)
        return render_template('previous_done_task.html', view_model=item_view_model, strRole=userRole)

    
    @app.route('/gettodaydonetasks', methods=['GET'])
    @login_required
    def get_today_done_tasks():
        cardslist = []
        qry = {
            "status": "Done",
            "dateLastActivity": datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d')    
        }
        items = todo.get_qryItems(qry)
        for item in items:
            cardslist.append(Card(item))
        item_view_model = ViewModel(cardslist)
        userRole = usermanager.IsDisable(current_user.id)
        return render_template('today_done_task.html', view_model=item_view_model, strRole=userRole)

############# UserManagement ##########################

    @app.route('/usermanager', methods=['GET'])  #portal
    @login_required
    def get_usermanager():
        if usermanager.IsRoleAdmin(current_user.id):
            user_list = []
            items = usermanager.get_AllUsers()
            for item in items:
                user_list.append(User(item))
            item_view_model = ViewModel(user_list)
            return render_template('userManager.html', view_model=item_view_model)        
        return render_template("access_error.html",error="insufficient privileges!")
    
    @app.route('/edituser/<id>', methods=['GET']) #Edit user
    @login_required
    def get_edituser(id):
        if usermanager.IsRoleAdmin(current_user.id):
            item = usermanager.get_user(id=id)
            if (str(item) != ""):
                item_info = User(item)
                return render_template('editUser.html', user=item_info)
            else:
                return render_template("error.html", error="failed to obtain user info!")
        return render_template("access_error.html",error="insufficient privileges!")
    
    @app.route('/edituser/<id>', methods=['POST']) #Edit user
    @login_required
    def post_edituser(id):
        if usermanager.IsRoleAdmin(current_user.id):
            response= usermanager.update_user(
                id = id,
                username = request.form['username'],
                role = request.form['role']
            )
            if (str(response) != ""):
                return redirect('/usermanager')
            else:
                return render_template("error.html", error="failed to update user!")
        return render_template("access_error.html",error="insufficient privileges!")
    
    @app.route('/deleteuser/<id>') # delete user
    @login_required
    def deleteuser(id):
        if usermanager.IsRoleAdmin(current_user.id):
            response = usermanager.delete_user(id=id)
            if str(response) != "":
                return redirect('/usermanager')
            else:
                return render_template("error.html",error="failed to delete user!")
        return render_template("access_error.html",error="insufficient privileges!")  

###############################################
      
    
    return app

