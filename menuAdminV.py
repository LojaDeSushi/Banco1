import customtkinter as ck
import admin as ad

class MenuAdmin(ck.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu Adminstrador")

        self.msgLabel = ck.CTkLabel(self, text="")
        self.msgLabel.pack(padx=10, pady=10)

        self.abas = ck.CTkTabview(self)
        self.abas.pack(padx=20, pady=20)

        self.msgLabel.configure(text="Bem vindo!")

        self.abas.add("Clientes")
        self.abas.add("Produtos")
        self.abas.add("Pedidos")
        self.abas.add("Consultas")
        self.abas.add("Atendentes")

        #parte clientes
        abaCli=self.abas.tab("Clientes")
        botaoNC =ck.CTkButton(abaCli, text="Novo Cliente", command=self.novoCliente)
        botaoNC.pack(padx=10, pady=10)

        botaoAC =ck.CTkButton(abaCli, text="Atualiza Cliente", command=self.AtualizaCliente)
        botaoAC.pack(padx=10, pady=10)

        botaoDC =ck.CTkButton(abaCli, text="Deleta Cliente", command=self.DeletaCliente)
        botaoDC.pack(padx=10, pady=10)

        botaoVC =ck.CTkButton(abaCli, text="Clientes", command=self.VisuClientes)
        botaoVC.pack(padx=10, pady=10)

        botaoFiltro =ck.CTkButton(abaCli, text="Filtrar clientes", command=self.FiltraCliente)
        botaoFiltro.pack(padx=10, pady=10)

        #parte produtos
        abaProduto=self.abas.tab("Produtos")
        botaoNP =ck.CTkButton(abaProduto, text="Novo Produto", command=self.NovoProdu)
        botaoNP.pack(padx=10, pady=10)

        botaoAP =ck.CTkButton(abaProduto, text="Atualiza Produto", command=self.AtualizaProdu)
        botaoAP.pack(padx=10, pady=10)

        botaoDP =ck.CTkButton(abaProduto, text="Deleta Produto", command=self.DeletaProdu)
        botaoDP.pack(padx=10, pady=10)

        botaoVP =ck.CTkButton(abaProduto, text="Produto", command=self.VisuProdutos)
        botaoVP.pack(padx=10, pady=10)


        #parte pedidos
        abaPedido=self.abas.tab("Pedidos")
        botaoVP =ck.CTkButton(abaPedido, text="Visualizar Pedidos", command=self.VisuPedidos)
        botaoVP.pack(padx=10, pady=10)

        botaoVPC =ck.CTkButton(abaPedido, text="Visualizar Pedido Cliente", command=self.PedidoCli)
        botaoVPC.pack(padx=10, pady=10)

        botaoMS =ck.CTkButton(abaPedido, text="Mudar Status", command=self.MudarStatus)
        botaoMS.pack(padx=10, pady=10)

        botaoCP =ck.CTkButton(abaPedido, text="Cancela Pedido", command=self.CancelaPedido)
        botaoCP.pack(padx=10, pady=10)

        #parte consultas
        abaConsul=self.abas.tab("Consultas")

        botaoPagM =ck.CTkButton(abaConsul, text="Pag Mais", command=self.MaisPaga)
        botaoPagM.pack(padx=10, pady=10)

        botaoMediaPe =ck.CTkButton(abaConsul, text="Media Pedidos", command=self.MediaValor)
        botaoMediaPe.pack(padx=10, pady=10)

        botaoMaioV_MA =ck.CTkButton(abaConsul, text="Maior mes e ano", command=self.MaiorVenda)
        botaoMaioV_MA.pack(padx=10, pady=10)

        botaoClienAnual =ck.CTkButton(abaConsul, text="Cliente anual", command=self.ClienteAnual)
        botaoClienAnual.pack(padx=10, pady=10)

        botaoProdutoMais =ck.CTkButton(abaConsul, text="Produto mais", command=self.ProdutoMais)
        botaoProdutoMais.pack(padx=10, pady=10)


        #parte atendentes
        abaAten=self.abas.tab("Atendentes")
        botaoNA =ck.CTkButton(abaAten, text="Novo Atendente")
        botaoNA.pack(padx=10, pady=10)

        botaoDA =ck.CTkButton(abaAten, text="Deleta Atendente")
        botaoDA.pack(padx=10, pady=10)

        botaoVA =ck.CTkButton(abaAten, text="Visualiza Atendente")
        botaoVA.pack(padx=10, pady=10)

#botoes cliente
    def novoCliente(self):
        janela = ck.CTkToplevel(self)
        janela.title("Novo Cliente")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.NascEntry = ck.CTkEntry(janela, placeholder_text="AAAA-MM-DD")
        janela.NascEntry.pack(padx=10, pady=10)

        janela.TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        janela.TelEntry.pack(padx=20, pady=10)

        janela.RuaEntry = ck.CTkEntry(janela, placeholder_text="Coloque sua rua")
        janela.RuaEntry.pack(padx=10, pady=10)

        janela.BairroEntry = ck.CTkEntry(janela, placeholder_text="Coloque deu bairro")
        janela.BairroEntry.pack(padx=20, pady=10)

        janela.CidadeEntry = ck.CTkEntry(janela, placeholder_text="Coloque sua cidade")
        janela.CidadeEntry.pack(padx=10, pady=10)

        janela.EstadoEntry = ck.CTkEntry(janela, placeholder_text="Coloque seu estado")
        janela.EstadoEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Nasc = janela.NascEntry.get()
            Tel = janela.TelEntry.get()
            Rua = janela.RuaEntry.get()
            Bairro = janela.BairroEntry.get()
            Cidade = janela.CidadeEntry.get()
            Estado = janela.EstadoEntry.get()

            novo = ad.NovoCliente(Nome, Nasc, Tel, Rua, Cidade, Bairro, Estado)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma, fg_color="purple")
        botaoConf.pack(padx=10, pady=10)

    def AtualizaCliente(self):
        janela = ck.CTkToplevel(self)
        janela.title("Atualiza Cliente")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        janela.TelEntry.pack(padx=20, pady=10)

        janela.Tel2Entry = ck.CTkEntry(janela, placeholder_text="Coloque novo telefone")
        janela.Tel2Entry.pack(padx=20, pady=10)

        janela.RuaEntry = ck.CTkEntry(janela, placeholder_text="Coloque nova rua")
        janela.RuaEntry.pack(padx=10, pady=10)

        janela.BairroEntry = ck.CTkEntry(janela, placeholder_text="Coloque novo bairro")
        janela.BairroEntry.pack(padx=20, pady=10)

        janela.CidadeEntry = ck.CTkEntry(janela, placeholder_text="Coloque nova cidade")
        janela.CidadeEntry.pack(padx=10, pady=10)

        janela.EstadoEntry = ck.CTkEntry(janela, placeholder_text="Coloque novo estado")
        janela.EstadoEntry.pack(padx=20, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Tel = janela.TelEntry.get()
            Rua = janela.RuaEntry.get() or None
            Bairro = janela.BairroEntry.get() or None
            Cidade = janela.CidadeEntry.get() or None
            Estado = janela.EstadoEntry.get() or None
            Tel2 = janela.Tel2Entry.get() or None

            novo = ad.atualizaCliente(Nome, Tel, Ntel=Tel2, Nrua= Rua, Ncidade=Cidade, Nbairro=Bairro, Nestado=Estado)
            janela.destroy()

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def DeletaCliente(self):
        janela = ck.CTkToplevel(self)
        janela.title("Deleta Cliente")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        janela.TelEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Tel = janela.TelEntry.get()

            novo = ad.mataCliente(Nome, Tel)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def VisuClientes(self):
        janela = ck.CTkToplevel(self)
        janela.title("Clientes")

        frame = ck.CTkScrollableFrame(janela)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        clientes = ad.Usuarios()
        for cliente in clientes:
            printa =ck.CTkLabel(frame, text=f"ID: {cliente[0]} | Nome: {cliente[1]} | Tel: {cliente[3]} | Cidade: {cliente[5]} | Estado: {cliente[7]}")
            printa.pack(padx=10, pady=10)

    def FiltraCliente(self):
        janela = ck.CTkToplevel(self)
        janela.title("Filtra Cliente")

        janela.BairroEntry = ck.CTkEntry(janela, placeholder_text="Coloque bairro")
        janela.BairroEntry.pack(padx=20, pady=10)

        janela.CidadeEntry = ck.CTkEntry(janela, placeholder_text="Coloque cidade")
        janela.CidadeEntry.pack(padx=10, pady=10)

        janela.EstadoEntry = ck.CTkEntry(janela, placeholder_text="Coloque estado")
        janela.EstadoEntry.pack(padx=20, pady=10)

        def confirma():

            Bairro = janela.BairroEntry.get() or None
            Cidade = janela.CidadeEntry.get() or None
            Estado = janela.EstadoEntry.get() or None

            novo = ad.FiltraLocal(Bairro=Bairro, Cidade=Cidade, Estado=Estado)
            frame = ck.CTkScrollableFrame(janela)
            frame.pack(padx=10, pady=10, fill="both", expand=True)
            for cliente in novo:
                printa =ck.CTkLabel(frame, text=f"ID: {cliente[0]} | Nome: {cliente[1]}")
                printa.pack(padx=10, pady=10)
    

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

#botoes produtos
    def NovoProdu(self):

        janela = ck.CTkToplevel(self)
        janela.title("Novo Produto")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.DescEntry = ck.CTkEntry(janela, placeholder_text="Coloque a descricao")
        janela.DescEntry.pack(padx=20, pady=10)

        janela.ValorEntry = ck.CTkEntry(janela, placeholder_text="Coloque o valor")
        janela.ValorEntry.pack(padx=10, pady=10)

        janela.QuantiEntry = ck.CTkEntry(janela, placeholder_text="Coloque a quantidade")
        janela.QuantiEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Desc = janela.DescEntry.get()
            Valor = janela.ValorEntry.get()
            Quanti = janela.QuantiEntry.get()

            novo = ad.NovoProdu(Nome, Desc, Valor, Quanti)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def AtualizaProdu(self):
        janela = ck.CTkToplevel(self)
        janela.title("Atualiza Produto")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.DescEntry = ck.CTkEntry(janela, placeholder_text="Coloque a nova descricao")
        janela.DescEntry.pack(padx=20, pady=10)

        janela.ValorEntry = ck.CTkEntry(janela, placeholder_text="Coloque o novo valor")
        janela.ValorEntry.pack(padx=10, pady=10)

        janela.QuantiEntry = ck.CTkEntry(janela, placeholder_text="Coloque a nova quantidade")
        janela.QuantiEntry.pack(padx=20, pady=10)

        janela.Nome2Entry = ck.CTkEntry(janela, placeholder_text="Coloque o novo nome")
        janela.Nome2Entry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)
        

        def confirma():

            Nome = janela.NomeEntry.get()
            Desc = janela.DescEntry.get() or None
            Valor = janela.ValorEntry.get() or None
            Quanti = janela.QuantiEntry.get() or None
            Nome2 = janela.Nome2Entry.get() or None

            novo = ad.atualizaProd(Nome, Nnome=Nome2, Ndescricao=Desc, Nvalor=Valor, Nquanti=Quanti)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def DeletaProdu(self):
        janela = ck.CTkToplevel(self)
        janela.title("Deleta Produto")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()

            novo = ad.mataProduto(Nome)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def VisuProdutos(self):
        janela = ck.CTkToplevel(self)
        janela.title("Produtos")

        frame = ck.CTkScrollableFrame(janela)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        produtos = ad.Produtos()
        for produto in produtos:
            printa =ck.CTkLabel(frame, text=f"ID: {produto[0]} | Nome: {produto[1]} | Descrição: {produto[2]} | Valor: {produto[3]} | Quantidade: {produto[4]}")
            printa.pack(padx=10, pady=10)

#botoes pedidos
    def VisuPedidos(self):
        janela = ck.CTkToplevel(self)
        janela.title("Pedidos")

        frame = ck.CTkScrollableFrame(janela)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        pedidos = ad.Pedidos()
        for pedido in pedidos:
            printa =ck.CTkLabel(frame, text=f"ID: {pedido[0]} | Dia: {pedido[2]} | Status: {pedido[4]} | Total: {pedido[5]}")
            printa.pack(padx=10, pady=10)

    def PedidoCli(self):
        janela = ck.CTkToplevel(self)
        janela.title("Novo Cliente")


        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        janela.TelEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Tel = janela.TelEntry.get()

            pedidos = ad.visuPedi(Nome, Tel)
            frame = ck.CTkScrollableFrame(janela)
            frame.pack(padx=10, pady=10, fill="both", expand=True)
            for pedido in pedidos:
                printa = ck.CTkLabel(frame, text=f"ID: {pedido[0]} | Total = {pedido[1]} reais | Numero: {pedido[3]} | Status: {pedido[2]}")
                printa.pack(padx=10, pady=10)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma, fg_color="purple")
        botaoConf.pack(padx=10, pady=10)

    def MudarStatus(self):
        janela = ck.CTkToplevel(self)
        janela.title("Muda status")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        janela.TelEntry.pack(padx=20, pady=10)

        janela.NumPEntry = ck.CTkEntry(janela, placeholder_text="Coloque o numero do pedido")
        janela.NumPEntry.pack(padx=10, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Tel = janela.TelEntry.get() 
            NumP = janela.NumPEntry.get() 

            novo = ad.MudaStatus(Nome, Tel, NumP)
            self.msgLabel.configure(text=novo)
            janela.after(2000, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def CancelaPedido(self):
        janela = ck.CTkToplevel(self)
        janela.title("Cancela Pedido")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        janela.TelEntry.pack(padx=20, pady=10)

        janela.NumPEntry = ck.CTkEntry(janela, placeholder_text="Coloque o numero do pedido")
        janela.NumPEntry.pack(padx=10, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Tel = janela.TelEntry.get() 
            NumP = janela.NumPEntry.get() 

            novo = ad.Cancela(Nome, Tel, NumP)
            self.msgLabel.configure(text=novo)
            janela.after(2000, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

#botoes consultas

    def MaisPaga(self):
        janela = ck.CTkToplevel(self)
        janela.title("Pagamento mais usado")

        resultado = ad.PagamentoMais()
        if resultado is None:
                printa = ck.CTkLabel(janela, text=f"Nao houve pagamentos")
                printa.pack(padx=10, pady=10)
        for pag in resultado:
            printa =ck.CTkLabel(janela, text=f"Metodo: {pag[0]} | Quantidade: {pag[1]}")
            printa.pack(padx=10, pady=10)

    def MediaValor(self):
        janela = ck.CTkToplevel(self)
        janela.title("Média de valor de vendas")

        resultado = ad.MediAnual()
        if resultado is None:
                printa = ck.CTkLabel(janela, text=f"Nao houve vendas")
                printa.pack(padx=10, pady=10)
        for med in resultado:
            printa =ck.CTkLabel(janela, text=f"Ano: {med[0]} | Valor: {med[1]}")
            printa.pack(padx=10, pady=10)

    def MaiorVenda(self):
        janela = ck.CTkToplevel(self)
        janela.title("Maior mes e ano de vendas")

        resultado = ad.M_A_Vendas()
        if resultado is None:
                printa = ck.CTkLabel(janela, text=f"Nao houve vendas")
                printa.pack(padx=10, pady=10)
        for i in resultado:
            printa = ck.CTkLabel(janela, text=f"Ano: {i[0]}| Mes: {i[1]} | Pedidos: {i[2]}")
            printa.pack(padx=10, pady=10)

    def ClienteAnual(self):
        janela = ck.CTkToplevel(self)
        janela.title("Cliente Anual")

        janela.AnoEntry = ck.CTkEntry(janela, placeholder_text="Coloque o ano")
        janela.AnoEntry.pack(padx=20, pady=10)

        def confirma():

            ano = janela.AnoEntry.get()

            resultado = ad.ClienteAnual(ano)
            if resultado is None:
                printa = ck.CTkLabel(janela, text=f"Nao houve clientes com compras todos os meses no ano {ano}")
                printa.pack(padx=10, pady=10)

            for i in resultado:
                printa = ck.CTkLabel(janela, text=f"ID: {i[0]}")
                printa.pack(padx=10, pady=10)


        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def ProdutoMais(self):
        janela = ck.CTkToplevel(self)
        janela.title("Produto Mais vendido")

        resultado = ad.ProdutoMais()
        if resultado is None:
                printa = ck.CTkLabel(janela, text=f"Nao houve venda")
                printa.pack(padx=10, pady=10)
        j = 1
        for prod in resultado:
            printa =ck.CTkLabel(janela, text=f"{j}° Produto: {prod[0]} | Quantidade: {prod[1]}")
            printa.pack(padx=10, pady=10)
            j += 1