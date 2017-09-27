from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, flash, \
    send_from_directory
import os
from functools import wraps
from flask_mysqldb import MySQL

SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'

RAIZ_APP = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='static', template_folder='templates')

# é necessário um secret_key para que a sessão da aplicação não fique acessível para qualquer um
app.config['SECRET_KEY'] = '*#caleum&*'
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "admin"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_FOLDER'] = RAIZ_APP + '/uploads'


db = MySQL(app)


class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console

    def save(self):
        cursor = db.connection.cursor()
        if self.id:
            cursor.execute(SQL_ATUALIZA_JOGO,
                                           (self.nome, self.categoria, self.console, self.id))
        else:
            cursor.execute(SQL_CRIA_JOGO,
                                           (self.nome, self.categoria, self.console))
            self.id = cursor.lastrowid
        db.connection.commit()
        return self

    @staticmethod
    def get_all():
        cursor = db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = Jogo.traduz_jogos(cursor.fetchall())

        return jogos

    @staticmethod
    def get(id):
        cursor = db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        jogo = Jogo.traduz_jogos((cursor.fetchone(),))[0]
        return jogo

    @staticmethod
    def traduz_jogos(jogos):
        def cria_jogo_com_tupla(tupla):
            return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

        return list(map(cria_jogo_com_tupla, jogos))

    @staticmethod
    def delete(id):
        db.connection.cursor().execute(SQL_DELETA_JOGO, (id,))
        db.connection.commit()
        deleta_foto(id)


def deleta_foto(jogo_id):
    foto = 'foto{id}.jpg'.format(id=jogo_id)
    pasta = os.listdir(app.config['UPLOAD_FOLDER'])
    if foto in pasta:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], foto))


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

    def save(self):
        print('salvo')

    @staticmethod
    def traduz_usuario(tupla):
        return Usuario(tupla[0], tupla[1], tupla[2])

    @staticmethod
    def get(id):
        cursor = db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = Usuario.traduz_usuario(dados) if dados else None
        return usuario


def protegida(f):
    @wraps(f)
    def valida_usuario(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] is None:
            return redirect(url_for('login', proxima=request.url))
        return f(*args, **kwargs)
    return valida_usuario


@app.route('/')
def index():
    jogos = Jogo.get_all()
    return render_template('index.html', jogos=jogos)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuario.get(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.nome
            proxima_pagina = request.form['proxima']

            return redirect(proxima_pagina or url_for('index'))
    return abort(401)


@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash('Usuário não está mais logado.')
    return redirect(url_for('index'))


@app.route('/novo')
@protegida
def novo():
    categorias = ['RPG', 'Ação', 'FPS', 'Indie', 'Esporte']
    return render_template('novo.html', categorias=categorias)


@app.route('/criar', methods=['GET', 'POST'])
@protegida
def criar():
    novo_jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'])
    jogo_salvo = novo_jogo.save()
    message = 'Jogo criado com sucesso!'
    if 'nome_arquivo' in request.files:
        arquivo = request.files['nome_arquivo']
        if arquivo.filename != '':
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            if extensao != 'jpg':
                message = 'Jogo criado , mas formato da foto deve ser jpg.'
            else:
                arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                          'foto{id}.jpg'.format(id=jogo_salvo.id)))
    flash(message)
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
@protegida
def editar(id):
    categorias = ['RPG', 'Ação', 'FPS', 'Indie', 'Esporte']
    jogo = Jogo.get(id)
    return render_template('editar.html', jogo=jogo, categorias=categorias)


@app.route('/atualizar', methods=['GET', 'POST'])
@protegida
def atualizar():
    jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'], id=request.form['id'])
    jogo.save()
    message = 'Jogo atualizado com sucesso!'
    if 'nome_arquivo' in request.files:
        arquivo = request.files['nome_arquivo']
        if arquivo.filename != '':
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            if extensao != 'jpg':
                message = 'Jogo atualizado , mas formato da foto deve ser jpg.'
            else:
                arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                          'foto{id}.jpg'.format(id=jogo.id)))
    flash(message)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    Jogo.delete(int(id))
    return jsonify(id=id)


@app.route('/uploads/<nome_arquivo>')
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.errorhandler(404)
def pagina_nao_encontrada(err):
    return render_template('404.html'), 404


@app.errorhandler(401)
def nao_autorizado(err):
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
