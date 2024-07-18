import os
import tkinter as tk
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkFont
from .functions_aux import clear_window, create_user_folder, verificar_senha, clear_camps, toggle_password_visibility

from .function_insert import save_insert_password
from .function_edit import edit_function_aux
from .function_acess import to_view_password
from .function_remove import remove_password_aux

# Abrindo o site do Git - Facebook - Instagram
from .social_media import open_facebook, open_instagram, openmygithub

# Import que permite adicionar imagens
from PIL import Image, ImageTk, ImageOps

# Configuração para janelas de opções:
JANELA_ACESSO = {'relx': 0.5, 'rely': 0.25, 'anchor': tk.N}
TITLE_LABEL = {'relx': 0.5, 'rely': 0.1, 'anchor': tk.N}
FIRST_ENTRY_LABEL = {'relx': 0.5, 'rely': 0.25, 'anchor': tk.N}
SECOND_ENTRY_LABEL = {'relx': 0.5, 'rely': 0.45, 'anchor': tk.N}
THIRD_ENTRY_LABEL = {'relx': 0.5, 'rely': 0.65, 'anchor': tk.N}

BUTTON = {'relx': 0.5, 'rely': 0.75, 'anchor': tk.N}
BUTTON_THIRD = {'relx': 0.5, 'rely': 0.85, 'anchor': tk.N}
LABEL_RESULT = {'relx': 0.5, 'rely': 0.80, 'anchor': tk.N}

# Fonte para Titulos para Frames:
font_title = ('Helvetica', 22, 'bold')

class PasswordManagerApp:

    def __init__(self):
        self.app = CTk()
        self.app.title("Password Manager")
        self.app.geometry("1280x720")
        self.app.configure(bg="white")
        self.app.resizable(width=True, height=True)
        
        # Definindo o ícone da janela
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "../assets/icon_app.ico")
        self.app.iconbitmap(icon_path)
        
    def run(self):
        # THE RUN FUNCTION INITIALIZES WHICH SCREEN SHOULD BE DISPLAYED FIRST.
        self.welcome()
        self.app.mainloop()

    def login_screen(self):
        clear_window(self.app)
        login_frame = CTkFrame(self.app, width=1280, height=720, fg_color="white")
        login_frame.pack_configure(side="left", fill="both", expand=True)

        CTkLabel(login_frame, text="Área de Login:", font=("Arial", 26, "bold"), text_color="#5cac9c").place_configure(relx=0.5, rely=0.1, anchor='n')

        # Carregando a imagem de visibilidade
        script_dir = os.path.dirname(__file__)
        hide_image_path = os.path.join(script_dir, "../assets/hide.png")
        hide_image = Image.open(hide_image_path)
        hide_image = hide_image.resize((20, 20), resample=Image.Resampling.BILINEAR)
        hide_photo = ImageTk.PhotoImage(hide_image)

        login_username_entry = CTkEntry(login_frame, placeholder_text="Digite o usuário", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black")
        login_username_entry.place(relx=0.5, rely=0.25, anchor=tk.N)

        login_password_entry = CTkEntry(login_frame, placeholder_text="Senha", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", show='*')
        login_password_entry.place(relx=0.5, rely=0.35, anchor=tk.N)

        # Adicionando o botão para revelar a senha
        self.show_password_button = CTkButton(login_frame, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(login_password_entry), fg_color="transparent", text="")
        self.show_password_button.place(relx=0.64, rely=0.36, anchor=tk.NE)

        login_button = CTkButton(login_frame, text="ENVIAR", corner_radius=32, text_color="white", fg_color="#5cac9c", width=120, height=40, command=lambda: self.login(login_username_entry, login_password_entry))
        login_button.place(relx=0.5, rely=0.65, anchor=tk.N)

        link_register = CTkLabel(login_frame, text="Não tem uma conta? Clique aqui para se registrar!", cursor="hand2", font=("Arial", 16), text_color="#5cac9c")
        link_register.place(relx=0.5, rely=0.85, anchor=tk.N)
        link_register.bind("<Button-1>", lambda e: self.welcome())

    def login(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        caminho_pasta_user = os.path.join("user_database", "users", username)
        arquivo_senha = os.path.join(caminho_pasta_user, f"password_{username}.json")

        if os.path.exists(caminho_pasta_user):
            if verificar_senha(arquivo_senha, password):
                self.current_user = username
                self.render_options()
            else:
                incorret = CTkLabel(self.app, fg_color="white", text="Usuário ou Senha incorretos!", text_color="red")
                incorret.place(relx=0.5, rely=0.80, anchor=tk.N)
                self.app.after(2000, lambda: incorret.destroy())
        else:
            user_not_found = CTkLabel(self.app, fg_color="white", text="Usuário não existe! ", text_color="red")
            user_not_found.place(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: user_not_found.destroy())

    def render_options(self):
        clear_window(self.app)
        
        self.app.configure(bg="black")

        text_central = tk.Label(self.app, text="Gerenciador de Senhas", fg="#242424", bg="white", font=("Arial", 20, "bold"))
        text_central.place_configure(relx=0.5, rely=0.1, anchor=tk.N)

        logout_frame = CTkFrame(self.app, width=1280, height=720, fg_color="#5cac9c")
        logout_frame.pack_configure(side="top", fill="both", expand=True)

        # Criando Icone e Funcionalidade para o botão em LOGOUT:
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "../assets/logout.png")
        image = Image.open(image_path)
        image = image.resize((60,60))
        photo = ImageTk.PhotoImage(image)
        
        # Criando um botão com a imagem adicionada acima
        button_logout = CTkButton(logout_frame, image=photo, command=self.welcome, width=50, height=50, fg_color="#5cac9c", hover=False, text="")
        button_logout.place_configure(relx=0.05, rely=0.055, anchor=tk.NW)

        # Import para imagem do Inserir:
        script_dir_insert = os.path.dirname(__file__)
        image_path_insert = os.path.join(script_dir_insert, "../assets/inserir_2.png")
        image_insert = Image.open(image_path_insert)
        image_insert = image_insert.resize((120, 120), resample=Image.Resampling.BILINEAR)
        photo_insert = ImageTk.PhotoImage(image_insert)

        font = CTkFont(family="Helvetica", size=24, weight="bold")

        # Criando um botão com a imagem adicionada acima
        inserir_option_frame = CTkButton(self.app, image=photo_insert, corner_radius=False, width=120, height=120, command=lambda:self.inserir(), hover=False, text="", fg_color="#5cac9c")
        inserir_option_frame.place(relx=0.20, rely=0.35, anchor=tk.CENTER)

        # Import para imagem do Acessar:
        script_dir_acessar = os.path.dirname(__file__)
        image_path_acessar = os.path.join(script_dir_acessar, "../assets/acessar_senha.png")
        image_acessar = Image.open(image_path_acessar)
        image_acessar = image_acessar.resize((120, 120), resample=Image.Resampling.BILINEAR)
        photo_acessar = ImageTk.PhotoImage(image_acessar)

        # Criando um botão com a imagem adicionada acima
        acessar_option_frame = CTkButton(self.app, image=photo_acessar, corner_radius=False, width=120, height=120, command=lambda:self.acess(), hover=False, text="", fg_color="#5cac9c", compound="bottom", font=font)
        acessar_option_frame.place(relx=0.50, rely=0.35, anchor=tk.CENTER)

        # Import para imagem do Editar:
        script_dir_editar = os.path.dirname(__file__)
        image_path_editar = os.path.join(script_dir_editar, "../assets/editar_senha.png")
        image_editar = Image.open(image_path_editar)
        image_editar = image_editar.resize((120, 120), resample=Image.Resampling.BILINEAR)
        photo_editar = ImageTk.PhotoImage(image_editar)

        # Criando um botão com a imagem adicionada acima
        editar_option_frame = CTkButton(self.app, image=photo_editar, corner_radius=False, width=120, height=120, command=lambda:self.editar(), hover=False, text="", fg_color="#5cac9c", compound="bottom", font=font)
        editar_option_frame.place(relx=0.80, rely=0.35, anchor=tk.CENTER)


        # Import para imagem do Remover:
        script_dir_remover = os.path.dirname(__file__)
        image_path_remover = os.path.join(script_dir_remover, "../assets/remover_senha.png")
        image_remover = Image.open(image_path_remover)
        image_remover = image_remover.resize((120, 120), resample=Image.Resampling.BILINEAR)
        photo_remover = ImageTk.PhotoImage(image_remover)

        # Criando um botão com a imagem adicionada acima
        remover_option_frame = CTkButton(self.app, image=photo_remover, corner_radius=False, width=120, height=120, command=lambda:self.remover(), hover=False, text="", fg_color="#5cac9c", compound="bottom", font=font)
        remover_option_frame.place(relx=0.33, rely=0.75, anchor=tk.CENTER)

        # Import para imagem do Sair:
        script_dir_sair = os.path.dirname(__file__)
        image_path_sair = os.path.join(script_dir_sair, "../assets/sair.png")
        image_sair = Image.open(image_path_sair)
        image = ImageOps.expand(image, border=1, fill='white')
        image_sair = image_sair.resize((120, 120), resample=Image.Resampling.BILINEAR)
        photo_sair = ImageTk.PhotoImage(image_sair)

        # Criando um botão com a imagem adicionada acima
        sair_option_frame = CTkButton(self.app, image=photo_sair, corner_radius=False, width=120, height=120, command=lambda:self.sair(), hover=False, text="", fg_color="#5cac9c", compound="bottom", font=font)
        sair_option_frame.place(relx=0.66, rely=0.75, anchor=tk.CENTER)
    # Função para Inserir uma senha a ser salva na Aplicação. Tal senha deve ser guardada em saved_password{user}.JSON
    def inserir(self):
        clear_window(self.app)

        # Frame da Tela do Inserir:
        insert_frame = CTkFrame(self.app, width=1280, height=720, fg_color="#5cac9c")
        insert_frame.pack_configure(side="top", fill="both", expand=True)

        # Frame secundário sobrepondo o frame principal
        inser_frame_2 = CTkFrame(insert_frame, width=400, height=360, fg_color="white")
        inser_frame_2.place(relx=0.5, rely=0.25, anchor=tk.N)

        # Botão de Voltar
        button_frame = CTkFrame(self.app, width=40, height=40)
        button_frame.place(relx=0.08, rely=0.08, anchor=tk.NW)

        # Carregando a imagem
        script_dir = os.path.dirname(__file__)
        image_path_back = os.path.join(script_dir, "../assets/return_button.png")
        image_back = Image.open(image_path_back)
        image_back = image_back.resize((40, 40))
        photo_back = ImageTk.PhotoImage(image_back)

        button_back = CTkButton(button_frame, image=photo_back, command=lambda: self.back(), width=50, height=50, fg_color="#5cac9c", hover=False, text="")
        button_back.place_configure(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Carregando a imagem de visibilidade
        hide_image_path = os.path.join(script_dir, "../assets/hide.png")
        hide_image = Image.open(hide_image_path)
        hide_image = hide_image.resize((20, 20), resample=Image.Resampling.BILINEAR)
        hide_photo = ImageTk.PhotoImage(hide_image)

        insert_label = CTkLabel(inser_frame_2, text="Inserir nova senha:", font=font_title, text_color="#5cac9c")
        insert_label.place(relx=0.5, rely=0.1, anchor='n')

        name_password = CTkEntry(inser_frame_2, placeholder_text="Digite o nome da senha", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        name_password.place_configure(FIRST_ENTRY_LABEL)

        password_insert = CTkEntry(inser_frame_2, placeholder_text="Digite a senha a ser guardada", width=280, height=40, corner_radius=10, show="*", fg_color="transparent", text_color="black", border_color="#d3d3d3")
        password_insert.place_configure(SECOND_ENTRY_LABEL)

        # Adicionando o botão para revelar a senha
        self.show_password_button = CTkButton(inser_frame_2, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(password_insert), fg_color="white", text="")
        self.show_password_button.place(relx=0.94, rely=0.47, anchor=tk.NE)

        password_confirm = CTkEntry(inser_frame_2, width=280, height=40, placeholder_text="Digite a senha do seu login", show="*", corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        password_confirm.place_configure(THIRD_ENTRY_LABEL)

        # Adicionando o botão para revelar a senha
        self.show_password_button = CTkButton(inser_frame_2, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(password_confirm), fg_color="white", text="")
        self.show_password_button.place(relx=0.94, rely=0.67, anchor=tk.NE)

        save_button = CTkButton(inser_frame_2, text="Salvar", width=120, height=40,  corner_radius=32, text_color="white", fg_color="#5cac9c", hover=False, command=lambda: self.salvar_senha(name_password, password_insert, password_confirm))
        save_button.place_configure(BUTTON_THIRD)

        # Collect User, Password, Confirm Password, and save it to a JSON file

    def salvar_senha(self, name_password, password_insert, password_confirm):
        user = self.current_user
        nome_senha = name_password.get()
        senha_guardada = password_insert.get()
        senha_login = password_confirm.get()

        caminho_pasta_user = os.path.join("user_database", "users", user)
        arquivo_senha = os.path.join(caminho_pasta_user, f"password_{user}.json")

        if not verificar_senha(arquivo_senha, senha_login):
            error_label = CTkLabel(self.app, text="Senha de Login incorreta!", bg_color="#5cac9c", text_color="red")
            error_label.place(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: error_label.destroy())
            return
        
        try:
            save_insert_password(user, nome_senha, senha_guardada)
            success_label = CTkLabel(self.app, text="Senha salva com sucesso!", bg_color="#5cac9c", text_color="green")
            success_label.place(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: success_label.destroy())

        except ValueError as e:
            error_label = CTkLabel(self.app, text=str(e), bg_color="#5cac9c", text_color="red")
            error_label.place(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: error_label.destroy())

        clear_camps(name_password, password_insert, password_confirm)

    def acess(self):
        clear_window(self.app)

        # Frame da Tela de Acesso:
        acess_frame = CTkFrame(self.app, width=1280, height=720, fg_color="#5cac9c")
        acess_frame.pack_configure(side="top", fill="both", expand=True)

        # Frame secundário sobrepondo o frame principal
        acess_frame_2 = CTkFrame(acess_frame, width=400, height=380, fg_color="white")
        acess_frame_2.place_configure(JANELA_ACESSO)

        # Botão de Voltar
        button_frame = CTkFrame(self.app, width=40, height=40)
        button_frame.place(relx=0.08, rely=0.08, anchor=tk.NW)

        # Carregando a imagem
        script_dir = os.path.dirname(__file__)
        image_path_back = os.path.join(script_dir, "../assets/return_button.png")
        image_back = Image.open(image_path_back)
        image_back = image_back.resize((40, 40))
        photo_back = ImageTk.PhotoImage(image_back)

        button_back = CTkButton(button_frame, image = photo_back, command=lambda: self.back(), width=50, height=50, fg_color="#5cac9c", hover=False, text="")
        button_back.place_configure(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Carregando a imagem de visibilidade
        script_dir = os.path.dirname(__file__)
        hide_image_path = os.path.join(script_dir, "../assets/hide.png")
        hide_image = Image.open(hide_image_path)
        hide_image = hide_image.resize((20, 20), resample=Image.Resampling.BILINEAR)
        hide_photo = ImageTk.PhotoImage(hide_image)

        acess_label = CTkLabel(acess_frame_2, text="Acessar senha:", font=font_title, text_color="#5cac9c")
        acess_label.place_configure(TITLE_LABEL)

        acess_entry = CTkEntry(acess_frame_2, placeholder_text="Digite o nome da senha", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        acess_entry.place_configure(FIRST_ENTRY_LABEL)

        password_acess = CTkEntry(acess_frame_2, width=280, height=40, placeholder_text="Digite a senha do seu login", show="*", corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        password_acess.place_configure(SECOND_ENTRY_LABEL)

        # Adicionando o botão para revelar a senha
        self.show_password_button = CTkButton(acess_frame_2, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(password_acess), fg_color="white", text="")
        self.show_password_button.place(relx=0.94, rely=0.47, anchor=tk.NE)

        save_button = CTkButton(acess_frame_2, text="Vizualizar", width=120, height=40, text_color="white", fg_color="#5cac9c", corner_radius=32, command=lambda: self.view_password(acess_entry, password_acess))
        save_button.place_configure(BUTTON)

    def view_password(self, acess_entry, password_acess):
        user = self.current_user  # Coleta o nome do usuário
        nome_senha = acess_entry.get()  # Coleta o nome da senha a ser acessada
        senha_login = password_acess.get()  # Confirma se a senha de Login está correta uma forma de segurança

        caminho_pasta_user = os.path.join("user_database", "users", user)
        arquivo_senha_login = os.path.join(caminho_pasta_user, f"password_{user}.json")

        if os.path.exists(caminho_pasta_user):
            if verificar_senha(arquivo_senha_login, senha_login):
                sucesso, valor_senha = to_view_password(user, nome_senha)
                if sucesso:
                    success_label = CTkLabel(self.app, text=f"Senha encontrada: {valor_senha}", bg_color="#5cac9c", text_color="white", font=font_title)
                    success_label.place_configure(LABEL_RESULT)
                    self.app.after(2000, lambda: success_label.destroy())
                else:
                    error_label = CTkLabel(self.app, text="Senha não encontrada.", bg_color="#5cac9c", text_color="red")
                    error_label.place_configure(LABEL_RESULT)
                    self.app.after(2000, lambda: error_label.destroy())
            else:
                error_label = CTkLabel(self.app, text="Senha de Login incorreta!", bg_color="#5cac9c", text_color="red")
                error_label.place_configure(LABEL_RESULT)
                self.app.after(2000, lambda: error_label.destroy())
        else:
            error_label = CTkLabel(self.app, text="Usuário não encontrado!")
            error_label.place(relx=0.5, rely=0.55, anchor=tk.N)
            self.app.after(2000, lambda: error_label.destroy())

        clear_camps(acess_entry, password_acess)

    def editar(self):
        clear_window(self.app)

        # Frame da Tela de Acesso:
        acess_frame = CTkFrame(self.app, width=1280, height=720, fg_color="#5cac9c")
        acess_frame.pack_configure(side="top", fill="both", expand=True)

        # Frame secundário sobrepondo o frame principal
        acess_frame_2 = CTkFrame(acess_frame, width=400, height=380, fg_color="white")
        acess_frame_2.place_configure(JANELA_ACESSO)

        # Botão de Voltar
        button_frame = CTkFrame(self.app, width=40, height=40)
        button_frame.place(relx=0.08, rely=0.08, anchor=tk.NW)

        # Carregando a imagem
        script_dir = os.path.dirname(__file__)
        image_path_back = os.path.join(script_dir, "../assets/return_button.png")
        image_back = Image.open(image_path_back)
        image_back = image_back.resize((40, 40))
        photo_back = ImageTk.PhotoImage(image_back)

        button_back = CTkButton(button_frame, image = photo_back, command=lambda: self.back(), width=50, height=50, fg_color="#5cac9c", hover=False, text="")
        button_back.place_configure(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Carregando a imagem de visibilidade
        script_dir = os.path.dirname(__file__)
        hide_image_path = os.path.join(script_dir, "../assets/hide.png")
        hide_image = Image.open(hide_image_path)
        hide_image = hide_image.resize((20, 20), resample=Image.Resampling.BILINEAR)
        hide_photo = ImageTk.PhotoImage(hide_image)

        edit_label = CTkLabel(acess_frame_2, text="Editar senha:", font=font_title, text_color="#5cac9c")
        edit_label.place_configure(TITLE_LABEL)

        name_password = CTkEntry(acess_frame_2, placeholder_text="Digite a senha a editar", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        name_password.place_configure(FIRST_ENTRY_LABEL)

        password_confirm = CTkEntry(acess_frame_2, placeholder_text="Digite a senha atual", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3", show="*")
        password_confirm.place_configure(SECOND_ENTRY_LABEL)

        new_password = CTkEntry(acess_frame_2, placeholder_text="Digite a nova senha", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3", show="*")
        new_password.place_configure(THIRD_ENTRY_LABEL)

        # Adicionando o botão para revelar a senha
        self.show_password_button = CTkButton(acess_frame_2, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(password_confirm), fg_color="white", text="")
        self.show_password_button.place(relx=0.94, rely=0.47, anchor=tk.NE)

        self.show_password_button = CTkButton(acess_frame_2, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(new_password), fg_color="white", text="")
        self.show_password_button.place(relx=0.94, rely=0.67, anchor=tk.NE)

        # Adicionando o botão para revelar a senha (Editar)
        edit_button_confirm = CTkButton(acess_frame_2, text="Alterar", width=120, height=40, text_color="white", fg_color="#5cac9c", corner_radius=32, command=lambda: self.edit_function(name_password, password_confirm, new_password))
        edit_button_confirm.place_configure(BUTTON_THIRD)

    def edit_function(self, name_password, password_confirm, new_password):
        user = self.current_user
        name_password_value = name_password.get()
        password_confirm_value = password_confirm.get()
        new_password_value = new_password.get()

        try:
            edit_function_aux(user, name_password_value, password_confirm_value, new_password_value)
            sucess_label = CTkLabel(self.app, text="Senha alterada com sucesso!", bg_color="#5cac9c", text_color="green", font=font_title)
            sucess_label.place_configure(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: sucess_label.destroy())

        except ValueError as e:
            error_label = CTkLabel(self.app, text=str(e), bg_color="#5cac9c", text_color="red")
            error_label.place(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: error_label.destroy())

        clear_camps(name_password, password_confirm, new_password)

    def remover(self):
        clear_window(self.app)
        
        # Frame da Tela de Acesso:
        acess_frame = CTkFrame(self.app, width=1280, height=720, fg_color="#5cac9c")
        acess_frame.pack_configure(side="top", fill="both", expand=True)

        # Frame secundário sobrepondo o frame principal
        acess_frame_2 = CTkFrame(acess_frame, width=400, height=380, fg_color="white")
        acess_frame_2.place_configure(JANELA_ACESSO)

        # Botão de Voltar
        button_frame = CTkFrame(self.app, width=40, height=40)
        button_frame.place(relx=0.08, rely=0.08, anchor=tk.NW)

        # Carregando a imagem
        script_dir = os.path.dirname(__file__)
        image_path_back = os.path.join(script_dir, "../assets/return_button.png")
        image_back = Image.open(image_path_back)
        image_back = image_back.resize((40, 40))
        photo_back = ImageTk.PhotoImage(image_back)

        button_back = CTkButton(button_frame, image = photo_back, command=lambda: self.back(), width=50, height=50, fg_color="#5cac9c", hover=False, text="")
        button_back.place_configure(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Carregando a imagem de visibilidade
        script_dir = os.path.dirname(__file__)
        hide_image_path = os.path.join(script_dir, "../assets/hide.png")
        hide_image = Image.open(hide_image_path)
        hide_image = hide_image.resize((20, 20), resample=Image.Resampling.BILINEAR)
        hide_photo = ImageTk.PhotoImage(hide_image)

        remove_Title = CTkLabel(acess_frame_2, text="Remover senha:", font=font_title, text_color="#5cac9c")
        remove_Title.place_configure(TITLE_LABEL)

        name_password = CTkEntry(acess_frame_2, placeholder_text="Digite o nome da senha", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        name_password.place_configure(FIRST_ENTRY_LABEL)

        password_confirm = CTkEntry(acess_frame_2, placeholder_text="Digite a senha de login", show="*", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black", border_color="#d3d3d3")
        password_confirm.place_configure(SECOND_ENTRY_LABEL)

        # Adicionando o botão para apagar
        self.show_password_button = CTkButton(acess_frame_2, image=hide_photo, width=20, height=20, hover=False, command=lambda: toggle_password_visibility(password_confirm), fg_color="white", text="")
        self.show_password_button.place(relx=0.94, rely=0.47, anchor=tk.NE)

        remove_button = CTkButton(acess_frame_2, text="Remover", width=120, height=40, text_color="white", fg_color="#5cac9c", corner_radius=32, command=lambda: self.remove_password(name_password, password_confirm))
        remove_button.place_configure(BUTTON)

    def remove_password(self, name_password, password_confirm):
        user = self.current_user
        name_password_value = name_password.get()
        password_confirm_value = password_confirm.get()

        try:
            remove_password_aux(user, name_password_value, password_confirm_value)
            success_label = CTkLabel(self.app, text="Senha removida com sucesso!", bg_color="#5cac9c", text_color="green")
            success_label.place_configure(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: success_label.destroy())

        except ValueError as e:
            error_label = CTkLabel(self.app, text=str(e), bg_color="#5cac9c", text_color="red")
            error_label.place(relx=0.5, rely=0.80, anchor=tk.N)
            self.app.after(2000, lambda: error_label.destroy())

        clear_camps(name_password, password_confirm)

    def sair(self):
        self.app.quit()

    def back(self):
        self.render_options()

    def welcome(self):
        clear_window(self.app)

        # Carregando a imagem de visibilidade
        script_dir = os.path.dirname(__file__)
        hide_image_path = os.path.join(script_dir, "../assets/hide.png")
        hide_image = Image.open(hide_image_path)
        hide_image = hide_image.resize((20, 20), resample=Image.Resampling.BILINEAR)
        hide_photo = ImageTk.PhotoImage(hide_image)

        # Carregando a imagem do Facebook
        facebook_image_path = os.path.join(script_dir, "../assets/facebook.png")
        facebook_image = Image.open(facebook_image_path)
        facebook_image = facebook_image.resize((40, 40), resample=Image.Resampling.BILINEAR)
        photo_facebook = ImageTk.PhotoImage(facebook_image)

        # Carregando a imagem do Instagram
        instagram_image_path = os.path.join(script_dir, "../assets/instagram.png")
        instagram_image = Image.open(instagram_image_path)
        instagram_image = instagram_image.resize((40, 40), resample=Image.Resampling.BILINEAR)
        photo_instagram = ImageTk.PhotoImage(instagram_image)

        # Carregando a imagem do GitHub
        github_image_path = os.path.join(script_dir, "../assets/github.png")
        github_image = Image.open(github_image_path)
        github_image = github_image.resize((40, 40), resample=Image.Resampling.BILINEAR)
        photo_github = ImageTk.PhotoImage(github_image)

        # Criando dois frames:
        left_frame = CTkFrame(self.app, width=380, height=380, fg_color="#5cac9c", corner_radius=False)
        left_frame.pack(side="left", fill="both", expand=True)

        right_frame = CTkFrame(self.app, width=400, height=380, fg_color="white", corner_radius=False)
        right_frame.pack(side="right", fill="both", expand=True)

        # Conteúdo do left_frame
        welcome_label = CTkLabel(left_frame, text="Seja Bem-Vindo de Volta!", font=("Arial", 26, "bold"), text_color="white")
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        sub_label_welcome = CTkLabel(left_frame, text="Para continuar, faça login com sua conta", font=("Arial", 16), text_color="white")
        sub_label_welcome.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        button_login = CTkButton(left_frame, text="ENTRAR", corner_radius=32, command=self.login_screen, width=120, height=40, text_color="#5cac9c", fg_color="white", hover_color="white")
        button_login.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Conteúdo do right_frame
        create_label = CTkLabel(right_frame, text="Criar Conta", font=("Arial", 26, "bold"), text_color="#5cac9c")
        create_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        social_media_frame = CTkFrame(right_frame, fg_color="transparent")
        social_media_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        button_facebook = CTkButton(social_media_frame, image=photo_facebook, text="", width=40, height=40, corner_radius=20, text_color="#5cac9c", fg_color="white", hover=False, command=lambda: open_facebook())
        button_facebook.grid(row=0, column=0, padx=5)

        button_instagram = CTkButton(social_media_frame, image=photo_instagram, text="", width=40, height=40, corner_radius=20, text_color="#5cac9c", fg_color="white", hover=False, command=lambda: open_instagram())
        button_instagram.grid(row=0, column=1, padx=5)

        button_github = CTkButton(social_media_frame, image=photo_github, text="", width=40, height=40, corner_radius=20, text_color="#5cac9c", fg_color="white", hover=False, command=lambda: openmygithub())
        button_github.grid(row=0, column=2, padx=5)

        or_label = CTkLabel(right_frame, text="ou use seu email para registrar:", font=("Arial", 16), text_color="#5cac9c")
        or_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        register_entry_name = CTkEntry(right_frame, placeholder_text="Nome", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black")
        register_entry_name.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        register_entry_email = CTkEntry(right_frame, placeholder_text="Email", width=280, height=40, corner_radius=10, fg_color="transparent", text_color="black")
        register_entry_email.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        register_entry_password = CTkEntry(right_frame, placeholder_text="Senha", width=280, height=40, corner_radius=10, fg_color="transparent", show="*", text_color="black")
        register_entry_password.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Adicionando o botão para revelar a senha
        show_password_button = CTkButton(right_frame, image=hide_photo, width=20, height=20, hover=False, command=lambda:toggle_password_visibility(register_entry_password), fg_color="white", text="")
        show_password_button.place(relx=0.775, rely=0.68, anchor=tk.NE)

        button_signup = CTkButton(right_frame, text="SIGN UP", corner_radius=32, command=lambda: self.register(register_entry_name, register_entry_password), width=120, height=40, text_color="white", fg_color="#5cac9c")
        button_signup.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def register(self, entry_name, entry_password):
        username = entry_name.get()
        password = entry_password.get()
    
        if not username or not password:
            not_found = CTkLabel(self.app, text="Algum campo vazio  ", fg_color="white", text_color="red")
            not_found.place(relx=0.75, rely=0.85, anchor=tk.N)
            self.app.after(2000, lambda: not_found.destroy())
            return
        
        try:
            create_user_folder(username, password)
            success_label = CTkLabel(self.app, text="Usuário Registrado ", fg_color="white", text_color="green")
            success_label.place(relx=0.75, rely=0.85, anchor=tk.N)
            self.app.after(2000, lambda: success_label.destroy())

            clear_camps(entry_name, entry_password)

        except ValueError as e:
            error_label = CTkLabel(self.app, text=str(e), fg_color="white", text_color="green")
            error_label.place(relx=0.75, rely=0.85, anchor=tk.N)
            self.app.after(2000, lambda: error_label.destroy())

            clear_camps(entry_name, entry_password)

def iniciar_app():
    app = PasswordManagerApp()
    app.run()