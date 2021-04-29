import os
from flask import Flask, render_template, request, redirect
#from todo_app.flask_config import Config
from todo_app.trelloclient import *
from todo_app.view import ViewModel
from todo_app.models.card import Card


#app = Flask(__name__)
#app.config.from_object(Config)


def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    statusMappingList = []
    board_Name = os.environ['TRELLO_BOARD_NAME']
    board_Id = ""

    def build_status_mapping():
        cboard = TrelloClient()
        result = cboard.get_AllBoardList()
        if result.status_code == 200:
            for item in result.json():
                if item['name'] == board_Name:
                    board_Id = item['id']  
        else:        
            print( f'Trello Board {board_Name} not found!' )
            raise SystemExit

        if not (board_Id is None):
            cTrelloClient = TrelloClient()
            TrelloClients = cTrelloClient.get_BoardLists(id=board_Id)
            if TrelloClients.status_code == 200:
                for list in TrelloClients.json():
                    if list['name'] == 'To Do':
                        statusMappingList.append(StatusMapping(list_id=list['id'], status='Not Started'))
                    elif list['name'] == 'Doing':
                        statusMappingList.append(StatusMapping(list_id=list['id'], status='In Progress'))
                    elif list['name'] == 'Done':
                        statusMappingList.append(StatusMapping(list_id=list['id'], status='Completed'))
                    else:
                        pass  #do nothing
            else:            
                print("problem connecting to Trello API endpoint")
                raise SystemExit         
        else:
            print( f"Trello Board {board_Name} not found!")
            raise SystemExit

    def get_listId(status):
        for item in statusMappingList:
            if item.status == status:
                listid = item.list_id
        return listid

    def get_statusLabel(list_id):
        for item in statusMappingList:
            if item.list_id == list_id:
                listStatus = item.status
        return listStatus

    build_status_mapping()


    # error handling for 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error='resource not found!')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    # default
    @app.route('/', methods=['GET'])
    def get_index():
        cardslist = []
        for status_mapping in statusMappingList:
            cbl_board = TrelloClient()
            result = cbl_board.get_ListCards(status_mapping.list_id)    
            if result.status_code == 200:
                for card in result.json():
                    if not (card['due'] is None):
                        card['due'] = (card['due']).split("T")[0]
                    card['dateLastActivity'] = (card['dateLastActivity']).split("T")[0]
                    cardslist.append( Card(card=card, statuslabel=status_mapping.status) )    
            else:
                return render_template("error.html",error="failed to get Trello cards!")    
        #return render_template('index.html', tasks=cardslist)
        item_view_model = ViewModel(cardslist)
        return render_template('index.html', view_model=item_view_model)

    # new task
    @app.route('/new', methods=['GET'])
    def getnew_post():
        return render_template('new_task.html')

    @app.route('/', methods=['POST'])
    def post_index():    
        cbl = TrelloClient()
        result = cbl.create_Card(
            name = request.form['title'],
            due = request.form['duedate'],
            desc = request.form['descarea'],
            id = get_listId(status='Not Started')
        )
        
        if (result.status_code == 200):
            return redirect('/')
        else:
            return render_template("error.html",error="failed to create Trello card!")

    # edit task
    @app.route('/edit/<id>', methods=['GET'])
    def get_edit(id):
        cbl = TrelloClient()
        result = cbl.get_Card(id=id)
        if (result.status_code == 200):
            card_info = Card(
            card = result.json(),
            statuslabel = get_statusLabel(result.json()['idList'])
            )
            return render_template('edit.html', task=card_info)
        else:
            return render_template("error.html", error="failed to obtain Trello card info!")

    @app.route('/edit/<id>', methods=['POST'])
    def post_edit(id):
        cbl = TrelloClient()
        result = cbl.update_Card(
            id = id,
            listId = get_listId(status=request.form['status']),
            name = request.form['title'],
            desc = request.form['descarea'],
            due = request.form['duedate']
        )
        if result.status_code == 200:
            return redirect('/')
        else:
            return render_template("error.html", error="failed to update Trello card!")

    # delete task
    @app.route('/delete/<id>')
    def delete(id):
        cbl = TrelloClient()
        result = cbl.delete_Card(id=id)
        if result.status_code == 200:
            return redirect('/')
        else:
            return render_template("error.html",error="failed to delete Trello card!")



    return app

