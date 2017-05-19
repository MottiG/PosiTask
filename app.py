from flask import Flask, url_for, request, render_template, jsonify, flash, redirect
from flask_bootstrap import Bootstrap
from task_db import TaskDB
from nocache import nocache

TASKS_TO_SERVE = 5
DB_FILENAME = 'db/dbshort.pickle'

app = Flask(__name__)
app.secret_key = 'many random bytes'
Bootstrap(app)

db = TaskDB(DB_FILENAME)


@app.route('/')
@nocache
def main():
    return render_template('explore.html', tasks=db.get_tasks_dict(), num_tasks=db.max_id)


@app.route('/create', methods=['GET', 'POST'])
@nocache
def create():
    if request.method == 'GET':
        return render_template('create.html', types=db.task_types)
    else:
        title = request.form['title']
        description = request.form['description']
        task_type = request.form['task_type']
        duration = request.form['duration']
        in_out_everywhere = request.form['in_out_everywhere']
        try:
            db.insert_task(title=title, desc=description, creator='Motti The King', in_out_everywhere=in_out_everywhere,
                           task_type=task_type, location='Jerusalem', duration=duration, value=1)
        except:
            flash('Task creation faild!', category='error')
            return redirect(url_for('create'))

        flash('Task created!', category='info')
        return redirect(url_for('main'))


@app.route('/do/<task_id>')
@nocache
def do(task_id=None):
    task = db.get_by_id(int(task_id))
    return render_template('do.html', task=task)


@app.route('/comments/')
@nocache
def comments():
    return render_template('comments.html')