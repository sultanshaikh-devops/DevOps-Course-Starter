from os import error
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.trelloclient import *


app = Flask(__name__)
app.config.from_object(Config)

status_mapping = []
board_Name = "ToDo"
board_Id = ""

def build_status_mapping():
    trello_Board = TrelloBoard()
    result = trello_Board.get_BoardList()
    if result.status_code == 200:
        for item in result.json():
            if item['name'] == board_Name:
                board_Id = item['id']   
    else:
        return render_template("404.html", error="Trello board 'ToDo' not found!")

    if not (board_Id is None):
        trello_List = TrelloList()
        lists = trello_List.get_List(id=board_Id)
        if lists.status_code == 200:
            for list in lists.json():
                if list['name'] == 'To Do':
                    status_mapping.append ({
                        'id' : list['id'],
                        'status' : "Not Started"
                    })
                elif list['name'] == 'Doing':
                    status_mapping.append ({
                        'id' : list['id'],
                        'status' : "In Progress"
                    })
                elif list['name'] == 'Done':
                    status_mapping.append ({
                        'id' : list['id'],
                        'status' : "Completed"
                    })
                else:
                    pass
                    #do nothing
        else:
            return render_template("404.html", error="problem connecting to Trello API endpoint")           
    else:
        return render_template("404.html", error="Trello board 'ToDo' not found!") 

def get_listId(status):
    for item in status_mapping:
        if item['status'] == status:
            listid = item['id']
    return listid

def get_statusName(id):
    for item in status_mapping:
        if item['id'] == id:
            listStatus = item['status']
    return listStatus

build_status_mapping()

# error handling for 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", error='resource not found!')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# default
@app.route('/', methods=['GET'])
def get_index():
    cards = []
    for item in status_mapping:
        list_cards = TrelloCard()
        result = list_cards.get_List(id = item['id']) 
        if result.status_code == 200:
            for card in result.json():
                if not (card['due'] is None):
                    formated_date = (card['due']).split("T")[0]
                else:
                    formated_date = card['due']
                cards.append ({
                    'id' : card['id'],
                    'title': card['name'],
                    'status' : item['status'],
                    'due' : formated_date
                })
        else:
            return render_template("404.html",error="failed to get Trello cards!")    
    return render_template('index.html', tasks=cards)

# new task
@app.route('/new', methods=['GET'])
def getnew_post():
   return render_template('new_task.html')

@app.route('/', methods=['POST'])
def post_index():    
    card = TrelloCard()
    result = card.create_Card(
        name = request.form['title'],
        due = request.form['duedate'],
        desc = request.form['descarea'],
        id = get_listId(status='Not Started')
    )
    
    if (result.status_code == 200):
        return redirect('/')
    else:
        return render_template("404.html",error="failed to create Trello card!")

# edit task
@app.route('/edit/<id>', methods=['GET'])
def get_edit(id):
    card = TrelloCard()
    result = card.get_Card(id=id)
    if (result.status_code == 200):
        card_info = Card(
           json = result.json(),
           statusName = get_statusName(id=result.json()['idList'])
        )
        return render_template('edit.html', task=card_info)
    else:
        return render_template("404.html", error="failed to obtain Trello card info!")

@app.route('/edit/<id>', methods=['POST'])
def post_edit(id):
    card = TrelloCard()
    result = card.update_Card(
        id = id,
        listId = get_listId(status=request.form['status']),
        name = request.form['title'],
        desc = request.form['descarea'],
        due = request.form['duedate']
    )
    if result.status_code == 200:
        return redirect('/')
    else:
        return render_template("404.html", error="failed to update Trello card!")

# delete task
@app.route('/delete/<id>')
def delete(id):
    card = TrelloCard()
    result = card.delete_Card(id=id)
    if result.status_code == 200:
        return redirect('/')
    else:
        return render_template("404.html",error="failed to delete Trello card!")


if __name__ == '__main__':
    app.run(debug='true')