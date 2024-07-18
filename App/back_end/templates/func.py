# Correção do script
import webbrowser
import os

file_index = os.path.join("..","index.html")
file_path = os.path.abspath(file_index)

webbrowser.open(file_path)

