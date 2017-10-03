from flask import Flask, render_template


app = Flask(__name__, static_folder='public', template_folder='template')


@app.route('/')
def hello():
    return render_template('teste.html', lista=range(10))


app.run()
