import sqlite3

class Connection(object):

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # imprimindo nome do banco
            # print("Banco:", db_name)
            # # lendo a versão do SQLite
            # self.cursor.execute('SELECT SQLITE_VERSION()')
            # self.data = self.cursor.fetchone()
            # # imprimindo a versão do SQLite
            # print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Erro ao abrir banco.")
            return False

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")