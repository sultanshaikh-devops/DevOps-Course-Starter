from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.trelloclient import *


app = Flask(__name__)
app.config.from_object(Config)

status_mapping = []

all_boards = TrelloClient.get_boards()
if all_boards.status_code == 200:
   for board in all_boards.json():
      if board['name'] == 'ToDo':
         board_id = board['id']

if not (board_id is None):
   all_list = TrelloClient.get_lists(boardid=board_id)
   if all_list.status_code == 200:
      for item in all_list.json():
         if item['name'] == "To Do":
            status_mapping.append ({
                  'id' : item['id'],
                  'status' : 'Not Started'
            })
         if item['name'] == "Doing":
            status_mapping.append ({
                  'id' : item['id'],
                  'status' : 'In Progress'
            })
         if item['name'] == "Done":
            status_mapping.append ({
                  'id' : item['id'],
                  'status' : 'Completed'
            })

def get_listid(listname):
    for item in status_mapping:
        if item['status'] == listname:
            listid = item['id']
    return listid

# error handling for 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

# default
@app.route('/', methods=['GET'])
def get_index():
    all_tasks = []

    for item in status_mapping:
        todotask = TrelloClient.list_card(listid = item['id'])

        if todotask.status_code == 200:
            for task in todotask.json():
                if not (task['due'] is None):
                    formated_date = (task['due']).split("T")[0]
                else:
                    formated_date = task['due']
                all_tasks.append ({
                    'id' : task['id'],
                    'title': task['name'],
                    'status' : item['status'],
                    'due' : formated_date
                })
        else:
            print("Problem getting To Do List")
    
    return render_template('index.html', tasks=all_tasks)

# new task
@app.route('/new', methods=['GET'])
def getnew_post():
   return render_template('new_task.html')

@app.route('/', methods=['POST'])
def post_index():    
    task_title = request.form['title']
    listId = get_listid(listname='Not Started')
    due = request.form['duedate']
    desc = request.form['descarea']
    new_card = TrelloClient.create_card(cardname=task_title, listid=listId, desc=desc, due=due)
    if (new_card.status_code == 200):
        return redirect('/')
    else:
        return render_template("404.html")

# delete task
@app.route('/delete/<id>')
def delete(id):
    result = TrelloClient.delete_card(cardid=id)
    if result.status_code == 200:
        return redirect('/')
    else:
        return render_template("404.html")

# edit task
@app.route('/edit/<id>', methods=['GET'])
def get_edit(id):
    task = []    
    result  = TrelloClient.get_card(cardid=id)
    if (result.status_code == 200):
        for item in status_mapping:
            if item['id'] == result.json()['idList']:
                task.append ({
                    'listid' : item['id'],
                    'id' : id,                     
                    'status' : item['status'],
                    'title' : result.json()['name'],
                    'due' : result.json()['due'],
                    'desc' : result.json()['desc']
                })
                return render_template('edit.html', task=task[0])
    else:
        return render_template("404.html")

@app.route('/edit/<id>', methods=['POST'])
def post_edit(id):
    name = request.form['title']
    status = request.form['status']
    due = request.form['duedate']
    desc = request.form['descarea']

    for item in status_mapping:
        if status == item['status']:
            update_card = TrelloClient.update_card(cardid=id,cardname=name,carddesc=desc,listid=item['id'],duedate=due)
            if update_card.status_code == 200:
                return redirect('/')
            else:
                return render_template("404.html")


if __name__ == '__main__':
    app.run(debug='true')