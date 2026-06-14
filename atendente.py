import mysql.connector as sql
from mysql.connector import Error
from configs import configAtendente
from configs import Conecta
import datetime


config = configAtendente

#---------------------------------------------
#busca id_atendente
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

def BuscaProd(nome):
    conex = Conecta(config)
    cursor = conex.cursor()
    verf = ("select id_produto from produto where nome_produto = %s")
    cursor.execute(verf, (nome,))
    resul = cursor.fetchone()
    cursor.close()
    conex.close()
    if resul is None:
        return None
    return resul[0]

def AddItemCarr(nomeCli, tel, NomePro, quant):
    Id_conta = BuscaConta(nomeCli, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        car = "select id_carrinho from carrinho where id_conta = %s"
        cursor.execute(car, (Id_conta,))
        result = cursor.fetchone()
        Id_car = result[0] if result is not None else None

        print(f"DEBUG: Id_conta={Id_conta}, Id_car={Id_car}")

        Id_prod = BuscaProd(NomePro) 
        if Id_prod is None:
            return "Produto nao encontrado"
        
        print(f"DEBUG: Id_prod={Id_prod}")

        tam = "select quanti_pro from produto where id_produto = %s"
        cursor.execute(tam, (Id_prod,))
        estoque = cursor.fetchone()[0]

        verf = "select quanti_item from itemcarrinho where id_produto = %s and id_carrinho = %s"
        cursor.execute(verf, (Id_prod, Id_car))
        resul = cursor.fetchone()
        tem = resul[0] if resul is not None else None

        print(f"DEBUG: estoque={estoque}, tem={tem}")

        if tem is None:
            if(estoque >= quant):
                add = "insert into itemcarrinho (id_carrinho, id_produto, quanti_item) values (%s, %s, %s)"
                cursor.execute(add, (Id_car, Id_prod, quant,))
    
            else:
                add = "insert into itemcarrinho (id_carrinho, id_produto, quanti_item) values (%s, %s, %s)"
                cursor.execute(add, (Id_car, Id_prod, estoque,))
        else:
            if estoque >= quant:
                tem += quant
                mais = "update itemcarrinho set quanti_item = %s where id_produto = %s and id_carrinho = %s"
                cursor.execute(mais, (tem, Id_prod, Id_car,))
            else:
                mais = "update itemcarrinho set quanti_item = %s where id_produto = %s and id_carrinho = %s"
                cursor.execute(mais, (estoque, Id_prod, Id_car,))

        conex.commit()
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
def Pedido(nome, tel, id_atendente):
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

        cria = "insert into pedido (id_conta, dia_pedido, num_pedido, status, atendente) values (%s, %s, %s, %s, %s)"
        cursor.execute(cria, (Id_conta, dia, numP, 'Processos', id_atendente))
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
        #print("Pedido criado\n")
        #print(f"O total deu {total} reais\n")

        dell = "delete from itemcarrinho where id_carrinho = %s"
        cursor.execute(dell, (id_carrinho,))
        finalP.append(numP)
        finalP.append(total)

        #print("Carrinho esvaziado\n")
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
                "pagamento": ", ".join(t[0] for t in tipos) if tipos else "Sem pagamento"
            })
            
        return pedidoCompleto
    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()

#cancelar pedido admim e cliente
def Cancela(nome, tel, numP):
    id_conta = BuscaConta(nome, tel)
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        ped = "select id_pedido, status from pedido where id_conta = %s and num_pedido = %s"
        cursor.execute(ped, (id_conta, numP,))
        result = cursor.fetchone()
        if not result:
            return "pedido nao existe"
        elif result[1] == 'Entregue' or result[1] == 'Cancelado':
            return "Pedido entregue ou cancelado"

        ped = "select id_produto, quanti_item from itempedido where id_pedido = %s"
        cursor.execute(ped,(result[0],))
        resultado = cursor.fetchall()

        for itens in resultado:
            muda = "update produto set quanti_pro = quanti_pro + %s where id_produto = %s"
            cursor.execute(muda, (itens[1], itens[0]))
            
        up = "update pedido set status = 'Cancelado' where id_pedido = %s"
        cursor.execute(up, (result[0],))
        
        conex.commit()
        return f"Pedido de numero {numP} foi cancelado"
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
        return f"Removeu 1x de {NomeP} do carrinho"
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

def Produtos():
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        quant = "select count(*) from produto"
        cursor.execute(quant)
        quantidade = cursor.fetchone()[0]
        #print(f"Seu sistema tem {quantidade} produtos:")
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

def Pedidos(id_atendente):
    conex = Conecta(config)
    try:
        cursor = conex.cursor()
        quant = "select count(*) from pedido"
        cursor.execute(quant)
        quantidade = cursor.fetchone()[0]
        #print(f"Seu sistema tem {quantidade} pedidos:")
        usu = "select * from pedido where atendente = %s"
        cursor.execute(usu, (id_atendente,))
        result = cursor.fetchall()
        return result

    except Error as e:
        conex.rollback()
        return f"ihh erro {e}"
    finally:
        cursor.close()
        conex.close()