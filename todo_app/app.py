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
@app.route('/', methods=['GET', 'POST'])
def index():
    #return 'Hello World!'
    if request.method == 'POST':
        task_title = request.form['title']
        task_status = request.form['status']
        add_item(title=task_title, status=task_status)
        return redirect('/')
    else:
        all_tasks = get_items()
        return render_template('index.html', tasks=all_tasks)

#new task
@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        task_title = request.form['title']
        task_status = request.form['status']
        add_item(title=task_title, status=task_status)
        return redirect('/')
    else:
        return render_template('new_task.html')

#edit task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = get_item(id)
    print(task, file=sys.stderr)
    print(task, file=sys.stdout)
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['status'] = request.form['status']
        save_item(task)
        return redirect('/')
    else:
        return render_template('edit.html', task=task)

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
