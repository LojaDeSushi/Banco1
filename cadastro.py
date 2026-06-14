import mysql.connector as sql
from mysql.connector import Error
from configs import configAdmin
from configs import Conecta
import crypto

config = configAdmin

#Se já existe um cliente com o nome e telefone:
def BuscaId(nome, tel):
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select id_cliente from cliente where nome_cliente = %s and tel_cliente = %s ")
    cursor.execute(verf, (nome, tel))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

#Busca conta
def BuscaConta(nome, tel):
    resultado = BuscaId(nome, tel)
    if resultado is None:
        return"cliente sem cadastro"
    conex = Conecta(config)
    cursor = conex.cursor()

    verf = "select id_conta from conta where id_conta = %s"
    cursor.execute(verf, (resultado,))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

#Novo cliente: com conta e carrinho 
def NovoCliente(nome, nasc, tel, rua, cidade, bairro, estado):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        resultado = BuscaId(nome, tel)

        if resultado is not None:
            return f"Cliente {nome} já cadastrado"
        
        inser = "insert into cliente (nome_cliente, idade_cliente, tel_cliente, rua, cidade, bairro, estado) values (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(inser, (nome, nasc, tel, rua, cidade, bairro, estado,))
        id_cliente = cursor.lastrowid

        cont = "insert into conta (id_conta) values (%s)"
        cursor.execute(cont, (id_cliente,))
        
        id_conta = id_cliente

        Ncar = "insert into carrinho (id_conta) values (%s)"
        cursor.execute(Ncar, (id_conta,))

        conex.commit()
        return f"Cliente {nome} seja bem vindo!"
    
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#Nova Conta Web:
def NovoWeb(login, senha, nome, tel):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        resultado = BuscaId(nome, tel)
        if resultado is None:
            return "cliente sem cadastro" #verifica se tem cliente
        
        Id_conta = BuscaConta(nome, tel) #pega o id_conta

        verf = ("select id_cliente from clienteweb where id_cliente = %s") #verifica se já existe uma conta web
        cursor.execute(verf, (resultado,))
        resul = cursor.fetchone()

        if resul is not None: #se não tiver web
            return f"Cliente já possui conta web"
        
        status = 'Novo'
        cod = "insert into clienteweb (login, senha, id_cliente, status_web) values (%s, %s, %s, %s);" #cria web
        Vddsenha = crypto.SenHash(senha)
        cursor.execute(cod, (login, Vddsenha, resultado, status))

        conex.commit()
        return "Cliente web cadastrado"
        
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

def BuscaAtende(login): 
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select id_atendente from atendente where login_aten = %s ")
    cursor.execute(verf, (login,))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

def BuscaAdm(login): 
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select id_admin from admin where login_admin = %s")
    cursor.execute(verf, (login,))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

def BuscaWeb(login):
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select id_cliente from clienteweb where login = %s")
    cursor.execute(verf, (login,))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

def login(login, senha):
    conex = Conecta(config)
    cursor = conex.cursor()

    resultado = BuscaAdm(login)
    if resultado is not None:
        cod = "select senha_adm from admin where login_admin = %s"
        cursor.execute(cod, (login,))
        ver = cursor.fetchone()[0]
        vdd = crypto.Confia(senha, ver)
        if vdd == False:
            return "Senha errada"
        
        return 'admin'

    resultado = BuscaAtende(login)
    if resultado is not None:
        cod = "select senha_aten from atendente where login_aten = %s"
        cursor.execute(cod, (login,))
        ver = cursor.fetchone()[0]
        vdd = crypto.Confia(senha, ver)
        if vdd == False:
            return "Senha errada"
    
        return 'atendente'

    resultado = BuscaWeb(login)
    if resultado is not None:
        cod = "select senha from clienteweb where login = %s"
        cursor.execute(cod, (login,))
        ver = cursor.fetchone()[0]
        vdd = crypto.Confia(senha, ver)
        if vdd == False:
            return "Senha errada"
        
        return 'clienteweb'

    else:
        return "login nao encontrado"


