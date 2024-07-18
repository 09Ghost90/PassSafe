import os
import json

# INSERIR #
def save_insert_password(user, nome_senha, senha_guardada):
    folder_path_user = os.path.join("user_database", "users", user)
    file_path_password = os.path.join(folder_path_user, f"saved_passwords_{user}.json")

    if not os.path.exists(folder_path_user):
        os.makedirs(folder_path_user)

    # Verifica se o Diretório existe e caso não chama recursivamente criando a pasta.
    if not os.path.exists(file_path_password):
        with open(file_path_password, 'w') as file:
            json.dump({nome_senha: senha_guardada}, file, indent=4)
    else:
        with open(file_path_password, 'r') as file:
            data = json.load(file)

        if nome_senha in data:
            raise ValueError
        
        data[nome_senha] = senha_guardada

        with open(file_path_password, 'w') as file:
            json.dump(data, file, indent=4)

    with open(file_path_password, 'a') as file:
        file.write('\n')