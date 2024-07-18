import os
import json

def edit_function_aux(user, name_password, password_confirm, new_password):
    folder_path_user = os.path.join("user_database", "users", user)
    file_path_password = os.path.join(folder_path_user, f"saved_passwords_{user}.json")

    # Verifica se o arquivo com as senhas existe
    if not os.path.exists(file_path_password):
        os.makedirs(folder_path_user)
        raise ValueError("Arquivo de senhas não encontrado")
    
    # Lê o arquivo de senhas
    with open(file_path_password, "r") as file:
        data = json.load(file)

    # Procura a senha atual e verifica se está correta
    found = False
    for key, value in data.items():
        if key == name_password and value == password_confirm:
            data[key] = new_password
            found = True
            break

    if not found:
        raise ValueError("Senha atual incorreta ou nome da senha não encontrado")
    
    # Salvando as mudanças feitas
    with open(file_path_password, "w") as file:
        json.dump(data, file, indent=4)
