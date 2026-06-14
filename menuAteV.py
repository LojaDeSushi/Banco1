import customtkinter as ck
import atendente as at
import menuCliV as mc

class MenuAtendente(ck.CTk):
    def __init__(self, login):
        super().__init__()
        self.title("Menu Atendente")
        self.geometry("900x600")

        self.id_atendente = at.BuscaAtende(login)

        cabecalho = ck.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", padx=20, pady=(15,5))

        ck.CTkLabel(cabecalho, text=f"Bem vindo ", font=("", 15,"bold") ).pack(side="left")

        self.labelCli = ck.CTkLabel(cabecalho, text="", text_color="green")
        self.labelCli.pack(side="right", padx=10)

        self.abas = ck.CTkTabview(self)
        self.abas.pack(padx=20, pady=10, fill="both", expand=True)

        self.abas.add("Atendimento")
        self.abas.add("Produtos")
        self.abas.add("Pedidos")

        self._build_aba_atendimento()
        self._build_aba_produtos()
        self._build_aba_pedidos()

#------------------------------------------ ABAS -------------------------------------------------------------

# ── Aba Atendimento ─────────────────────────────────────────────
    def _build_aba_atendimento(self):
        abAtendi = self.abas.tab("Atendimento")

        col = ck.CTkFrame(abAtendi, fg_color="transparent")
        col.pack(fill="both", expand=True, padx=5, pady=5)
        col.columnconfigure((0,1), weight=1)

        #coluna esquerda - atendimento
        cli = ck.CTkFrame(col)
        cli.grid(row=0, column=0,padx=(0,8), pady=0, sticky="nsew")

        ck.CTkLabel(cli, text="Cliente em atendimento", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        self.labelNomeCli = ck.CTkLabel(cli, text="—", text_color="gray")
        self.labelNomeCli.pack(padx=12, pady=2, anchor="w")

        self.labelTelCli = ck.CTkLabel(cli, text="—", text_color="gray")
        self.labelTelCli.pack(padx=12, pady=2, anchor="w")

        frame_btns = ck.CTkFrame(cli, fg_color="transparent")
        frame_btns.pack(padx=12, pady=10, anchor="w")

        ck.CTkButton(frame_btns,text="▶  Iniciar atendimento", width=170,
                     command=self.abrirAtendimento).pack(side="left", padx=(0, 6))

        self.btnEncerrar = ck.CTkButton(frame_btns, text="Encerrar", width=100,
                                        fg_color="transparent", border_width=1,
                                        text_color=("gray10", "gray90"),
                                        command=self.encerrarAtendimento, state="disabled")
        self.btnEncerrar.pack(side="left")

        # Coluna direita – carrinho
        frame_carr = ck.CTkFrame(col)
        frame_carr.grid(row=0, column=1, padx=(8, 0), pady=0, sticky="nsew")

        ck.CTkLabel(frame_carr, text="Carrinho", font=("", 13, "bold")).pack(padx=12, pady=(12, 4), anchor="w")

        self.frameItensCarr = ck.CTkScrollableFrame(frame_carr, height=180)
        self.frameItensCarr.pack(fill="x", padx=12, pady=4)

        self.labelCarrinhoVazio = ck.CTkLabel(self.frameItensCarr, text="Nenhum item adicionado", text_color="gray")
        self.labelCarrinhoVazio.pack(pady=20)

        botaoFC= ck.CTkButton(frame_carr, text="✔  Finalizar pedido", fg_color="green", command=self.FinalizaCarr)
        botaoFC.pack(padx=12, pady=(4, 12), anchor="w")
        
        botaoVC =ck.CTkButton(frame_carr, text="Visualizar Carrinho", command=self.AtualizarCarrinho)
        botaoVC.pack(padx=12, pady=(4, 12), anchor="w")

    def abrirAtendimento(self):
        janela = ck.CTkToplevel(self)
        janela.title("Iniciar atendimento")
        janela.grab_set()

        ck.CTkLabel(janela, text="Buscar cliente", font=("", 15, "bold")).pack(padx=20, pady=(16, 4))

        nomeEntry = ck.CTkEntry(janela, placeholder_text="Nome completo", width=260)
        nomeEntry.pack(padx=20, pady=6)

        telEntry = ck.CTkEntry(janela, placeholder_text="Telefone", width=260)
        telEntry.pack(padx=20, pady=6)

        msgErr = ck.CTkLabel(janela, text="", text_color="red")
        msgErr.pack(padx=20)

        def confirma():
            nome = nomeEntry.get()
            tel = telEntry.get()
            if not nome or not tel:
                msgErr.configure(text="Preencha nome e telefone.")
                return
            conta = at.BuscaId(nome, tel)
            if conta is None:
                msgErr.configure(text="Cliente não encontrado.")
                return
            self.nomeCli = nome
            self.telCli = tel
            self.labelNomeCli.configure(text=f"Nome: {nome}", text_color=("gray10", "gray90"))
            self.labelTelCli.configure(text=f"Tel: {tel}", text_color=("gray10", "gray90"))
            self.labelCli.configure(text=f"● Atendendo: {nome}")
            self.btnEncerrar.configure(state="normal")
            self.AtualizarCarrinho()
            janela.destroy()

        frame_btns = ck.CTkFrame(janela, fg_color="transparent")
        frame_btns.pack(pady=12)
        ck.CTkButton(frame_btns, text="Cancelar", fg_color="transparent",
                     border_width=1, text_color=("gray10", "gray90"),
                     command=janela.destroy, width=110).pack(side="left", padx=4)
        ck.CTkButton(frame_btns, text="Confirmar", command=confirma, width=110).pack(side="left", padx=4)

    def encerrarAtendimento(self):
        self.nomeCli = None
        self.telCli = None
        self.labelNomeCli.configure(text="—", text_color="gray")
        self.labelTelCli.configure(text="—", text_color="gray")
        self.labelCli.configure(text="")
        self.btnEncerrar.configure(state="disabled")

# ── Aba Produtos ─────────────────────────────────────────────
    def _build_aba_produtos(self):
        aba = self.abas.tab("Produtos")

        frame = ck.CTkScrollableFrame(aba)
        frame.pack(fill="both", expand=True, padx=5, pady=5)

        produtos = at.Produtos()
        if not produtos:
            ck.CTkLabel(frame, text="Nenhum produto cadastrado").pack()

        for produto in produtos:
            nome = produto[1]
            desc = produto[2]
            valor =produto[3]

            linha = ck.CTkFrame(frame)
            linha.pack(fill="x", padx=4, pady=3)

            ck.CTkLabel(linha, text=nome, width=160, anchor="w").pack(side="left", padx=10)
            ck.CTkLabel(linha, text=desc, text_color="gray", anchor="w").pack(side="left", padx=4)
            ck.CTkLabel(linha, text=f"R$ {valor}", width=80, anchor="e").pack(side="right", padx=10)
            botaoADD = ck.CTkButton(linha, text="+ Carrinho", width=100, fg_color="green", command=lambda n=nome: self.AddProd(n))
            botaoADD.pack(side="right", padx=6)

    def AddProd(self, nomeP):
        if not self.nomeCli:
            self.labelCli.configure(text="⚠ Inicie um atendimento primeiro", text_color="orange")
            self.after(2000, lambda: self.labelCli.configure(text="", text_color="green"))
            return
        at.AddItemCarr(self.nomeCli, self.telCli, nomeP, 1)
        self.AtualizarCarrinho()

# ── Aba Pedidos ──────────────────────────────────────────────
    def _build_aba_pedidos(self):
        aba = self.abas.tab("Pedidos")

        ck.CTkButton(aba, text="↺  Atualizar lista",
                     command=self.CarregarPedidos).pack(anchor="w", padx=10, pady=(10, 4))

        self.framePedidos = ck.CTkScrollableFrame(aba)
        self.framePedidos.pack(fill="both", expand=True, padx=5, pady=5)

        self.CarregarPedidos()

    def CarregarPedidos(self):
        for w in self.framePedidos.winfo_children():
            w.destroy()

        pedidos = at.Pedidos(self.id_atendente) 
        if not pedidos:
            ck.CTkLabel(self.framePedidos, text="Nenhum pedido encontrado.").pack(pady=20)
            return
        
        for ped in pedidos:
            self.id_ped, data, self.numP, valor, status_atual = ped[0], ped[2], ped[3], ped[5], ped[4]

            linha = ck.CTkFrame(self.framePedidos)
            linha.pack(fill="x", padx=4, pady=3)

            ck.CTkLabel(linha, text=f"#{self.id_ped}", font=("", 12, "bold"), width=50).pack(side="left", padx=8)
            ck.CTkLabel(linha, text="nomex", width=150, anchor="w").pack(side="left", padx=4)
            ck.CTkLabel(linha, text=str(data), text_color="gray", width=100).pack(side="left", padx=4)
            ck.CTkLabel(linha, text=f"R$ {valor}", width=80).pack(side="left", padx=4)
            ck.CTkLabel(linha, text=f"Status {status_atual}", width=80).pack(side="left", padx=4)


            botaoAT=ck.CTkButton(linha, text="Atualizar Status", width=70, command=lambda i=self.id_ped: self.MudarStatus(i))
            botaoAT.pack(side="right", padx=10)

    def MudarStatus(self, id_ped):
        at.MudaStatus(id_ped) 
        self.CarregarPedidos()

# ── Carrinho ─────────────────────────────────────────────────
    def AtualizarCarrinho(self):
        for w in self.frameItensCarr.winfo_children():
            w.destroy()

        itens = at.visuCar(self.nomeCli, self.telCli)

        if not itens:
            ck.CTkLabel(self.frameItensCarr, text="Nenhum item adicionado", text_color="gray").pack(pady=20)
            return
        
        for item in itens:
            linha = ck.CTkFrame(self.frameItensCarr)
            linha.pack(padx = 4, pady = 2, anchor="w")

            ck.CTkLabel(linha, text=f"{item['quantidade']}x {item['nome']}", width=250).pack(side="left", padx=10)

            botaoRM = ck.CTkButton(linha, text="- R", width=100, fg_color="red", command=lambda n=item['nome']: self.RemoveCarr(n))
            botaoRM.pack(side="right", padx=10)

    def RemoveCarr(self, nomeP):
        at.RemoveItemCar(self.nomeCli, self.telCli, nomeP, 1)
        self.AtualizarCarrinho()

    def FinalizaCarr(self):
        if not self.nomeCli:
            return
        
        pedido = at.Pedido(self.nomeCli, self.telCli, self.id_atendente)

        janela = ck.CTkToplevel(self)
        janela.title("Pagamento")

        self.msgLabel = ck.CTkLabel(janela, text="")
        self.msgLabel.pack(padx=20, pady=(16,4))
        
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
        except ValueError:
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
        
        resultado = at.Pagamento(self.nomeCli, self.telCli, numP, self.pag)
        self.mensagemPag.configure(text=resultado)

        self.AtualizarCarrinho()

        if resultado == "Pagamento feito com sucesso":
            janela.after(1500, janela.destroy)

        


