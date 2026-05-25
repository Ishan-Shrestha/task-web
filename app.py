from flask import render_template, Flask, redirect, request
import logging
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# LOGGER SET-UP CONFIGURATIONS

logging.basicConfig(
    filename="info.log",
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# VARIABLES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = os.path.join(BASE_DIR, "tasks.json")

# FLASK APP SET-UP
app = Flask(__name__)

# DATABASE SETUP
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# MODEL 
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

# LOGIC OF PROGRAM

def load_data():
    try:
        data = db.session.execute(db.select(Task)).scalars().all()
        logger.info("Data loaded successfully!")
    except Exception as e:
        logger.exception("Unable to find the file!")
        data = []
    return data

def store_data(task_value, priority_value):
    value = Task(
            task=task_value,
            priority=priority_value,
        )
    db.session.add(value)
    db.session.commit()
    return 'added successfully'

@app.route('/')
def home(): 
    data = load_data()
    return render_template('index.html', data = data)

@app.route('/add/', methods=['POST'])
def post_data():
    logger.info("Add operation called.")
    task = request.form.get('task', '').strip()
    priority = request.form.get('priority', '').strip()
    store_data(task, priority)
        
    return redirect('/')

@app.route('/done/<int:index>', methods=['POST'])
def done_task(index):
    logger.info("Done operation called.")
    task = db.get_or_404(Task, index)
    db.session.delete(task)
    db.session.commit()

    return redirect('/')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    logger.info("Edit operation called.")
    current_task = db.get_or_404(Task, index)
    if request.method == 'POST':
        current_task.task = request.form.get('task', '').strip()
        current_task.priority = request.form.get('priority', '').strip()
        db.session.commit()
        
        return redirect('/')

    return render_template('edit.html', current_task = current_task)

if __name__ == '__main__':
    app.run(debug=True)