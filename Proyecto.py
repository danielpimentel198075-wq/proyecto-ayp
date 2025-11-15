import requests
import json

# 1. Construct the Raw Content URL
# Replace these placeholders with your actual details

USERNAME = "FernandoSapient"
REPOSITORY = "BTPSD05_2526-1"
BRANCH = "main"  # or "master" or another branch name
MENU_PATH = "menu.json"
ING_PATH = "ingredientes.json"

# Construimos las URLs para acceder a los archivos JSON del repositorio
MENU_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{MENU_PATH}"
ING_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{ING_PATH}"

# Solicitamos los archivos desde GitHub
menu_response = requests.get(MENU_URL)
ing_response = requests.get(ING_URL)

# Convertimos las respuestas a formato JSON
menu_data = menu_response.json()
ing_data = ing_response.json()

# Mostramos el contenido de ambos archivos de manera legible
print(json.dumps(menu_data, indent=4))
print(json.dumps(ing_data, indent=4))
