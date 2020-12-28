import sys
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items import *

app = Flask(__name__)
app.config.from_object(Config)

#error handling for 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

#default
@app.route('/', methods=['GET'])
def get_index():
    all_tasks = get_items()
    return render_template('index.html', tasks=all_tasks)

@app.route('/', methods=['POST'])
def post_index():
    task_title = request.form['title']
    task_status = request.form['status']
    add_item(title=task_title, status=task_status)
    return redirect('/')

#new task
@app.route('/new', methods=['GET'])
def getnew_post():
   return render_template('new_task.html')

#edit task
@app.route('/edit/<int:id>', methods=['GET'])
def get_edit(id):
    task = get_item(id)
    return render_template('edit.html', task=task)

@app.route('/edit/<int:id>', methods=['POST'])
def post_edit(id):
    task = get_item(id)
    task['title'] = request.form['title']
    task['status'] = request.form['status']
    save_item(task)
    return redirect('/')

#delete task
@app.route('/delete/<int:id>')
def delete(id):
    delete_item(id)
    return redirect('/')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=1)
