import customtkinter as ck
import cadastro as cd
import menuAdminV as ma
import menuAteV as mt
import menuCliV as mc

ck.set_default_color_theme("green")

class App(ck.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("tela login")
        self.geometry("900x600")

        self.TituloLabel = ck.CTkLabel(self, text="Faça seu login")
        self.TituloLabel.pack(padx=20, pady=20)

        self.loginEntry = ck.CTkEntry(self, placeholder_text="Coloque seu login")
        self.loginEntry.pack(padx=20, pady=10)

        self.senhaEntry = ck.CTkEntry(self, placeholder_text="Coloque sua senha", show="*")
        self.senhaEntry.pack(padx=10, pady=5)

        self.botao = ck.CTkButton(self, text="Fazer login", command=self.Pega, hover_color="purple")
        self.botao.pack(padx=10, pady=10)

        self.msgLabel = ck.CTkLabel(self, text="")
        self.msgLabel.pack(padx=10, pady=20)

        self.botaoCadas = ck.CTkButton(self, text="Criar Cadastro", command=self.AbrirCadastro, border_width=1)
        self.botaoCadas.pack(padx=10, pady=(0, 10))

    def Pega(self):
        login = self.loginEntry.get()
        senha = self.senhaEntry.get()
        perfil = cd.login(login, senha)

        if perfil == 'admin':
            self.destroy()
            ma.MenuAdmin().mainloop()
        elif perfil == 'atendente':
            self.destroy()
            mt.MenuAtendente(login).mainloop()
        elif perfil == 'clienteweb':
            self.destroy()
            mc.MenuCliente(login).mainloop()
        else:
            self.msgLabel.configure(text=perfil)
        
    def AbrirCadastro(self):
        janela = ck.CTkToplevel(self)
        janela.title("Criar Cadastro")
        janela.grab_set()

        ck.CTkLabel(janela, text="Criar cadastro", font=("", 15, "bold")).pack(padx=20, pady=(16, 8))

        NomeEntry = ck.CTkEntry(janela, placeholder_text="Coloque o nome")
        NomeEntry.pack(padx=20, pady=10)

        NascEntry = ck.CTkEntry(janela, placeholder_text="AAAA-MM-DD")
        NascEntry.pack(padx=20, pady=10)

        TelEntry = ck.CTkEntry(janela, placeholder_text="Coloque o telefone")
        TelEntry.pack(padx=20, pady=10)

        RuaEntry = ck.CTkEntry(janela, placeholder_text="Coloque sua rua")
        RuaEntry.pack(padx=20, pady=10)

        BairroEntry = ck.CTkEntry(janela, placeholder_text="Coloque seu bairro")
        BairroEntry.pack(padx=20, pady=10)

        CidadeEntry = ck.CTkEntry(janela, placeholder_text="Coloque sua cidade")
        CidadeEntry.pack(padx=20, pady=10)

        EstadoEntry = ck.CTkEntry(janela, placeholder_text="Coloque seu estado")
        EstadoEntry.pack(padx=20, pady=10)

        web = ck.BooleanVar(value=False)
        checkWeb = ck.CTkCheckBox(janela, text="Quero criar uma conta online", variable=web, command=lambda: WebT())
        checkWeb.pack(padx=10, pady=5, anchor="w")

        frameWeb = ck.CTkFrame(janela)

        LoginEntry = ck.CTkEntry(frameWeb, placeholder_text="Coloque seu login")
        LoginEntry.pack(padx=0, pady=10)

        SenhaEntry = ck.CTkEntry(frameWeb, placeholder_text="Coloque sua senha", show="*")
        SenhaEntry.pack(padx=0, pady=10)

        def WebT():
            if web.get():
                frameWeb.pack(padx=20, pady=0)
            else:
                frameWeb.pack_forget()

        erro = ck.CTkLabel(janela, text="", text_color="red")
        erro.pack(padx=20, pady=5)
        
        def Confirma():
            Nome = NomeEntry.get()
            Nasc = NascEntry.get()
            Tel = TelEntry.get()
            Rua = RuaEntry.get()
            Bairro = BairroEntry.get()
            Cidade = CidadeEntry.get()
            Estado = EstadoEntry.get()

            if not Nome or Tel or Nasc or Rua or Bairro or Cidade or Estado:
                erro.configure(text="Preencha todos os dados")
                erro.after(1500, lambda: erro.configure(text=""))
                return
            
            resultado = cd.NovoCliente(Nome, Nasc, Tel, Rua, Cidade, Bairro, Estado)

            if web.get():
                login = LoginEntry.get()
                senha = SenhaEntry.get()

                if not login or senha:
                    erro.configure(text="Preencha todos os dados")
                    erro.after(1500, lambda: erro.configure(text=""))
                    return
                
                resultado = cd.NovoWeb(login, senha, Nome, Tel)

            erro.configure(text=str(resultado), text_color="green")
            janela.after(2500, janela.destroy)

        ck.CTkButton(janela, text="Confirmar", fg_color="purple", command=Confirma).pack(padx=20, pady=15, side="bottom")


if __name__ == "__main__":
    app = App()
    app.mainloop()
