from flask import Flask


app = Flask(__name__, static_folder='public')


@app.route('/')
def hello():
    return app.send_static_file('main.html')
