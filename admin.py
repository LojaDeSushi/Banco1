import mysql.connector as sql
from mysql.connector import Error
from configs import configAdmin
from configs import Conecta
import datetime
import crypto

config = configAdmin

#-------------------------ações-------------------------------
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

#criar atendente
def NovoAtendente(login, senha, nome): 
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        resultado = BuscaAtende(login)
        if resultado is not None:
            return "atendente ja cadastrado" 

        cod = "insert into atendente (login_aten, senha_aten, nome_atendente) values (%s, %s, %s);" 
        Vddsenha = crypto.SenHash(senha)
        cursor.execute(cod, (login, Vddsenha, nome,))
        
        conex.commit()
        return "Atendente cadastrado"
        
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#criar adm
def NovoAdm(login, senha): 
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        resultado = BuscaAdm(login)
        if resultado is not None:
            return "adminstrador ja cadastrado" 
        
        cod = "insert into admin (login_admin, senha_adm) values (%s, %s)" 
        Vddsenha = crypto.SenHash(senha)
        cursor.execute(cod, (login, Vddsenha))
        conex.commit()
        return "Administrador cadastrado"
        
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#usa o nome e telefone para achar o id_cliente
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

#Busca Clienteweb
def BuscaClienteWeb(login):
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select id_cliente from clienteweb where login = %s")
    cursor.execute(verf, (login))
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

#Buscar produto e retorna quantidade
def BuscaProd(nome):
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select quanti_pro from produto where nome_produto = %s")
    cursor.execute(verf, (nome,))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

#Add novo produto
def NovoProdu(nome, descricao, valor, quanti):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        resultado = BuscaProd(nome)
        if resultado is not None:
            return f"Produto cadastrado com id de {resultado}"
        else:
            cod = "insert into produto (nome_produto, descricao_pro, valor, quanti_pro) values (%s, %s, %s, %s)"
            cursor.execute(cod, (nome, descricao, valor, quanti,))
        
        conex.commit()
        return f"produto {nome} cadastrado com valor {valor} e {quanti} itens!"
    
    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()
    
#Add item no carrinho
def AddItemCarr(nomeCli, tel, NomePro, quant):
    Id_conta = BuscaConta(nomeCli, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_carrinho from carrinho where id_conta = %s"
        cursor.execute(car, (Id_conta,))
        result = cursor.fetchone()
        Id_car = result[0] if result is not None else None

        Id_prod = BuscaProd(NomePro) 
        if Id_prod is None:
            return "Produto nao encontrado"

        tam = "select quanti_pro from produto where id_produto = %s"
        cursor.execute(tam, (Id_prod,))
        tam = cursor.fetchone()[0]

        verf = "select quanti_item from itemcarrinho where id_produto = %s and id_carrinho = %s"
        cursor.execute(verf, (Id_prod, Id_car))
        resul = cursor.fetchone()
        quantiCar = resul[0] if resul is not None else None

        if quantiCar is None:
            if(tam >= quant):
                add = "insert into itemcarrinho (id_carrinho, id_produto, quanti_item) values (%s, %s, %s)"
                cursor.execute(add, (Id_car, Id_prod, quant,))
                
            else:
                return "Sem estoque! :( "
                
        else:
            if tam >= quant and quantiCar < quant:
                quantiCar += quant
                mais = "update itemcarrinho set quanti_item = %s where id_produto = %s and id_carrinho = %s"
                cursor.execute(mais, (quantiCar, Id_prod, Id_car,))
                
            else:
                return "Não tem mais no estoque :("
                
        conex.commit()
        return f"{NomePro} foi adicionado ao carrinho!"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#visualizar carrinho
def visuCar(nomeCli, tel):
    Id_conta = BuscaConta(nomeCli, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_carrinho from carrinho where id_conta = %s"
        cursor.execute(car, (Id_conta,))
        result = cursor.fetchone()
        Id_car = result[0] if result is not None else None

        if Id_car is None:
            return "Nao possui carrinho"
        
        carr = "select id_produto, quanti_item from itemcarrinho where id_carrinho = %s"
        cursor.execute(carr,(Id_car,))
        result = cursor.fetchall()
    
        carrinho = []
        for itens in result:
            teste = "select nome_produto from produto where id_produto = %s"
            cursor.execute(teste, (itens[0],))
            produt = cursor.fetchone()[0]
            carrinho.append({
                "nome": produt,
                "quantidade":itens[1]
            })

        return carrinho
    
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#transferir do carrinho para o pedido
def Pedido(nome, tel):
    Id_conta = BuscaConta(nome, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_carrinho from carrinho where id_conta = %s"
        cursor.execute(car, (Id_conta,))
        id_carrinho = cursor.fetchone()[0]
        dia = datetime.datetime.now()

        num = "select count(*) from pedido where id_conta = %s"
        cursor.execute(num, (Id_conta,))
        numP = cursor.fetchone()[0] + 1

        cria = "insert into pedido (id_conta, dia_pedido, num_pedido, status) values (%s, %s, %s, %s)"
        cursor.execute(cria, (Id_conta, dia, numP, 'Processos',))
        id_pedido = cursor.lastrowid

        trans = "select id_produto, quanti_item from itemcarrinho where id_carrinho = %s"
        cursor.execute(trans, (id_carrinho,))
        resul = cursor.fetchall()
        if not resul: 
            conex.rollback()
            return "Carrinho vazio"

        total = 0
        for produto in resul:
            coloca = "insert into itempedido (id_pedido, id_produto, quanti_item) values (%s, %s, %s)"
            cursor.execute(coloca, (id_pedido, produto[0], produto[1]))
            preco = "select valor from produto where id_produto = %s"
            cursor.execute(preco, (produto[0],))
            resulta = cursor.fetchone()
            total += resulta[0] * produto[1]
            update = "update produto set quanti_pro = quanti_pro - %s where id_produto = %s"
            cursor.execute(update, (produto[1], produto[0],))

        finalP = []
        valor = "update pedido set total_pedido = %s, status = %s where id_pedido = %s"
        cursor.execute(valor, (total, "Confirmado",id_pedido,))

        dell = "delete from itemcarrinho where id_carrinho = %s"
        cursor.execute(dell, (id_carrinho,))
        finalP.append(numP)
        finalP.append(total)

        conex.commit()

        return finalP
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}\n"
    finally:
        cursor.close()
        conex.close()

#visualizar carrinho
def visuPedi(nomeCli, tel):
    Id_conta = BuscaConta(nomeCli, tel)
    if Id_conta is None:
        return "cliente nao encontrado"
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_pedido, total_pedido, status, num_pedido from pedido where id_conta = %s"
        cursor.execute(car, (Id_conta,))
        result = cursor.fetchall()
        if not result:
            return "Nenhum pedido"
        
        pedidoCompleto = []

        for pedido in result:
            ped = "select id_produto, quanti_item from itempedido where id_pedido = %s"
            cursor.execute(ped,(pedido[0],))
            itens = cursor.fetchall()

            produtos = []
            for item in itens:
                teste = "select nome_produto from produto where id_produto = %s"
                cursor.execute(teste, (item[0],))
                nomeProd = cursor.fetchone()[0]
                produtos.append(f"{nomeProd} x{item[1]} ")

            pag = "select metodo_pag, valor_pag from pagamento where id_pedido = %s"
            cursor.execute(pag, (pedido[0],))
            tipos = cursor.fetchall()

            pedidoCompleto.append({
                "id": pedido[0],
                "total": pedido[1],
                "status": pedido[2],
                "num_pedido": pedido[3],
                "produtos": ", ".join(produtos),
                "pagamento": tipos[0][0] if tipos else "Sem pagamento"
            })
            
        return pedidoCompleto
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#cancelar pedido admn
def Cancela(id_pedido):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        ped = "select status from pedido where id_pedido = %s"
        cursor.execute(ped, (id_pedido,))
        result = cursor.fetchone()[0]
        if not result:
            return "pedido nao existe"
        elif result == 'Entregue' or result == 'Cancelado':
            return "Pedido entregue ou cancelado"

        ped = "select id_produto, quanti_item from itempedido where id_pedido = %s"
        cursor.execute(ped,(id_pedido,))
        resultado = cursor.fetchall()

        if result in ['Confirmado', 'Pago', 'Em transito']:
            for itens in resultado:
                muda = "update produto set quanti_pro = quanti_pro + %s where id_produto = %s"
                cursor.execute(muda, (itens[1], itens[0]))
            
        up = "update pedido set status = 'Cancelado' where id_pedido = %s"
        cursor.execute(up, (id_pedido,))
        
        conex.commit()
        return f"Pedido de id {id_pedido} foi cancelado"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#Muda status
def MudaStatus(id_pedido):
    ordem = {
    'Processos': 'Confirmado',
    'Confirmado': 'Pago',
    'Pago': 'Em transito',
    'Em transito': 'Entregue'
    }
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        ped = "select status from pedido where id_pedido = %s"
        cursor.execute(ped, (id_pedido,))
        result = cursor.fetchone()[0]
        if not result:
            return "pedido nao existe"
        elif result == 'Entregue' or result == 'Cancelado':
            return "Pedido entregue ou cancelado"
        
        prox = ordem[result]
        atua = "update pedido set status = %s where id_pedido = %s"
        cursor.execute(atua, (prox, id_pedido,))
        if prox == 'Confirmado':
            ped = "select id_produto, quanti_item from itempedido where id_pedido = %s"
            cursor.execute(ped,(id_pedido,))
            resultado = cursor.fetchall()
            for itens in resultado:
                retira = "update produto set quanti_pro = quanti_pro - %s where id_produto = %s"
                cursor.execute(retira, (itens[1], itens[0],))

        conex.commit()
        return f"pedido de id {id_pedido} foi atualizado para {prox}"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#pagamentos
def Pagamento(nome, tel, numP, pag):
    Id_conta = BuscaConta(nome, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_pedido, total_pedido, status from pedido where id_conta = %s and num_pedido = %s"
        cursor.execute(car, (Id_conta, numP))
        result = cursor.fetchone()

        if not result:
            return "Nenhum pedido achado\n"
        if result[2] in ['Cancelado', 'Entregue']:
            return "Não pode mais alterar o pagamento"
        
        totalPag = sum(t['valor'] for t in pag)
        if totalPag != result[1]:
            return f"Total pago diferente do total pedido R${result[1]}"
        
        diaP = datetime.datetime.now()
        for t in pag:
            pagamento = "insert into pagamento (id_pedido, metodo_pag, valor_pag, data_pag) values (%s, %s, %s, %s)"
            cursor.execute(pagamento, (result[0], t['metodo'], t['valor'], diaP,))

        status = "update pedido set status = %s where id_pedido = %s"
        cursor.execute(status, ("Pago", result[0],))

        conex.commit()
        return "Pagamento feito com sucesso"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}\n"
    finally:
        cursor.close()
        conex.close()

#remover item do carrinho
def RemoveItemCar(nome, tel, NomeP, quant):
    id_conta = BuscaConta(nome, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_carrinho from carrinho where id_conta = %s"
        cursor.execute(car, (id_conta,))
        id_car = cursor.fetchone()
        if not id_car:
            return "Carrinho vazio"
        id_car = id_car[0]

        id_prod = BuscaProd(NomeP)
        if id_prod is None:
            return "Produto nao encontrado"

        it = "select quanti_item from itemcarrinho where id_produto = %s and id_carrinho = %s"
        cursor.execute(it, (id_prod, id_car,))
        quantidade = cursor.fetchone()
        if quantidade is None:
            return f"Nao tem {NomeP} no carrinho"
        quantidade = quantidade[0]
        
        if quant >= quantidade:
            remove = "delete from itemcarrinho where id_produto = %s and id_carrinho = %s"
            cursor.execute(remove, (id_prod, id_car,))
        elif quant < quantidade:
            atua = "update itemcarrinho set quanti_item = quanti_item - %s where id_produto = %s and id_carrinho = %s"
            cursor.execute(atua, (quant, id_prod, id_car,))

        conex.commit()
        return f"{NomeP}"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#atualizar cliente
def atualizaCliente(nome, tel, Ntel=None, Nrua=None, Ncidade=None, Nbairro=None, Nestado=None):
    id_cliente = BuscaId(nome, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        campos = []
        valores = []

        if Ntel is not None:
            campos.append("tel_cliente = %s")
            valores.append(Ntel)
        if Nrua is not None:
            campos.append("rua = %s")
            valores.append(Nrua)
        if Ncidade is not None:
            campos.append("cidade = %s")
            valores.append(Ncidade)
        if Nbairro is not None:
            campos.append("bairro = %s")
            valores.append(Nbairro)
        if Nestado is not None:
            campos.append("estado = %s")
            valores.append(Nestado)

        if not campos:
            return "Nenhuma alteração feita"

        valores.append(id_cliente)
        atua = f"update cliente set {', '.join(campos)} where id_cliente = %s"
        cursor.execute(atua, tuple(valores))

        conex.commit()
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()
    
#atualiza produto
def atualizaProd(nomeP, Nnome=None, Ndescricao=None, Nvalor=None, Nquanti=None):
    id_produto = BuscaProd(nomeP)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        campos = []
        valores = []

        if Nnome is not None:
            campos.append("nome_produto = %s")
            valores.append(Nnome)
        if Ndescricao is not None:
            campos.append("descricao_pro = %s")
            valores.append(Ndescricao)
        if Nvalor is not None:
            campos.append("valor = %s")
            valores.append(Nvalor)
        if Nquanti is not None:
            campos.append("quanti_pro = %s")
            valores.append(Nquanti)

        if not campos:
            return "Nenhuma alteração feita"

        valores.append(id_produto)
        atua = f"update produto set {', '.join(campos)} where id_produto = %s"
        cursor.execute(atua, tuple(valores))

        conex.commit()
        return f"Produto {nomeP} atualizado, veja no campo de visualizar produtos"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#deletar cliente
def mataCliente(nome, tel):
    id_cliente = BuscaId(nome, tel)
    conex = Conecta(config)
    try:
        cursor= conex.cursor()
        if id_cliente is None:
            return "Esse cliente não existe"
        
        mata = "Delete from cliente where id_cliente = %s"
        cursor.execute(mata, (id_cliente,))
    
        conex.commit()
        return f"o cliente {nome} de id = {id_cliente} foi retirado do sistema"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()
    
#deleta produto
def mataProduto(nomeP):
    id_prod = BuscaProd(nomeP)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        if id_prod is None:
            return "Esse produto não existe"
        
        deleta = "Delete from produto where id_produto = %s"
        cursor.execute(deleta, (id_prod,))
        conex.commit()
        return f"O produto {nomeP} e id = {id_prod} foi retirado do sistema"

    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#deletar atendente
def mataAtendente(nome, login):
    id_atendente = BuscaAtende(login)
    conex = Conecta(config)
    try:
        cursor= conex.cursor()
        if id_atendente is None:
            return "Esse atendente não existe"
        
        mata = "Delete from atendente where id_atendente = %s and nome_atendente = %s"
        cursor.execute(mata, (id_atendente,))
    
        conex.commit()
        return f"o atendente {nome} de id = {id_atendente} foi retirado do sistema"
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#---------------------consultas ao banco de dados-------------------------------
#quantidade de usuários, id nome e cidade
def Usuarios():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        quant = "select count(*) from cliente"
        cursor.execute(quant)
        quantidade = cursor.fetchone()[0]

        usu = "select * from cliente"
        cursor.execute(usu)
        result = cursor.fetchall()
        return result

    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#quantidade de produtos 
def Produtos():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        quant = "select count(*) from produto"
        cursor.execute(quant)
        quantidade = cursor.fetchone()[0]
        
        usu = "select * from produto"
        cursor.execute(usu)
        result = cursor.fetchall()
        return result

    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#quantidade de atendentes
def Atendentes():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        quant = "select count(*) from atendente"
        cursor.execute(quant)
        quantidade = cursor.fetchone()[0]
    
        usu = "select * from atendente"
        cursor.execute(usu)
        result = cursor.fetchall()

        atend = []
        for atendente in result:
            id_atend = atendente[0]
            nome_atend = atendente[1]

            ped = "select id_pedido from pedido where atendente = %s"
            cursor.execute(ped, (id_atend,))
            pedidos = cursor.fetchall()

            atend.append({
                "id": id_atend,
                "nome": nome_atend,
                "pedidos": [p[0] for p in pedidos]
            })

        return atend

    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#quantidade de pedidos 
def Pedidos():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        quant = "select count(*) from pedido"
        cursor.execute(quant)
        quantidade = cursor.fetchone()[0]
        
        usu = "select * from pedido"
        cursor.execute(usu)
        result = cursor.fetchall()

        pedidoCompleto = []

        for pedido in result:
            ped = "select id_produto, quanti_item from itempedido where id_pedido = %s"
            cursor.execute(ped,(pedido[0],))
            itens = cursor.fetchall()

            produtos = []
            for item in itens:
                teste = "select nome_produto from produto where id_produto = %s"
                cursor.execute(teste, (item[0],))
                nomeProd = cursor.fetchone()[0]
                produtos.append(f"{nomeProd} x{item[1]} ")

            pag = "select metodo_pag, valor_pag from pagamento where id_pedido = %s"
            cursor.execute(pag, (pedido[0],))
            tipos = cursor.fetchall()

            pedidoCompleto.append({
                "id": pedido[0],
                "total": pedido[5],
                "status": pedido[4],
                "num_pedido": pedido[3],
                "produtos": ", ".join(produtos),
                "pagamento": tipos[0][0] if tipos else "N tem",
                "quant_pedidos": quantidade
            })

        return pedidoCompleto

    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#pagamento mais usado 
#visão
def PagamentoMais():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        cursor.execute("select * from MetodoMais")
        dados = cursor.fetchall()
        if not dados:
            return "Nenhum pagamento feito"
        return dados

    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#Filtro de usuários por bairro, cidade, estado
def FiltraLocal(Bairro=None, Cidade=None, Estado=None):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        campos = []
        valores = []

        if Bairro is not None:
            campos.append("bairro = %s")
            valores.append(Bairro)
        if Cidade is not None:
            campos.append("cidade = %s")
            valores.append(Cidade)
        if Estado is not None:
            campos.append("estado = %s")
            valores.append(Estado)
        if not campos:
            Usuarios()
            return
        
        usu = f"select * from cliente where {' and '.join(campos)}"
        cursor.execute(usu, tuple(valores))
        result = cursor.fetchall()
        if result is None:
            return "Nenhum cliente encontrado"
        return result


    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#Média anual de venda (por valor)
#visão
def MediAnual():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        cursor.execute("select * from MediaPedidosAno")
        dados = cursor.fetchall()
        if not dados:
            return None
    
        return dados
    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()
    
#Mes e ano com maior num de vendas
#visão
def M_A_Vendas():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        cursor.execute("select * from MaiorVendasM_A order by total desc limit 1")
        dados = cursor.fetchone()
        if not dados:
            return None
        return dados

    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#clientes com compras todos os meses de um ano x
#procedure
def ClienteAnual(ano):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        cursor.execute("call ClienteAnual(%s)", (ano,))
        dados = cursor.fetchall()
        if not dados:
            return None
        
        for i in dados:
            cli = "select nome_cliente from cliente where id_cliente = %s"
            cursor.execute(cli, (i[0],))
            nome = cursor.fetchone()
            return nome

    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#Produto mais vendido CONSULTA EXTRA
#visão
def ProdutoMais():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        cursor.execute("select * from ProdutoMais")
        dados = cursor.fetchall()
        if not dados:
            return None
        return dados
    except Error as e:
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()
