from asyncio import taskgroups
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

# Task model(database table)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form.get('task')
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ ==("__main__"):
    app.run(debug=True)