from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__, static_folder='static', template_folder='templates')

app.config.from_pyfile('config.py')
db = MySQL(app)

from app.views import *

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
