import os
import json
import tkinter as tk

# Permite ou não a visibilidade da senha
def toggle_password_visibility(entry):
    if entry.cget("show") == "*":
        entry.configure(show="")
    else:
        entry.configure(show="*")

# Função para Limpar os campos usados em uma entrada de dados
def clear_camps(*entries):
    for entry in entries:
        entry.delete(0, tk.END)

def clear_window(app):
    for widget in app.winfo_children():
        widget.destroy()

def text_central(app):
    text_central = tk.Label(app,text="Gerenciador de Senhas", fg="white", bg="#5cac9c", font=("Arial", 20, "bold"))
    text_central.pack(pady=20)

def create_user_folder(username, password):
    folder_path = os.path.join("user_database", "users", username)
    
    # Verifica se a pasta do usuário já existe
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        # Se a pasta já existir, retorne um erro ou mensagem apropriada
        raise ValueError("Usuário já registrado")
    
    # Cria o arquivo com a senha do usuário
    password_file_path = os.path.join(folder_path, f"password_{username}.json")
    with open(password_file_path, 'w') as password_file:
        json.dump({"password": password}, password_file)
    
    # Cria o arquivo para armazenar as senhas salvas
    saved_passwords_file_path = os.path.join(folder_path, f"saved_passwords_{username}.json")
    with open(saved_passwords_file_path, 'w') as saved_passwords_file:
        json.dump({"saved_passwords": []}, saved_passwords_file)
    
    return True

def verificar_senha(arquivo_senha, senha):
    if os.path.exists(arquivo_senha):
        with open(arquivo_senha, 'r') as arquivo:
            dados = json.load(arquivo)
            senha_arquivo = dados.get('password', '').strip()
            return senha == senha_arquivo
    return False
