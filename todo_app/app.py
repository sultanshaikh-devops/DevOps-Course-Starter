import os, requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
from loggly.handlers import HTTPSHandler
from pythonjsonlogger import jsonlogger
from todo_app.models.view import ViewModel
from todo_app.models.card import Card
from todo_app.models.user import User
from todo_app.adapters.mongodb_todo import *
from todo_app.adapters.MongoDbUserService import *


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
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        formatter = jsonlogger.JsonFormatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s %(requesterIpAddr)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    client_id = os.environ['GITHUB_CLIENT_ID']
    client_secret = os.environ['GITHUB_CLIENT_SECRET']
    base_url="https://api.github.com"
    authorization_url="https://github.com/login/oauth/authorize"
    token_endpoint = "https://github.com/login/oauth/access_token"

    client = WebApplicationClient(client_id)
    todo = mongodb_todo()
    usermanager = MongoDbUserService()

    login_manager = LoginManager()
    login_manager.init_app(app)

    def write_log_entry(message, method, requesterIpAddr, url, status_code, data):
        app.logger.error(message, extra={
            "method": "{}".format(method),
            "requesterIpAddr": "{}".format(requesterIpAddr),
            "url": "{}".format(url),
            "status_code": "{}".format(status_code),
            "data": "{}".format(data)
        })


    @app.errorhandler(Exception)
    def handle_error(e):
        app.logger.error('exception', extra={
            "method": "{}".format(request.method),
            "requesterIpAddr": "{}".format(request.remote_addr),
            "url": "{}".format(request.url)
        }, exc_info=True)

        return render_template("error.html", error=str(e))
    
    @app.after_request
    def after_request(response):
        write_log_entry('after_request',request.method,request.remote_addr,request.url,response.status,"")
        # app.logger.info("after_request", extra={
        #     "method": "{}".format(request.method),
        #     "requesterIpAddr": "{}".format(request.remote_addr),
        #     "url": "{}".format(request.url),
        #     "status_code": "{}".format(response.status)
        # })
        return response

    @login_manager.user_loader
    def load_user(user_id):        
        return UserToLogin(user_id)
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        write_log_entry('Unauthorized attemp made',request.method,request.remote_addr,request.url,"None","None")
        # app.logger.info("Unauthorized attemp made.", extra={
        #     "method": "{}".format(request.method),
        #     "requesterIpAddr": "{}".format(request.remote_addr),
        #     "url": "{}".format(request.url)
        # })
        return redirect(url_for('login'))
    
    @app.route('/logout')
    @login_required
    def logout():
        write_log_entry("User {} logged out of the system.".format(current_user.id),request.method,request.remote_addr,request.url,"None","None")
        # app.logger.info("User {} logged out of the system.".format(current_user.id), extra={
        #     "method": "{}".format(request.method),
        #     "requesterIpAddr": "{}".format(request.remote_addr),
        #     "url": "{}".format(request.url)
        # })
        logout_user()
        session.clear()        
        return redirect("https://github.com/logout")
    
    @app.route("/login")
    def login():
        request_uri = client.prepare_request_uri(
            authorization_url,
            redirect_uri=request.base_url + "/callback",
            scope=None,
        )
        return redirect(request_uri)

    @app.route("/login/callback")
    def callback():
        code = request.args.get("code")
        app.logger.debug("{}".format(code), extra={
            "method": "{}".format(request.method),
            "requesterIpAddr": "{}".format(request.remote_addr),
            "url": "{}".format(request.url)
        })

        # Prepare and send request to get tokens! 
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(client_id, client_secret),
        )

        if token_response.status_code != 200:
            app.logger.warning("Unable to get token from github.", extra={
                "method": "{}".format(request.method),
                "requesterIpAddr": "{}".format(request.remote_addr),
                "url": "{}".format(request.url)
            })
            return redirect(url_for('login'))

        json_data = token_response.content.decode('utf8').replace("'", '"')
        # Parse the tokens!
        client.parse_request_body_response(json_data)
        userinfo_endpoint = "{}/user".format(base_url)
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.ok:
            account_info_json = userinfo_response.json()
            currentUserName = str(account_info_json['login'])               
            login_user(UserToLogin(currentUserName))
            app.logger.info("User logged in {}".format(current_user.id), extra={
                "method": "{}".format(request.method),
                "requesterIpAddr": "{}".format(request.remote_addr),
                "url": "{}".format(request.url)
            })

            if usermanager.get_totalusercount() == 0:
                usermanager.create_user(username=currentUserName,role="admin")
                write_log_entry("User logged in {} has been give admin level access.".format(current_user.id),request.method,request.remote_addr,request.url,"None", "None")
                # app.logger.info("User logged in {} has been give admin level access.".format(current_user.id), extra={
                #     "method": "{}".format(request.method),
                #     "requesterIpAddr": "{}".format(request.remote_addr),
                #     "url": "{}".format(request.url)
                # })
            
            if (usermanager.get_totalusercount() > 0) and (usermanager.get_findusercount(qry={"username": currentUserName}) == 0):
                usermanager.create_user(username=currentUserName,role="read")
                write_log_entry("User logged in {} has been give read level access.".format(current_user.id),request.method,request.remote_addr,request.url,"None", "None")
                # app.logger.info("User logged in {} has been give read level access.".format(current_user.id), extra={
                #     "method": "{}".format(request.method),
                #     "requesterIpAddr": "{}".format(request.remote_addr),
                #     "url": "{}".format(request.url)
                # })

        return redirect(url_for('get_index'))


    @app.route('/', methods=['GET'])
    @login_required
    def sendhome():
        return redirect(url_for('get_index'))


    ##### Core TODO_Tasks#####
    #error handling for 404
    # @app.errorhandler(404)
    # def not_found(e):
    #     return render_template("error.html", error='resource not found!')

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
            userRole = usermanager.IsDisable()

        for item in items:
            cardslist.append(Card(item))
        item_view_model = ViewModel(cardslist)
        return render_template('index.html', view_model=item_view_model, strRole=userRole)

  
    @app.route('/new', methods=['GET'])   # New Task
    @login_required
    @usermanager.hasWritePermission
    def getnew_post():
        return render_template('new_task.html')

    @app.route('/home', methods=['POST'])   # New Task
    @login_required
    @usermanager.hasWritePermission
    def post_index():
        response = todo.create_task(
            name = request.form['title'],
            due = request.form['duedate'],
            desc = request.form['descarea']
        )        
        if response is not None:
            if current_app.config["LOGIN_DISABLED"]==False:
                write_log_entry("{} create new task".format(current_user.id),request.method,request.remote_addr,request.url,"None","name: {} due: {} desc: {}".format(request.form['title'], str(request.form['duedate']), request.form['descarea']))
                # app.logger.info("{} create new task".format(current_user.id), extra={
                #     "method": "{}".format(request.method),
                #     "requesterIpAddr": "{}".format(request.remote_addr),
                #     "url": "{}".format(request.url),
                #     "data": "name: {} due: {} desc: {}".format(request.form['title'], str(request.form['duedate']), request.form['descarea'])
                # })
            return redirect('/home')
        else:
            return render_template("error.html",error="failed to create task!")

    
    @app.route('/edit/<id>', methods=['GET']) #Edit task
    @login_required
    @usermanager.hasWritePermission
    def get_edit(id):
        item = todo.get_task(id=id)
        if item is not None:
            item_info = Card(item)
            return render_template('edit.html', task=item_info)
        else:
            return render_template("error.html", error="failed to obtain task info!")

    @app.route('/edit/<id>', methods=['POST']) #Edit task
    @login_required
    @usermanager.hasWritePermission
    def post_edit(id):
        response= todo.update_task(
            id = id,
            name = request.form['title'],
            desc = request.form['descarea'],
            due = request.form['duedate'],
            status = request.form['status']
        )
        if response is not None:
            if current_app.config["LOGIN_DISABLED"]==False:
                write_log_entry("{} update task".format(current_user.id),request.method,request.remote_addr,request.url,"None","id: {} name: {} due: {} desc: {} status: {}".format(id, request.form['title'], str(request.form['duedate']), request.form['descarea'], request.form['status']))
                # app.logger.info("{} update task".format(current_user.id), extra={
                #     "method": "{}".format(request.method),
                #     "requesterIpAddr": "{}".format(request.remote_addr),
                #     "url": "{}".format(request.url),
                #     "data": "id: {} name: {} due: {} desc: {} status: {}".format(id, request.form['title'], str(request.form['duedate']), request.form['descarea'], request.form['status'])
                # })
            return redirect('/home')
        else:
            return render_template("error.html", error="failed to update task!")
    
    @app.route('/delete/<id>') # delete task
    @login_required
    @usermanager.hasWritePermission
    def delete(id):
        response = todo.delete_task(id=id)
        if response is not None: 
            if current_app.config["LOGIN_DISABLED"]==False:
                write_log_entry("{} deleted task".format(current_user.id),request.method,request.remote_addr,request.url,"None","id: {}".format(id))
                # app.logger.info("{} deleted task".format(current_user.id), extra={
                #     "method": "{}".format(request.method),
                #     "requesterIpAddr": "{}".format(request.remote_addr),
                #     "url": "{}".format(request.url),
                #     "data": "id: {}".format(id)
                # })
            return redirect('/home')
        else:
            return render_template("error.html",error="failed to delete task!") 
    
    ### Additional views ###
    @app.route('/getpreviousdonetasks', methods=['GET'])
    @login_required
    def get_previous_done_tasks():
        cardslist = []
        items = todo.get_older_done_task()
        for item in items:
            cardslist.append(Card(item))
        item_view_model = ViewModel(cardslist)
        userRole = usermanager.IsDisable()
        return render_template('previous_done_task.html', view_model=item_view_model, strRole=userRole)

    
    @app.route('/gettodaydonetasks', methods=['GET'])
    @login_required
    def get_today_done_tasks():
        cardslist = []
        items = todo.get_today_done_task()
        for item in items:
            cardslist.append(Card(item))
        item_view_model = ViewModel(cardslist)
        userRole = usermanager.IsDisable()
        return render_template('today_done_task.html', view_model=item_view_model, strRole=userRole)

############# UserManagement ##########################

    @app.route('/usermanager', methods=['GET'])  #portal
    @login_required
    @usermanager.hasRoleAdmin
    def get_usermanager():
        user_list = []
        items = usermanager.get_AllUsers()
        for item in items:
            user_list.append(User(item))
        item_view_model = ViewModel(user_list)
        return render_template('userManager.html', view_model=item_view_model)        
    
    @app.route('/edituser/<id>', methods=['GET']) #Edit user
    @login_required
    @usermanager.hasRoleAdmin
    def get_edituser(id):
        item = usermanager.get_user(id=id)
        if item is not None:
            item_info = User(item)
            return render_template('editUser.html', user=item_info)
        else:
            return render_template("error.html", error="failed to obtain user info!")

    
    @app.route('/edituser/<id>', methods=['POST']) #Edit user
    @login_required
    @usermanager.hasRoleAdmin
    def post_edituser(id):
        response = usermanager.update_user(
            id = id,
            username = request.form['username'],
            role = request.form['role']
        )
        if response is not None:
            write_log_entry("{} updated user permission".format(current_user.id),request.method,request.remote_addr,request.url,"None","id: {} username: {} role: {}".format(id, request.form['username'], request.form['role']))
            # app.logger.info("{} updated user permission".format(current_user.id), extra={
            #     "method": "{}".format(request.method),
            #     "requesterIpAddr": "{}".format(request.remote_addr),
            #     "url": "{}".format(request.url),
            #     "data": "id: {} username: {} role: {}".format(id, request.form['username'], request.form['role'])
            # })
            return redirect('/usermanager')
        else:
            return render_template("error.html", error="failed to update user!")

    
    @app.route('/deleteuser/<id>') # delete user
    @login_required
    @usermanager.hasRoleAdmin
    def deleteuser(id):
        response = usermanager.delete_user(id=id)
        if response is not None:
            write_log_entry("{} deleted user".format(current_user.id),request.method,request.remote_addr,request.url,"None","id: {}".format(id))
            # app.logger.info("{} deleted user".format(current_user.id), extra={
            #     "method": "{}".format(request.method),
            #     "requesterIpAddr": "{}".format(request.remote_addr),
            #     "url": "{}".format(request.url),
            #     "data": "id: {}".format(id)
            # })
            return redirect('/usermanager')
        else:
            return render_template("error.html",error="failed to delete user!")

###############################################
      
    
    return app

