"""
    Gerenciador de notas RMI
    Desenvolvedores: Brendow e Lucas

    Classe:     Database

    Funcionamento:  Realiza a conexão com o banco de dados
"""

import sqlite3

class Database:

    def connect(self):
        try:
            db = sqlite3.connect('gerenciamento_notas.db')
        except:
            print('Não foi possível conectar ao banco de dados')
        
        return db
