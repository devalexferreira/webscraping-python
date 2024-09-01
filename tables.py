import sqlite3
from datetime import date
from os import path

class Tables():

    def verificarUsuarios():
       conn = sqlite3.connect('systemet.db')
       cursor = conn.cursor()
       atual = f"{date.today()}"
       cursor.execute('SELECT * from login where excluido = ? ', ('',))
       registro = cursor.fetchall()
       if len(registro) < 1:
           cursor.execute("""
           INSERT INTO login (descricao, senha, nivel, data, excluido, idcriador)
           VALUES ('salao', '102030', '9', ?, '', '0')
           """, (atual,))
           conn.commit()
       conn.close()

    def createTableLogin():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS login (
                idoperador INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                descricao VARCHAR(255),
                senha VARCHAR(255),
                nivel VARCHAR(1),
                data DATE,
                excluido VARCHAR(1),
                idcriador INTEGER
                );
        """)
        print("tabela criada")
        conn.close() 


    def createTableUltima():
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS busca (
                idbusca INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                descricao VARCHAR(255),
                codigo VARCHAR(255)
                );
        """)
        print("tabela criada")
        conn.close()  


    def createTableSmtp():
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS smtp (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                host VARCHAR(255),
                porta VARCHAR(10),
                email VARCHAR(255),
                senha VARCHAR(255)
                );
        """)
        print("tabela criada")
        conn.close()


    def createTableServico():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS servico (
                idagenda INTEGER,
                porcentagem INTEGER,
                descricao VARCHAR(255),
                valor DECIMAL(10,2)
                );
        """)
        print("tabela criada")
        conn.close()


    def createTableDespesa():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesa (
                iddespesa INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                idprofissional INTEGER,
                descricao VARCHAR(255),
                valor DECIMAL(10,2),
                data DATE
                );
        """)
        print("tabela criada")
        conn.close()


    def updateDespesa():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        ALTER TABLE despesa ADD COLUMN observacao VARCHAR(255);
        """)
        print("tabela criada")
        conn.close()


    def createTableProduto():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produto (
                idproduto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                
                descricao VARCHAR(255),
                valor DECIMAL(10,2),
                porcentagem INTEGER,
                venda DECIMAL(10,2),
                excluido VARCHAR(1)
                );
        """)
        print("tabela criada")
        conn.close()


    def createTableEstoque():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
                idproduto INTEGER,                
                movimento VARCHAR(1),
                qtd INTEGER
                );
        """)
        print("tabela criada")
        conn.close()


    def createTableVenda():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS venda (
                idvenda INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                
                data DATE
                );
        """)
        print("tabela criada")
        conn.close()


    def createTableItems():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
                idvenda INTEGER,  
                idproduto INTEGER, 
                qtd INTEGER,  
                valor DECIMAL(10,2)
                );
        """)
        print("tabela criada")
        conn.close()


    def createTableCliente():
        conn = sqlite3.connect('systemet.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
                idcliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                
                nome VARCHAR(255),
                telefone VARCHAR(50),
                nascimento VARCHAR(20),
                rua VARCHAR(255),
                numero VARCHAR(10),
                cep VARCHAR(20),
                bairro VARCHAR(255),
                cidade VARCHAR(255),
                estado VARCHAR(255),
                data Date,
                excluido VARCHAR(1)
                );
        """)
        print("tabela cliente criada")
        conn.close()


    def createTableValidar():
        main_folder = path.join(path.expanduser("~"), "AppData/Local/Salao/salao.db")
        conn = sqlite3.connect(main_folder)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS instalacao (
                idinstalacao VARCHAR(255),  
                licenca VARCHAR(255),
                data DATE
                );
        """)
        print("tabela criada instalacao")
        conn.close()
