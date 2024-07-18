import os
import json

# FUNÇÃO AUXILIAR PARA VISUALIZAR A SENHA ESCOLHIDA PELO USUÁRIO:
# Esta função busca a senha salva de um usuário específico e a retorna, se encontrada.
# Ela verifica se o arquivo de senhas do usuário existe e, se existir, carrega os dados.
# Em seguida, verifica se a senha solicitada está presente nos dados carregados e a retorna.
# Retorna True e a senha encontrada se a senha existir, caso contrário, retorna False e None.

def to_view_password(user, nome_senha):
    folder_path_user = os.path.join("user_database", "users", user)
    file_path_password = os.path.join(folder_path_user, f"saved_passwords_{user}.json")

    if not os.path.exists(file_path_password):
        return False, None

    with open(file_path_password, 'r') as arquivo:
        data = json.load(arquivo)

    # Verifica se a senha de login está correta
    if nome_senha in data:
        return True, data[nome_senha]
    else:
        return False, None