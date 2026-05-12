from flask import render_template, Flask
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

# FLASK APP SET-UP

app = Flask(__name__)

# LOGIC OF PROGRAM

# VARIABLES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = os.path.join(BASE_DIR, "tasks.json")

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

if __name__ == '__main__':
    app.run(debug=True)