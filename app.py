from flask import render_template, Flask, redirect, request, flash
import logging
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin


# LOGGER SET-UP CONFIGURATIONS

logging.basicConfig(
    filename="info.log",
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# PATH VARIABLES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = os.path.join(BASE_DIR, "tasks.json")

# FLASK APP SET-UP
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'KEY2222'

# DATABASE SETUP
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db) 

# initialize the app with the extension
db.init_app(app)

# FOR PASSWORD HASHING
bcrypt = Bcrypt(app)

# session
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# MODELS
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_value = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


# LOGIC OF PROGRAM

def load_data():
    try:
        data = db.session.execute(db.select(Task).filter_by(user_id=current_user.id)).scalars().all()
        logger.info("Data loaded successfully!")
    except Exception as e:
        logger.exception("Unable to find the file!")
        data = []
    return data

def store_data(task, priority_value):
    value = Task(
            task_value=task,
            priority=priority_value,
            user_id = current_user.id
        )
    db.session.add(value)
    db.session.commit()
    return 'added successfully'

def store_user(name, hpass):
    user =User(
        user_name =name,
        password = hpass
    )
    db.session.add(user)
    db.session.commit()
    return 'added successfully'

# HELPER FUNCTION
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, int(user_id))

# ROUTING FUCNTIONS

# HOME ROUTE 
@app.route('/')
@login_required
def home(): 
    data = load_data()
    return render_template('index.html', data = data)

# SIGN-UP ROUTE
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    logger.info("Signup operation called.")
    if request.method == 'POST':
        user_name = request.form.get('user_name', '').strip()
        password = request.form.get('password', '').strip()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = db.session.execute(db.select(User).filter_by(user_name=user_name)).scalar_one_or_none()
        if existing_user:
            flash('Username already exists')
            return redirect('/signup')
        store_user(user_name, hashed_password)
        return redirect('/')

    return render_template('signup.html')

# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    logger.info("login operation called.")
    if request.method == 'POST':
        user_name = request.form.get('user_name', '').strip()
        password = request.form.get('password', '').strip()
        user = db.session.execute(db.select(User).filter_by(user_name=user_name)).scalar_one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            logger.info('login success!')
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid username or password')
            return redirect('/login')
    return render_template('login.html')

# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ADD TASK ROUTE
@app.route('/add/', methods=['POST'])
def post_data():
    logger.info("Add operation called.")
    task = request.form.get('task', '').strip()
    priority = request.form.get('priority', '').strip()
    store_data(task, priority)
        
    return redirect('/')

# FINISH TASK ROUTE
@app.route('/done/<int:index>', methods=['POST'])
def done_task(index):
    logger.info("Done operation called.")
    task = db.get_or_404(Task, index)
    db.session.delete(task)
    db.session.commit()

    return redirect('/')

# EDIT TASK ROUTE
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    logger.info("Edit operation called.")
    current_task = db.get_or_404(Task, index)
    if request.method == 'POST':
        current_task.task_value = request.form.get('task', '').strip()
        current_task.priority = request.form.get('priority', '').strip()
        db.session.commit()
        
        return redirect('/')

    return render_template('edit.html', current_task = current_task)


# APP START
if __name__ == '__main__':
    app.run(debug=True)