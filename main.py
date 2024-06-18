from flask import *
from customtkinter import *
import tkinter as tk
import tkinter as font
import os
import webbrowser

# ANOTAÇÕES PARA OS DEV:

"""
Distância padrão entre as entradas: 0.15 no rely.
"""

app_flask = Flask(__name__)

width = 800
height = 600

# Global variables:
logged_in_username = None
logged_in_password = None

# Coleta User and Password:
def user():
    user_global = (logged_in_username)
    return  user_global
def password():
    password_global = (logged_in_password)
    return password_global

banco_senhas = {}
entradas = []
banco_user = {}

x = width / 2
y = height / 2

# Função que abre arquivo:
def open_user_file(logged_in_username):
    nome_pasta_usuario = os.path.join("users", logged_in_username)
    caminho_arquivo_senha = os.path.join(nome_pasta_usuario, f'keys_{logged_in_username}.txt')

    return caminho_arquivo_senha

# Função limpa campos:
def clear_field(*field):
    for entry in field:
        entry.delete(0, 'end')

# Criando o rótulo central
def text_central():
    text_central = tk.Label(app, text="Gerenciador de Senhas", bg="#242424", fg="white", font=("Helvetica", 16))
    text_central.pack(pady=20)


def text_central_in_app():
    text_central = tk.Label(app, text="Gerenciador de Senhas", bg="#242424", fg="white", font=("Helvetica", 16))
    text_central.place_configure(relx=0.65, rely=0.05, anchor=N)


def coletar_dados():
    global banco_user
    user, senha = login_screen()
    print(f"Usuário: {user}, Senha: {senha}")
    return user, senha


# Configurações Gerais para GUI:
janela_acesso = {'relx': 0.65, 'rely': 0.25, 'anchor': 'n', 'width': 400, 'height': 300}
janela_mensagem = {'relx': 0.5, 'rely': 0.1, 'anchor': 'n'}
janela_entrada = {'relx': 0.5, 'rely': 0.3, 'anchor': 'n'}
janela_botao = {'relx': 0.5, 'rely': 0.7, 'anchor': 'n'}


def create_user_folder(username, password):
    folder_path = os.path.join("users", username)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f'senha_{username}.txt')
    with open(file_path, 'w') as file:
        file.write(f"{password}")

    file_path_key = os.path.join(folder_path, f"keys_{username}.txt")
    with open(file_path_key, 'w') as file:
        file.write(f"")

def clear_entry(entry):
    entry.delete(0, 'end')

def limpa_campo(campo):
    campo = ""
    return campo

def destruir_entrada():
    for entrada in entradas:
        entrada.destroy()
    entradas.clear()


def selecionar_opcao(opcao):
    if opcao.strip() == "Inserir":
        inserir_nome()
    elif opcao.strip() == "Acessar":
        acessar_GUI()
    elif opcao.strip() == "Editar":
        editar()
    elif opcao.strip() == "Remover":
        remover()
    elif opcao.strip() == "Voltar":
        voltar()
    elif opcao.strip() == "Sair":
        app.quit()

def help_user(event=None):
    with app_flask.app_context():
        return render_template("index.html")

def remover():
    destruir_entrada()
    voltar()

    remover_frame = CTkFrame(master=app)
    remover_frame.place_configure(janela_acesso)

    remover_label = CTkLabel(remover_frame, text="Remover senha:")
    remover_label.place_configure(janela_mensagem)

    remover_nome = CTkEntry(remover_frame, width=250, placeholder_text="Digite o nome da senha")
    remover_nome.place_configure(relx=0.5, rely=0.25, anchor=N)

    remover_senha = CTkEntry(remover_frame, width=250, placeholder_text="Digite a senha de login")
    remover_senha.place_configure(relx=0.5, rely=0.40, anchor=N)

    def remover_():
        nome = remover_nome.get()
        senha_user = remover_senha.get()

        caminho_arquivo_senha = open_user_file(logged_in_username)

        with open(caminho_arquivo_senha, 'r') as arquivo:
            linhas = arquivo.readlines()

        senha_removida = False
        novas_linhas = []
        for linha in linhas:
            chave, valor = linha.strip().split(":")
            if chave == nome and senha_user == logged_in_password:
                senha_removida = True
            else:
                novas_linhas.append(linha)

        with open(caminho_arquivo_senha, 'a+', encoding='utf-8') as arquivo:
            arquivo.writelines(novas_linhas)

        clear_field(remover_nome, remover_senha)

        if senha_removida:
            CTkLabel(remover_frame, text="Senha removida com sucesso!").place_configure(relx=0.5, rely=0.85, anchor=N)
        else:
            CTkLabel(remover_frame, text="Senha não encontrada ou senha incorreta!").place_configure(relx=0.5, rely=0.85, anchor=N)

            
    botao_remover = CTkButton(master=remover_frame, text="Enviar", corner_radius=32, command=remover_)
    botao_remover.place_configure(janela_botao)

    help_link = CTkLabel(master=remover_frame, text="Precisa de ajuda?", cursor = "hand2")
    help_link.place_configure(relx=0.5, rely=0.82, anchor=N)

    help_link.bind("<Button-1>", help_user)
    

#================================================================================================================================================#


def editar():
    destruir_entrada()
    voltar()

    editar_frame = CTkFrame(master=app)
    editar_frame.place_configure(janela_acesso)

    editar_label = CTkLabel(editar_frame, text="Alterar Senha:")
    editar_label.place_configure(janela_mensagem)

    editar_entrada = CTkEntry(editar_frame, width=250, placeholder_text="Digite o nome da senha")
    editar_entrada.place_configure(relx=0.5, rely=0.25, anchor=N)

    editar_senha = CTkEntry(editar_frame, width=250, placeholder_text="Digite a senha atual", show="*")
    editar_senha.place_configure(relx=0.5, rely=0.40, anchor=N)

    nova_senha = CTkEntry(editar_frame, width=250, placeholder_text="Digite a nova senha", show="*")
    nova_senha.place_configure(relx=0.5, rely=0.55, anchor=N)
    nova_senha.visible = False

    def editar_():
        name = editar_entrada.get()
        senha_atual = editar_senha.get()
        nova_senha_texto = nova_senha.get()

        nome_pasta_usuario = os.path.join("users", logged_in_username)
        caminho_arquivo_senha = os.path.join(nome_pasta_usuario, f'keys_{logged_in_username}.txt')

        with open(caminho_arquivo_senha, 'r') as arquivo:
            linhas = arquivo.readlines()

        senha_modificada = False
        with open(caminho_arquivo_senha, 'w') as arquivo:
            for linha in linhas:
                chave, valor = linha.strip().split(":")
                if chave == name and valor == senha_atual:
                    arquivo.write(f"{name}:{nova_senha_texto}\n")
                    senha_modificada = True        
                    # Limpando os campos
                    clear_field(editar_entrada, editar_senha, nova_senha)
                else:
                    arquivo.write(linha)
                    # Limpando os campos
                    clear_field(editar_entrada, editar_senha, nova_senha)

        if senha_modificada:
            CTkLabel(editar_frame, text="Senha alterada com sucesso").place_configure(relx=0.5, rely=0.91, anchor=N)
        else:
            CTkLabel(editar_frame, font=font(size=8), text="Senha não encontrada").place_configure(relx=0.5, rely=0.91, anchor=N)

    botao_editar = CTkButton(master=editar_frame, text="Alterar", corner_radius=32, command=editar_)
    botao_editar.place_configure(relx=0.5, rely=0.70, anchor=N)

    help_label = CTkLabel(master=editar_frame, text="Precisa de ajuda?")
    help_label.place_configure(relx=0.5, rely=0.82, anchor=N)


#================================================================================================================================================#

def acessar_GUI():
    destruir_entrada()
    voltar()

    text_central_in_app()

    acessar_frame = CTkFrame(master=app)
    acessar_frame.place_configure(janela_acesso)

    acessar_label = CTkLabel(acessar_frame, text="Insira o nome da senha:")
    acessar_label.place_configure(relx=0.5, rely=0.1, anchor=N)

    acessar_entrada = CTkEntry(acessar_frame, placeholder_text="Digite o nome da senha", width=250)
    acessar_entrada.place_configure(relx=0.5, rely=0.25, anchor=N)

    acessar_senha = CTkEntry(acessar_frame, placeholder_text="Digite a senha", width=250, show="*")
    acessar_senha.place_configure(relx=0.5, rely=0.45, anchor=N)

    def acessar_():
        nome = acessar_entrada.get()
        senha = acessar_senha.get()

        nome_pasta_usuario = os.path.join("users", logged_in_username)
        caminho_arquivo_senha = os.path.join(nome_pasta_usuario, f'keys_{logged_in_username}.txt')

        with open(caminho_arquivo_senha, 'r') as arquivo:
            linhas = arquivo.readlines()

        valor_encontrado = None
        chave_encontrada = False
        novas_linhas = []
        for linha in linhas:
            chave, valor = linha.strip().split(":")
            if chave == nome and logged_in_password == senha:
                chave_encontrada = True
                valor_encontrado = valor

        clear_field(acessar_entrada, acessar_senha)

        if chave_encontrada:
            CTkLabel(acessar_frame, text=f"Senha: {valor_encontrado}").place_configure(relx=0.5, rely=0.5, anchor=N)
        elif not chave_encontrada:
            CTkLabel(acessar_frame, text=f"Senha não encontrada.").place_configure(relx=0.5, rely=0.5, anchor=N)
            acessar_GUI()

    botao_revelar = CTkButton(master=acessar_frame, text="Revelar", corner_radius=32, command=acessar_)
    botao_revelar.place_configure(relx=0.3, rely=0.65, anchor=N)

    botao_apagar  = CTkButton(master=acessar_frame, text="Apagar", corner_radius=32, command=acessar_GUI)
    botao_apagar.place_configure(relx=0.7, rely=0.65, anchor=N)

    help_label = CTkLabel(master=acessar_frame, text="Precisa de ajuda?")
    help_label.place_configure(relx=0.5, rely=0.85, anchor=N)


#================================================================================================================================================#

def inserir_nome():
    destruir_entrada()
    voltar()

    text_central_in_app()

    inserir_frame = CTkFrame(master=app)
    inserir_frame.place_configure(janela_acesso)

    inserir_label = CTkLabel(inserir_frame, text="Inserir nova senha:")
    inserir_label.place_configure(relx=0.5, rely=0.1, anchor=N)

    nome_entrada = CTkEntry(inserir_frame, width=250, placeholder_text="Digite o nome da senha")
    nome_entrada.place_configure(relx=0.5, rely=0.25, anchor=N)

    senha_entrada = CTkEntry(inserir_frame, width=250, placeholder_text="Digite a senha do seu login",show="*")
    senha_entrada.place_configure(relx=0.5, rely=0.40, anchor=N)

    def inserir_():
        nome = nome_entrada.get()
        senha = senha_entrada.get()

        if nome and senha in banco_senhas:
            return CTkLabel(inserir_frame, text="A senha já existe. Use Editar para alterar.").place_configure(relx=0.5, rely=0.7, anchor=N)
        elif nome in banco_senhas: 
            return CTkLabel(inserir_frame, text="Alerta! Existe uma senha com esse nome.").place_configure(relx=0.5, rely=0.7, anchor=N)
        else:
            banco_senhas[nome] = senha 

        caminho_pasta_usuario = os.path.join("users", user())
        caminho_arquivo_senha = os.path.join(caminho_pasta_usuario, f'keys_{user()}.txt')

        CTkLabel(inserir_frame, text="Senha inserida com sucesso!").place_configure(relx=0.5, rely=0.75, anchor=N)

        with open(caminho_arquivo_senha, 'a') as arquivo:
            arquivo.write(f'{nome}:{senha}\n')
            print('Chave adicionada com sucesso')

        inserir_nome()

    botao_inserir = CTkButton(master=inserir_frame, text="Adicionar", corner_radius=32, command=inserir_)
    botao_inserir.place_configure(relx=0.5, rely=0.65, anchor=N)

    help_label = CTkLabel(master=inserir_frame, text="Precisa de ajuda?")
    help_label.place_configure(relx=0.5, rely=0.85, anchor=N)


#================================================================================================================================================#


def voltar():
    clear_window()

    opcoes = ['Inserir', 'Acessar', 'Editar', 'Remover', 'Sair']

    x_position = 0
    y_position = 0

    y_calculo = height/len(opcoes)

    for opcao in opcoes:
        botao = CTkButton(app, text=opcao, width=240, height=120, command=lambda opcao=opcao: selecionar_opcao(opcao), corner_radius=0, hover=True, border_color="black", font=("Arial", 20), bg_color="#242424", fg_color="black")
        botao.place(x=x_position, y=y_position)

        y_position += y_calculo
    text_central = tk.Label(app, text="Gerenciador de Senhas", bg="#242424", fg="white", font=("Helvetica", 16))
    text_central.place_configure(relx=0.65, rely=0.05, anchor=N)


def registrar():
    return inserir_nome()


def login_screen(event=None):
    global logged_in_username, logged_in_password

    def login_(event=None):
        global logged_in_username, logged_in_password
        
        user = login_entrada.get()
        senha = login_password.get()
        
        user_ = user.strip()
        senha_ = senha.strip()

        logged_in_username = user_
        logged_in_password = senha_

        caminho_pasta_usuario = os.path.join("users", user)
        arquivo_senha = os.path.join(caminho_pasta_usuario, f'senha_{user}.txt')

        if os.path.exists(caminho_pasta_usuario):
            
            if verificar_senha(arquivo_senha, senha):
                voltar()
            else:
                CTkLabel(login_frame, text="Usuário ou Senha incorretos!").place_configure(relx=0.5, rely=0.55, anchor=N)

        else:
            user_nao_encontrado = CTkLabel(login_frame, text="Usuário ou Senha incorretos!")
            user_nao_encontrado.place_configure(relx=0.5, rely=0.55, anchor=N)

        return user, senha
    
    
    def verificar_senha(arquivo_senha, senha):
        if os.path.exists(arquivo_senha):
            with open(arquivo_senha, 'r') as arquivo:
                senha_arquivo = arquivo.readline().strip()

                return senha == senha_arquivo
        else:
            return False
    
    clear_window()

    text_central()
    
    login_frame = CTkFrame(master=app)
    login_frame.place_configure(relx=0.5, rely=0.25, anchor=N, width=400, height=300)

    login_label = CTkLabel(login_frame, text="Área de Login:")
    login_label.place_configure(janela_mensagem)

    login_entrada = CTkEntry(login_frame, width=250, placeholder_text="Digite o seu usuário")
    login_entrada.place_configure(relx=0.5, rely=0.25, anchor=N)

    login_password = CTkEntry(login_frame, width=250, placeholder_text="Digite sua senha", show="*")
    login_password.place_configure(relx=0.5, rely=0.45, anchor=N)

    botao_login = CTkButton(login_frame, text="Enviar", corner_radius=32, command=login_)
    botao_login.place_configure(relx=0.5, rely=0.65, anchor=N)

    link_registrar = CTkLabel(login_frame, text="Não tem uma conta? Clique aqui para se registrar!", cursor="hand2")
    link_registrar.place_configure(relx=0.5, rely=0.85, anchor=N)

    link_registrar.bind("<Button-1>", register_screen)


def register_screen(event=None):

    def register(event=None):
        username = register_username_entry.get()
        password = register_password_entry.get()

        if not username or not password:
            erro_register = CTkLabel(register_frame, text="Usuário existe ou algum campo está vazio!")
            erro_register.place_configure(relx=0.5, rely=0.55, anchor=N)
            return
        
        create_user_folder(username, password)
        clear_entry(register_username_entry)
        clear_entry(register_password_entry)
        print("Usuário registrado com sucesso!")

    clear_window()

    text_central()
    register_frame = CTkFrame(app)
    register_frame.place_configure(relx=0.5, rely=0.25, anchor=N, width=400, height=300)

    CTkLabel(register_frame, text="Área de Registro:").place_configure(janela_mensagem)

    register_username_entry = CTkEntry(register_frame, width=250, placeholder_text="Digite o seu usuário")
    register_username_entry.place_configure(relx=0.5, rely=0.25, anchor=N)

    register_password_entry = CTkEntry(register_frame, width=250, placeholder_text="Digite a sua senha", show="*")
    register_password_entry.place_configure(relx=0.5, rely=0.45, anchor=N)

    register_button = CTkButton(register_frame, text="Registrar", corner_radius=32, command=register)
    register_button.place_configure(relx=0.5, rely=0.65, anchor=N)

    register_button_to_login = CTkLabel(register_frame, text="Já tem uma conta? Clique aqui para entrar!", cursor="hand2")
    register_button_to_login.place_configure(relx=0.5, rely=0.85, anchor=N)

    register_button_to_login.bind("<Button-1>", login_screen)


def clear_window():
    for widget in app.winfo_children():
        widget.destroy()


# Iniciando...
app = CTk()
app.title("Gerenciador de Senhas")
app.geometry(f"{width}x{height}")
app._set_appearance_mode("dark")
app.resizable(width=False, height=False)
# BackGround()

register_screen()
login_screen_data = ['Login_User']
position_login_x = 0.5
position_login_y = 0.2

app.mainloop()
