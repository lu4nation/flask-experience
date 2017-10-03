from .main import db as banco_de_dados


class Banco:
    __conn = None;
    __cursor = None;

    def __init__(self):
        self.__conn = banco_de_dados.connection
        self.__cursor = self.__conn.cursor()

    def executar(self, sql, parametros=None):
        if parametros:
            self.__cursor.execute(sql, parametros)
        else:
            self.__cursor.execute(sql)
        return self.__cursor

    def ultimo_id(self):
        return self.__cursor.lastrowid

    def confirmar(self):
        return self.__conn.commit()

    def fechar(self):
        self.__conn.close()