from .banco import Banco
import os
from app.main import app

SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'


class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console

    def salvar(self):
        bd = Banco()
        if self.id:
            bd.executar(SQL_ATUALIZA_JOGO, (self.nome, self.categoria, self.console, self.id))
        else:
            bd.executar(SQL_CRIA_JOGO, (self.nome, self.categoria, self.console))
            self.id = bd.ultimo_id()
        bd.confirmar()
        return self

    @staticmethod
    def buscar():
        bd = Banco()
        jogos = Jogo.traduz_jogos(bd.executar(SQL_BUSCA_JOGOS).fetchall())
        return jogos

    @staticmethod
    def buscar_por_id(id):
        bd = Banco()
        jogo = Jogo.traduz_jogos((bd.executar(SQL_JOGO_POR_ID, (id,)).fetchone(),))[0]
        return jogo

    @staticmethod
    def traduz_jogos(jogos):
        def cria_jogo_com_tupla(tupla):
            return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

        return list(map(cria_jogo_com_tupla, jogos))

    @staticmethod
    def deletar(id):
        bd = Banco()
        bd.executar(SQL_DELETA_JOGO, (id,))
        bd.confirmar()
        deleta_foto(id)


def imagem_existe(arquivo):
    return arquivo in os.listdir(app.config['UPLOAD_FOLDER'])


def recupera_imagem_jogo(jogo_id):
    foto = 'foto{id}-'.format(id=jogo_id)
    pasta = os.listdir(app.config['UPLOAD_FOLDER'])
    for arquivo in pasta:
        if foto in arquivo:
            return arquivo


def deleta_foto(jogo_id):
    arquivo = recupera_imagem_jogo(jogo_id)
    if imagem_existe(arquivo):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], arquivo))


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

    @staticmethod
    def traduz_usuario(tupla):
        return Usuario(tupla[0], tupla[1], tupla[2])

    @staticmethod
    def buscar_por_id(id):
        bd = Banco()
        dados = bd.executar(SQL_USUARIO_POR_ID, (id,)).fetchone()
        usuario = Usuario.traduz_usuario(dados) if dados else None
        return usuario

