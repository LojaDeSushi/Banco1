import customtkinter as ck
from tkinter import messagebox
import admin as ad

class MenuAdmin(ck.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu Adminstrador")
        self.geometry("900x600")

        cabecalho = ck.CTkFrame(self)
        cabecalho.pack(padx=20, pady=(15,5))

        msgCabe = ck.CTkLabel(cabecalho, text=f"Bem vindo!", font=("", 15, "bold"))
        msgCabe.pack(side="left")

        self.abas = ck.CTkTabview(self)
        self.abas.pack(padx=20, pady=20, fill="both", expand=True)

        self.abas.add("Clientes")
        self.abas.add("Produtos")
        self.abas.add("Pedidos")
        self.abas.add("Consultas")
        self.abas.add("Atendentes")

        self._build_aba_clientes()
        self._build_aba_produtos()
        self._build_aba_pedidos()
        self._build_aba_consultas()
        self._build_aba_atendentes()
        

#------------------------------------------ ABAS -----------------------------

# ── Aba Clientes ─────────────────────────────────────────────
    def _build_aba_clientes(self):
        abaCli=self.abas.tab("Clientes")

        col = ck.CTkFrame(abaCli, fg_color="transparent")
        col.pack(fill="both", expand=True, padx=5, pady=5)
        col.columnconfigure((0,1), weight=1)

        #coluna esquerda
        botao = ck.CTkFrame(col)
        botao.grid(row = 0, column = 0, padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(botao, text="Opções Clientes", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        botaoNC =ck.CTkButton(botao, text="Novo Cliente", command=self.novoCliente)
        botaoNC.pack(padx=10, pady=10)

        botaoAC =ck.CTkButton(botao, text="Atualiza Cliente", command=self.AtualizaCliente)
        botaoAC.pack(padx=10, pady=10)

        botaoDC =ck.CTkButton(botao, text="Deleta Cliente", command=self.DeletaCliente)
        botaoDC.pack(padx=10, pady=10)

        #coluna direita
        cli = ck.CTkFrame(col)
        cli.grid(row=0, column = 1, padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(cli, text="Clientes", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        self.frameCli = ck.CTkScrollableFrame(cli)
        self.frameCli.pack(padx=5, pady=5, fill="both", expand=True)
        self.Clientes()

        botaoFiltro =ck.CTkButton(cli, text="Filtrar clientes", command=self.FiltraCliente)
        botaoFiltro.pack(padx=10, pady=10, anchor="w")


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

    def Clientes(self, clientes=None):
        for w in self.frameCli.winfo_children():
            w.destroy()
        
        if clientes is None:
            clientes = ad.Usuarios()

        for cliente in clientes:
            texto = f"ID: {cliente[0]} | Nome: {cliente[1]} | Tel: {cliente[3]} | Cidade: {cliente[5]} | Estado: {cliente[7]}"
            printa = ck.CTkLabel(self.frameCli, text=texto, anchor="w", wraplength=350)
            printa.pack(padx=10, pady=4, fill="x", anchor="w")

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
            self.Clientes(novo)
    
        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

# ── Aba Produtos ─────────────────────────────────────────────
    def _build_aba_produtos(self):
        abaProduto=self.abas.tab("Produtos")

        col = ck.CTkFrame(abaProduto, fg_color="transparent")
        col.pack(fill="both", expand=True, padx=5, pady=5)
        col.columnconfigure((0,1), weight=1)

        #coluna esquerda
        botao = ck.CTkFrame(col)
        botao.grid(row = 0, column = 0, padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(botao, text="Opções Produtos", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        botaoNP =ck.CTkButton(botao, text="Novo Produto", command=self.NovoProdu)
        botaoNP.pack(padx=10, pady=10)

        botaoAP =ck.CTkButton(botao, text="Atualiza Produto", command=self.AtualizaProdu)
        botaoAP.pack(padx=10, pady=10)

        botaoDP =ck.CTkButton(botao, text="Deleta Produto", command=self.DeletaProdu)
        botaoDP.pack(padx=10, pady=10)

        #coluna direita
        pro = ck.CTkFrame(col)
        pro.grid(row=0, column = 1, padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(pro, text="Produtos", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        self.framePro = ck.CTkScrollableFrame(pro)
        self.framePro.pack(padx=5, pady=5, fill="both", expand=True)

        self.Produtos()

        botaoAL =ck.CTkButton(pro, text="Atualizar lista", command=self.Produtos)
        botaoAL.pack(padx=10, pady=10, anchor="w")


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

    def Produtos(self):
        for w in self.framePro.winfo_children():
            w.destroy()

        produtos = ad.Produtos()
        if not produtos:
            ck.CTkLabel(self.framePro, text="Nenhum produto cadastrado").pack()

        for produto in produtos:
            texto1 = f"ID: {produto[0]} | Nome: {produto[1]} | Descrição: {produto[2]} | Valor: {produto[3]} | Quantidade: {produto[4]}"
            printa1 = ck.CTkLabel(self.framePro, text=texto1, anchor="w", wraplength=350)
            printa1.pack(padx=10, pady=4, fill="x", anchor="w")


# ── Aba Pedidos ─────────────────────────────────────────────
    def _build_aba_pedidos(self):
        abaPedido=self.abas.tab("Pedidos")

        topo = ck.CTkFrame(abaPedido)
        topo.pack(fill="x", padx=5, pady=(5,0))

        botaoVPC =ck.CTkButton(topo, text="Visualizar Pedido Cliente", command=self.PedidoCli)
        botaoVPC.pack(padx=10, pady=(10, 4), side="left")

        botaoVPC =ck.CTkButton(topo, text="Pedidos clientes", command=self.VisuPedidos)
        botaoVPC.pack(padx=10, pady=10, side="right")

        self.framePed = ck.CTkScrollableFrame(abaPedido)
        self.framePed.pack(fill="both", expand=True, padx=5, pady=5)

        self.VisuPedidos()


    def VisuPedidos(self, pedidos=None):
        for w in self.framePed.winfo_children():
            w.destroy()

        if pedidos is None:
            pedidos = ad.Pedidos()
            
        for pedido in pedidos: 
            self.Id_pedido = pedido['id'] 
            Total = pedido['total']
            Numero = pedido['num_pedido']
            Status = pedido['status']
            Pagamento = pedido['pagamento']
            Produtos = pedido['produtos']

            linha = ck.CTkFrame(self.framePed)
            linha.pack(fill="x", padx=4, pady=3)

            if pedido['status'] != 'Cancelado':
                ck.CTkLabel(linha, text=f"#{self.Id_pedido}", font=("", 12, "bold"), width=50).pack(side="left", padx=8)
                ck.CTkLabel(linha, text=f"{Produtos}", width=150, anchor="w").pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"{Pagamento}", text_color="gray", width=100).pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"R$ {Total}", width=80).pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"{Status}", width=80).pack(side="left", padx=4)

                botaoCP=ck.CTkButton(linha, text="Cancelar Pedido", fg_color="red", width=70, command=lambda i=self.Id_pedido: self._salvar_status(i))
                botaoCP.pack(side="right", padx=10)
            
                botaoAT=ck.CTkButton(linha, text="Atualizar Status", width=70, command=lambda i=self.Id_pedido: self.MudarStatus(i))
                botaoAT.pack(side="right", padx=10)

            else:
                ck.CTkLabel(linha, text=f"#{self.Id_pedido}", font=("", 12, "bold"), width=50).pack(side="left", padx=8)
                ck.CTkLabel(linha, text=f"{Produtos}", width=150, anchor="w").pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"{Status}", text_color="red", width=80).pack(side="left", padx=4)
            
    def PedidoCli(self):
        janela = ck.CTkToplevel(self)
        janela.title("Pedido Cliente")

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
            self.VisuPedidos(pedidos)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma, fg_color="purple")
        botaoConf.pack(padx=10, pady=10)

    def MudarStatus(self, id_ped):
        ad.MudaStatus(id_ped)
        self.VisuPedidos()

    def CancelaPedido(self, id_ped):
        ad.Cancela(id_ped)
        self.VisuPedidos()

# ── Aba Consultas ─────────────────────────────────────────────
    def _build_aba_consultas(self):
        abaConsul=self.abas.tab("Consultas")

        botoes = ck.CTkFrame(abaConsul, fg_color="transparent")
        botoes.pack(fill="x", expand=True, padx=5, pady=(5, 0))

        botaoPagM =ck.CTkButton(botoes, text="Pagamento mais usado", command= lambda: self.Mostrar("pagmais"))
        botaoPagM.pack(side="left", padx=4, pady=8)

        botaoMediaPe =ck.CTkButton(botoes, text="Media de vendas", command= lambda: self.Mostrar("media"))
        botaoMediaPe.pack(side="left", padx=4, pady=8)

        botaoMaioV_MA =ck.CTkButton(botoes, text="Maior mês/ano", command= lambda: self.Mostrar("maior"))
        botaoMaioV_MA.pack(side="left", padx=4, pady=8)

        botaoClienAnual =ck.CTkButton(botoes, text="Cliente anual", command= lambda: self.Mostrar("cliente"))
        botaoClienAnual.pack(side="left", padx=4, pady=8)

        botaoProdutoMais =ck.CTkButton(botoes, text="Produto mais vendido", command= lambda: self.Mostrar("produto"))
        botaoProdutoMais.pack(side="left", padx=4, pady=8)

        self.frameConsul = ck.CTkScrollableFrame(abaConsul)
        self.frameConsul.pack(fill="both", expand=True, padx=5, pady=5)

        self.Mostrar("media")
        

    def LimparConsul(self):
        for w in self.frameConsul.winfo_children():
            w.destroy()

    def Mostrar(self, consulta):
        self.LimparConsul()

        if consulta == "pagmais":
            self.MaisPaga()
        elif consulta == "media":
            self.MediaValor()
        elif consulta == "maior":
            self.MaiorVenda()
        elif consulta == "cliente":
            self.ClienteAnual()
        elif consulta == "produto":
            self.ProdutoMais()

    def MaisPaga(self):
        resultado = ad.PagamentoMais()
        ck.CTkLabel(self.frameConsul, text="Métodos de pagamento mais usados", font=("", 13, "bold")).pack(anchor="w", padx=10, pady=(10,4))

        if resultado is None:
                printa = ck.CTkLabel(self.frameConsul, text="Não houve pagamentos")
                printa.pack(padx=10, pady=10)

        for pag in resultado:
            printa =ck.CTkLabel(self.frameConsul, text=f"Metodo: {pag[0]} | Quantidade: {pag[1]}")
            printa.pack(padx=10, pady=10)

    def MediaValor(self):
        resultado = ad.MediAnual()
        ck.CTkLabel(self.frameConsul, text="Média de pedidos", font=("", 13, "bold")).pack(anchor="w", padx=10, pady=(10,4))
        
        if resultado is None:
                printa = ck.CTkLabel(self.frameConsul, text=f"Não houve vendas")
                printa.pack(padx=10, pady=10)

        for med in resultado:
            printa =ck.CTkLabel(self.frameConsul, text=f"Ano: {med[0]} | Média de R$ {med[1]:.2f}")
            printa.pack(padx=10, pady=10)

    def MaiorVenda(self):
        resultado = ad.M_A_Vendas()
        ck.CTkLabel(self.frameConsul, text="Mês e ano com maior vendas", font=("", 13, "bold")).pack(anchor="w", padx=10, pady=(10,4))
        
        if resultado is None:
                printa = ck.CTkLabel(self.frameConsul, text="Não houve vendas")
                printa.pack(padx=10, pady=10)

        printa = ck.CTkLabel(self.frameConsul, text=f"Ano: {resultado[0]}| Mês: {resultado[1]} | Pedidos: {resultado[2]}")
        printa.pack(padx=10, pady=10)

    def ClienteAnual(self):
        ck.CTkLabel(self.frameConsul, text="Clientes que compraram todos os meses", font=("", 13, "bold")).pack(anchor="w", padx=10, pady=(10,4))

        linha = ck.CTkFrame(self.frameConsul)
        linha.pack(anchor="w", padx=10, pady=4)

        AnoEntry = ck.CTkEntry(linha, placeholder_text="Coloque o ano", width=120)
        AnoEntry.pack(side="left", padx=(0,6))

        self.frameCliResult = ck.CTkFrame(self.frameConsul)
        self.frameCliResult.pack(fill="x", padx=10, pady=4)

        def pesquisa():
            for w in self.frameCliResult.winfo_children():
                w.destroy()

            ano = AnoEntry.get()

            resultado = ad.ClienteAnual(ano)
            if resultado is None:
                printa = ck.CTkLabel(self.frameCliResult, text=f"Não houve clientes com compras todos os meses em {ano}")
                printa.pack(anchor="w", pady=4)

            for i in resultado:
                printa = ck.CTkLabel(self.frameCliResult, text=f"ID: {i[0]}")
                printa.pack(anchor="w", pady=2)


        botaoConf = ck.CTkButton(linha, text="Buscar", command=pesquisa)
        botaoConf.pack(side="left")

    def ProdutoMais(self):
        ck.CTkLabel(self.frameConsul, text="Ranking de produtos", font=("", 13, "bold")).pack(anchor="w", padx=10, pady=(10,4))
        resultado = ad.ProdutoMais()

        if resultado is None:
                printa = ck.CTkLabel(self.frameConsul, text=f"Nao houve venda")
                printa.pack(padx=10, pady=10)
        j = 1
        for prod in resultado:
            printa =ck.CTkLabel(self.frameConsul, text=f"{j}° Produto: {prod[0]} | Quantidade: {prod[1]}")
            printa.pack( padx=10, pady=4)
            j += 1


# ── Aba Atendentes ─────────────────────────────────────────────
    def _build_aba_atendentes(self):
        abaAten=self.abas.tab("Atendentes")

        col = ck.CTkFrame(abaAten, fg_color="transparent")
        col.pack(fill="both", expand=True, padx=5, pady=5)
        col.columnconfigure((0,1), weight=1)

        #coluna esquerda
        botao = ck.CTkFrame(col)
        botao.grid(row = 0, column = 0, padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(botao, text="Opções Atendentes", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        botaoNA =ck.CTkButton(botao, text="Novo Atendente", command=self.NovoAtendente)
        botaoNA.pack(padx=10, pady=10)

        botaoDA =ck.CTkButton(botao, text="Deleta Atendente", command=self.DeletaAtendente)
        botaoDA.pack(padx=10, pady=10)

        #coluna direita
        ate = ck.CTkFrame(col)
        ate.grid(row=0, column = 1, padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(ate, text="Atendentes", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        self.frameAte = ck.CTkScrollableFrame(ate)
        self.frameAte.pack(padx=5, pady=5, fill="both", expand=True)
        self.Atendente()

        botaoVPC =ck.CTkButton(ate, text="Atualizar Atendentes", command=self.Atendente)
        botaoVPC.pack(padx=10, pady=10, side="right")


    def NovoAtendente(self):

        janela = ck.CTkToplevel(self)
        janela.title("Novo Atendente")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        janela.LoginEntry = ck.CTkEntry(janela, placeholder_text="Coloque o login")
        janela.LoginEntry.pack(padx=20, pady=10)

        janela.SenhaEntry = ck.CTkEntry(janela, placeholder_text="Coloque a senha")
        janela.SenhaEntry.pack(padx=10, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Login = janela.LoginEntry.get()
            Senha = janela.SenhaEntry.get()

            novo = ad.NovoAtendente(Login, Senha, Nome)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def DeletaAtendente(self):
        janela = ck.CTkToplevel(self)
        janela.title("Deleta Atendente")

        janela.loginEntry = ck.CTkEntry(janela, placeholder_text="Coloque o login")
        janela.loginEntry.pack(padx=20, pady=10)

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        janela.NomeEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()
            Login = janela.LoginEntry.get()

            novo = ad.mataAtendente(Nome, Login)
            self.msgLabel.configure(text=novo)
            janela.after(1500, janela.destroy)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

    def Atendente(self):
        for w in self.frameAte.winfo_children():
            w.destroy()

        atendentes = ad.Atendentes()
        for atendente in atendentes:
            printa =ck.CTkLabel(self.frameAte, text=f"ID: {atendente["id"]} | Nome: {atendente["nome"]} | pedidos: {atendente["pedidos"]}")
            printa.pack(padx=10, pady=10)
