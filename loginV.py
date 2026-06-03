import customtkinter as ck
import cadastro as cd
import menuAdminV as ma
import menuAteV as mt
import menuCliV as mc

appWidth, appHeight = 1000, 900
ck.set_default_color_theme("green")

class App(ck.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("tela login")
        self.geometry(f"{appWidth}x{appHeight}")

        self.TituloLabel = ck.CTkLabel(self, text="Faça seu login")
        self.TituloLabel.pack(padx=20, pady=20)

        self.loginEntry = ck.CTkEntry(self, placeholder_text="Coloque seu login")
        self.loginEntry.pack(padx=20, pady=10)

        self.senhaEntry = ck.CTkEntry(self, placeholder_text="Coloque sua senha", show="*")
        self.senhaEntry.pack(padx=10, pady=10)

        self.msgLabel = ck.CTkLabel(self, text="")
        self.msgLabel.pack(padx=10, pady=10)

        self.botao = ck.CTkButton(self, text="Fazer login", command=self.pega, hover_color="purple")
        self.botao.pack(padx=10, pady=10)

    def pega(self):
        login = self.loginEntry.get()
        senha = self.senhaEntry.get()
        perfil = cd.login(login, senha)

        if perfil == 'admin':
            self.destroy()
            ma.MenuAdmin().mainloop()
        elif perfil == 'atendente':
            self.destroy()
            mt.MenuAtendente().mainloop()
        elif perfil == 'clienteweb':
            self.destroy()
            mc.MenuCliente().mainloop()
        else:
            self.msgLabel.configure(text="Login invalido!")
        


if __name__ == "__main__":
    app = App()
    app.mainloop()
