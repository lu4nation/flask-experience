from flask import render_template, request, redirect, url_for, abort, session, jsonify, flash, \
    send_from_directory
from functools import wraps
from .models import Jogo, Usuario, deleta_foto, recupera_imagem_jogo, imagem_existe
from .main import app
import os
import time

def protegida(f):
    @wraps(f)
    def valida_usuario(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] is None:
            return redirect(url_for('login', proxima=request.url))
        return f(*args, **kwargs)
    return valida_usuario


@app.route('/')
def index():
    jogos = Jogo.buscar()
    return render_template('index.html', jogos=jogos)


@app.route('/login/')
def login():
    proxima = request.args.buscar_por_id('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuario.buscar_por_id(request.form['usuario'])
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
    jogo_salvo = novo_jogo.salvar()
    message = 'Jogo criado com sucesso!'
    if 'nome_arquivo' in request.files:
        arquivo = request.files['nome_arquivo']
        if arquivo.filename != '':
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            if extensao != 'jpg':
                message = 'Jogo criado , mas formato da foto deve ser jpg.'
            else:
                arquivo.salvar(os.path.join(app.config['UPLOAD_FOLDER'],
                                          'foto{id}-{data}.jpg'.format(id=jogo_salvo.id, data=time.time())))
    flash(message)
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
@protegida
def editar(id):
    categorias = ['RPG', 'Ação', 'FPS', 'Indie', 'Esporte']
    jogo = Jogo.buscar_por_id(id)
    nome_arquivo = recupera_imagem_jogo(id)
    foto = nome_arquivo if imagem_existe(nome_arquivo) else 'capa.jpg'
    return render_template('editar.html', jogo=jogo, categorias=categorias, capa_jogo=foto )


@app.route('/atualizar', methods=['GET', 'POST'])
@protegida
def atualizar():
    jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'], id=request.form['id'])
    jogo.salvar()
    message = 'Jogo atualizado com sucesso!'
    if 'nome_arquivo' in request.files:
        arquivo = request.files['nome_arquivo']
        if arquivo.filename != '':
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            if extensao != 'jpg':
                message = 'Jogo atualizado , mas formato da foto deve ser jpg.'
            else:
                deleta_foto(jogo.id)
                arquivo.salvar(os.path.join(app.config['UPLOAD_FOLDER'],
                                          'foto{id}-{data}.jpg'.format(id=jogo.id, data=time.time())))
    flash(message)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
@protegida
def deletar(id):
    Jogo.deletar(int(id))
    return jsonify(id=id)


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.errorhandler(404)
def pagina_nao_encontrada(err):
    return render_template('404.html'), 404


@app.errorhandler(401)
def nao_autorizado(err):
    return render_template('401.html'), 401

