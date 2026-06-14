import mysql.connector as sql
from mysql.connector import Error

configteste = { #define as configurações de conexões
    'host': 'localhost',
    'user': 'root',
    'password': '1324',
    'database': 'banco1',
    'raise_on_warnings': True
}

configAdmin = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'senhaAdmin',
    'database': 'banco1',
    'raise_on_warnings': True
}

configAtendente = {
    'host': 'localhost',
    'user': 'atendente',
    'password': 'senhaAtendente',
    'database': 'banco1',
    'raise_on_warnings': True
}

configClienteweb = {
    'host': 'localhost',
    'user': 'cliente',
    'password': 'senhaCliente',
    'database': 'banco1',
    'raise_on_warnings': True
}


def Conecta(config): #conecta ao banco 
    try: 
        return sql.connect(**config) 
    except Error:
        print(f"Deu erro: {Error}")
        return None