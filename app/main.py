# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')
# é necessário um secret_key para que a sessão da aplicação não fique acessível para qualquer um
app.config['SECRET_KEY'] = '*#caleum&*'


class Jogo():
    def __init__(self, id, nome, categoria, console):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario():
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


fifa18 = Jogo(1, 'Fifa 18', 'Esporte', 'PS4')
gow4= Jogo(2, 'Gear of War 4', 'Ação', 'Xbox One')
titanfall = Jogo(3, 'Titan Fall 2', 'Ação', 'Xbox One')
rayman = Jogo(4, 'Rayman Legends', 'Indie', 'PS4')

admin = Usuario(id='luan', nome='Luan Marques', senha='trocarsenha')

# dicionario de usuarios para consulta por id
usuarios = {admin.id: admin,}

jogos = [fifa18,gow4,titanfall,rayman]
categorias= ['RPG', 'Ação', 'FPS', 'Indie', 'Esporte']


@app.route('/')
def index():
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
    if session.get('usuario_logado'):
        return render_template('novo.html', categorias=categorias)
    else:
        return render_template('login.html', next=url_for('novo'))


@app.route('/criar', methods=['GET','POST'])
def criar():
    if session['usuario_logado']:
        novo_jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'])
        jogos.append(novo_jogo)
        return index()
    else:
        return render_template('login.html', next=request.url)


@app.route('/deletar/<int:id>')
def deletar(id):
    """ Remove um jogo da lista """
    for jogo in jogos:
        if jogo.id == id:
            jogo_removido = jogo
            break

    if jogo_removido:
        jogos.remove(jogo_removido)

    return jsonify(id=id)


@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def nao_autorizado(e):
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
