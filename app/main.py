from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__, static_folder='static', template_folder='templates')

# é necessário um secret_key para que a sessão da aplicação não fique acessível para qualquer um
app.config['SECRET_KEY'] = '*#caleum&*'
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "admins"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)


class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console

    def save(self):
        db.connection.cursor().execute('INSERT into jogo (nome, categoria, console) values (%s, %s, %s)',
                                       (self.nome, self.categoria, self.console))
        db.connection.commit()

    @staticmethod
    def get_all():
        cursor = db.connection.cursor()
        cursor.execute('SELECT id, nome, categoria, console from jogo')
        jogos = Jogo.traduz_jogos(cursor.fetchall())

        return jogos

    @staticmethod
    def get(id):
        cursor = db.connection.cursor()
        cursor.execute('SELECT id, nome, categoria, console from jogo where id = %s', (id,))
        jogo = Jogo.traduz_jogos((cursor.fetchone(),))
        return jogo

    @staticmethod
    def traduz_jogos(jogos):
        def cria_jogo_com_tupla(tupla):
            return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

        return map(cria_jogo_com_tupla, jogos)

    @staticmethod
    def delete(id):
        db.connection.cursor().execute('delete from jogo where id = %s', (id,))
        db.connection.commit()


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

    def save(self):
        print('salvo')

    @staticmethod
    def get_by_id(id):
        print('lista')


@app.route('/')
def index():
    jogos = Jogo.get_all()
    return render_template('index.html', jogos=jogos)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuarios.get(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.nome
            next = request.form['next']

            return redirect(next or url_for('index'))
    return abort(401)


@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    return index()


@app.route('/novo')
def novo():
    categorias = ['RPG', 'Ação', 'FPS', 'Indie', 'Esporte']
    if session.get('usuario_logado'):
        return render_template('novo.html', categorias=categorias)
    else:
        return render_template('login.html', next=url_for('novo'))


@app.route('/criar', methods=['GET','POST'])
def criar():
    if session['usuario_logado']:
        novo_jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'])
        novo_jogo.save()
        return redirect(url_for('index'))
    else:
        return render_template('login.html', next=request.url)


@app.route('/deletar/<int:identificador>')
def deletar(identificador):
    """ Remove um jogo da lista """
    Jogo.delete(int(identificador))
    return jsonify(id=identificador)


@app.errorhandler(404)
def pagina_nao_encontrada():
    return render_template('404.html'), 404


@app.errorhandler(401)
def nao_autorizado():
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
