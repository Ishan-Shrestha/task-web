from flask import render_template, Flask, redirect, request
import logging
import os
import json

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

# LOGIC OF PROGRAM

def load_data():
    try:
        with open(FILE_DIR, 'r') as file:
            data = json.load(file)
            logger.info("Data loaded successfully!")
    except FileNotFoundError as e:
        logger.exception("Unable to find the file!")
        data = {}
    return data

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', data = data)

@app.route('/add/', methods=['POST'])
def post_data():
    data = load_data()
    task = request.form.get('task', '').strip()
    priority = request.form.get('priority', '').strip()
    new_id = str(len(data) + 1)
    data[new_id] = {
        "task": task,
        "priority": priority
    }
    with open(FILE_DIR, 'w') as file:
        json.dump(data, file, indent=4)
        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)