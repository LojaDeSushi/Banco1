import customtkinter as ck
import cliente as cl

class MenuCliente(ck.CTk):
    def __init__(self, login):
        super().__init__()
        self.geometry("900x600")

        id_cliente = cl.BuscaIdWeb(login)

        dados = cl.BuscaNomeTel(id_cliente)
        self.nome, self.tel = dados

        self.title(f"Menu {self.nome}")

        cabecalho = ck.CTkFrame(self)
        cabecalho.pack(padx=20, pady=(15,5))

        msgCabe = ck.CTkLabel(cabecalho, text=f"Bem vindo {self.nome}!", font=("", 15, "bold"))
        msgCabe.pack(side="left")

        self.abas = ck.CTkTabview(self)
        self.abas.pack(padx=20, pady=10, fill="both", expand=True)

        self.abas.add("Produtos")
        self.abas.add("Pedidos")
        self.abas.add("Carrinho")

        self._build_aba_produtos()
        self._build_aba_pedidos()
        self._build_aba_carrinho()

#--------------------------------------- ABAS --------------------------------------------

# ── Aba Produtos ─────────────────────────────────────────────
    def _build_aba_produtos(self):
        abaProduto=self.abas.tab("Produtos")
        
        botaoNP =ck.CTkButton(abaProduto, text="Busca Produto", command=self.BuscaProdu)
        botaoNP.pack(padx=10, pady=10)

        self.msgProd = ck.CTkLabel(abaProduto, text="")
        self.msgProd.pack(padx=15, pady=15)

        self.frame = ck.CTkScrollableFrame(abaProduto)
        self.frame.pack(padx=5, pady=5, fill="both", expand=True)

        produtos = cl.Produtos()
        if not produtos:
            ck.CTkLabel(self.frame, text="Nenhum produto").pack()
        else:
            for produto in produtos:
                nome = produto[1]
                desc = produto[2]
                valor = produto[3]
                quant = produto[4]

                linha = ck.CTkFrame(self.frame)
                linha.pack(padx = 5, pady = 5, fill="x")

                if quant < 1:
                    ck.CTkLabel(linha,text=nome, width=160, anchor="w").pack(side="left", padx=10)
                    ck.CTkLabel(linha, text=desc, anchor="w").pack(side="left", padx=4)
                    ck.CTkLabel(linha, text=f"Sem estoque :(", width=80, anchor="e").pack(side="right", padx=10)
                
                else:
                    ck.CTkLabel(linha, text=nome, width=160, anchor="w").pack(side="left", padx=10)
                    ck.CTkLabel(linha, text=desc, anchor="w", width=200).pack(side="left", padx=4)
                    ck.CTkLabel(linha, text=f" R$ {valor}", width=80, anchor="e").pack(side="right", padx=10)
                    ck.CTkLabel(linha, text=f"tem {quant} no estoque", text_color="grey", anchor="w").pack(side="left", padx=0)

                    botaoADD = ck.CTkButton(linha, text="Add Carrinho", width=100, fg_color="green", command=lambda n=nome: self.AddProd(n))
                    botaoADD.pack(side="right", padx=6)

    def AddProd(self, nomeP):
        teste =cl.AddItemCarr(self.nome, self.tel, nomeP, 1)
        self.msgProd.configure(text=teste)
        self.msgProd.after(1500, lambda: self.msgProd.configure(text=""))

        self.VisuCarrinho()
    
    def BuscaProdu(self):
        janela = ck.CTkToplevel(self)
        janela.title("Busca Produto")

        janela.NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome do produto")
        janela.NomeEntry.pack(padx=20, pady=10)

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)

        def confirma():

            Nome = janela.NomeEntry.get()

            novo = cl.BuscaProd(Nome)
            self.msgLabel.configure(text=novo)

        botaoConf = ck.CTkButton(janela, text="Confirmar", command=confirma)
        botaoConf.pack(padx=10, pady=10)

# ── Aba Pedidos ─────────────────────────────────────────────    
    def _build_aba_pedidos(self):
        abaPedido=self.abas.tab("Pedidos")

        self.frame = ck.CTkScrollableFrame(abaPedido)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        botaoCP =ck.CTkButton(abaPedido, text="Cancelar Pedido", command=self.CancelaPedido)
        botaoCP.pack(padx=10, pady=10)

        self.VisuPedidos()

    def VisuPedidos(self):
        for w in self.frame.winfo_children():
            w.destroy()

        pedidos = cl.visuPedi(self.nome, self.tel)
        if not pedidos:
            ck.CTkLabel(self.frame, text="Nenhum pedido feito")
            return
        
        for pedido in pedidos:
            self.numP = pedido['num_pedido']
            Status = pedido['status']
            Produtos = pedido['produtos']
            Total = pedido['total']
            Pagamento = pedido['pagamento']

            linha = ck.CTkFrame(self.frame)
            linha.pack(fill="x", padx = 5, pady = 5)

            if pedido['status'] != 'Cancelado':
                ck.CTkLabel(linha, text=f"#{self.numP}", font=("", 12, "bold"), width=50).pack(side="left", padx=8)
                ck.CTkLabel(linha, text=f"{Produtos}", text_color="gray", width=100).pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"R$ {Total}", width=80).pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"{Pagamento}", width=150, anchor="w").pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"Status {Status}", width=80).pack(side="left", padx=4)

                botaoCP=ck.CTkButton(linha, text="Cancelar", fg_color="red", width=70, command=lambda i=self.numP: self.CancelaPedido(i))
                botaoCP.pack(side="right", padx=10)

            else:
                ck.CTkLabel(linha, text=f"#{self.numP}", font=("", 12, "bold"), width=50).pack(side="left", padx=8)
                ck.CTkLabel(linha, text=f"{Produtos}", text_color="gray", width=100).pack(side="left", padx=4)
                ck.CTkLabel(linha, text=f"Status {Status}",text_color="red", width=80).pack(side="left", padx=4)

    def CancelaPedido(self, numP):
        cl.Cancela(self.nome, self.tel, numP)
        self.VisuPedidos()

# ── Aba Carrinho ─────────────────────────────────────────────
    def _build_aba_carrinho(self):
        abaCarrinho=self.abas.tab("Carrinho")

        self.frameCarrinho = ck.CTkScrollableFrame(abaCarrinho, height=180)
        self.frameCarrinho.pack(padx=10, pady=10, fill="both", expand=True)

        botaoFC =ck.CTkButton(abaCarrinho, text="Finalizar Carrinho", fg_color="green",command=self.FinalizaCarr)
        botaoFC.pack(anchor="w", padx=10, pady=10)

        botaoVC =ck.CTkButton(abaCarrinho, text="Visualizar Carrinho", command=self.VisuCarrinho)
        botaoVC.pack(anchor="w", padx=10, pady=10)

    def VisuCarrinho(self):
        for widget in self.frameCarrinho.winfo_children():
            widget.destroy()

        itens = cl.visuCar(self.nome, self.tel)

        if not itens:
            ck.CTkLabel(self.frameCarrinho, text="Carrinho vazio").pack()
            return
        
        for item in itens:
            linha = ck.CTkFrame(self.frameCarrinho)
            linha.pack(padx = 5, pady = 5, fill="x")

            ck.CTkLabel(linha, text=f"{item['quantidade']}x {item['nome']}", width=250).pack(side="left", padx=10)

            botaoRM = ck.CTkButton(linha, text="Remover", width=100, fg_color="red", command=lambda n=item['nome']: self.RemoveCarr(n))
            botaoRM.pack(side="right", padx=10)

    def RemoveCarr(self, nomeP):
        cl.RemoveItemCar(self.nome, self.tel, nomeP, 1)
        self.VisuCarrinho()

    def FinalizaCarr(self):
        pedido = cl.Pedido(self.nome, self.tel)

        janela = ck.CTkToplevel(self)
        janela.title("Pagamento")

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=10, pady=10)
        
        self.msgLabel.configure(text=f"Seu pedido numero {pedido[0]} ficou no total de R$ {pedido[1]}")

        self.pag = []

        self.framePag = ck.CTkScrollableFrame(janela, height=150)
        self.framePag.pack(padx=10, pady=5, fill='x')

        linha = ck.CTkFrame(janela)
        linha.pack(padx = 5, pady = 5, fill="x")

        self.tipo = ck.StringVar(value="Pix")
        tipos = ck.CTkOptionMenu(linha, values=["Pix", "Cartão", "Boleto"], variable=self.tipo)
        tipos.pack(side="left", padx=5)

        self.valorEntry = ck.CTkEntry(linha, placeholder_text="Valor R$", width=100)
        self.valorEntry.pack(side="left", padx=5)

        botaoPag = ck.CTkButton(linha, text="Add pag", width=100, fg_color="blue", command= lambda: self.AddPag(pedido[1]))
        botaoPag.pack(side="right", padx=10)

        self.mensagemPag = ck.CTkLabel(janela, text="")
        self.mensagemPag.pack(padx=10, pady=5)

        BotaoConf= ck.CTkButton(janela, text="Confirmar Pagamento", fg_color="green", command=lambda: self.ConfirmaPag(pedido[0], janela))
        BotaoConf.pack(padx=10, pady=10)

    def AddPag(self, total):
        total = float(total)
        try:
            valor = float(self.valorEntry.get())
        except ValueError or valor < 1:
            self.mensagemPag.configure(text="Valor invalido")
            return

        totalParc = sum(t['valor'] for t in self.pag)

        if totalParc + valor > total:
            self.mensagemPag.configure(text=f"Valor acima do total R${total}")
            return
        
        self.pag.append({'metodo': self.tipo.get(), 'valor': valor})

        met = ck.CTkLabel(self.framePag, text=f"{self.tipo.get()} -> R$ {valor}")
        met.pack()

        totalParc += valor
        falta = total - totalParc

        if falta > 0:
            self.mensagemPag.configure(text=f"Faltam ainda R${falta}") 
        else:
            self.mensagemPag.configure(text="Tudo pago!!")

    def ConfirmaPag(self, numP, janela):
        if not self.pag:
            self.mensagemPag.configure(text="Adicione pelo menos um pag")
            return
        
        resultado = cl.Pagamento(self.nome, self.tel, numP, self.pag)
        self.mensagemPag.configure(text=resultado)

        self.VisuCarrinho()

        if resultado == "Pagamento feito com sucesso":
            janela.after(1500, janela.destroy)

