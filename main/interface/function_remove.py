import os
import json
from .functions_aux import verificar_senha

def remove_password_aux(user, name_password, password_confirm):
    # Caminho da Pasta com as Senhas do Usuário (Login e Senha)
    folder_path_user = os.path.join("user_database", "users", user)
    # Caminho do arquivo com as senhas do usuário
    file_path_password = os.path.join(folder_path_user, f"saved_passwords_{user}.json")
    # Caminho do arquivo da senha de Login
    file_path_login_password = os.path.join(folder_path_user, f"password_{user}.json")

    # Verifica se o arquivo com as senhas existe
    if not os.path.exists(file_path_password):
        os.makedirs(folder_path_user)
        raise ValueError("Arquivo de senhas não encontrado")
    
    # Lê o arquivo com as senhas
    with open(file_path_password, "r") as file:
        data = json.load(file)

    if verificar_senha(file_path_login_password, password_confirm):
        found = False
        for key in list(data.keys()):
            if key == name_password:
                del data[key]
                found = True
                break
    else:
       raise ValueError("Senha de Incorreta")

    if not found:
        raise ValueError("Senha atual incorreta ou nome da senha não encontrado")

    # Salvando as mudanças Realizadas
    with open(file_path_password, "w") as file:
        json.dump(data, file, indent=4)

   



