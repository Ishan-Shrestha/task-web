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

def store_data(data):
    with open(FILE_DIR, 'w') as file:
            json.dump(data, file, indent=4)
    logger.info('Data is modified.')
    return 'added successfully'

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', data = data)

@app.route('/add/', methods=['POST'])
def post_data():
    logger.info("Add operation called.")
    data = load_data()
    task = request.form.get('task', '').strip()
    priority = request.form.get('priority', '').strip()
    new_id = str(len(data) + 1)
    data[new_id] = {
        "task": task,
        "priority": priority
    }
    store_data(data)
        
    return redirect('/')

@app.route('/done/<index>', methods=['POST'])
def done_task(index):
    logger.info("Done operation called.")
    data = load_data()
    if index in data:
        logger.info("Removed task: [%s]", data[index])
        del data[index]
    data = {k+1:v for k,v in enumerate(data.values())}
    store_data(data)

    return redirect('/')

@app.route('/edit/<index>', methods=['GET', 'POST'])
def edit_task(index):
    logger.info("Edit operation called.")
    data = load_data()
    current_task = data[index]
    if request.method == 'POST':
        data[index]['task'] = request.form.get('task','').strip()
        data[index]['priority']= request.form.get('priority', '').strip()
        store_data(data)
        return redirect('/')

    return render_template('edit.html', current_task = current_task, index=index)

if __name__ == '__main__':
    app.run(debug=True)