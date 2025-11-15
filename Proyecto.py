import requests
import json

# 1. Construct the Raw Content URL
# Replace these placeholders with your actual details

USERNAME = "FernandoSapient"
# CORRECCIÓN AQUÍ: Era "BTPSD05..."
REPOSITORY = "BPTSP05_2526-1"
BRANCH = "main"
MENU_PATH = "menu.json"
ING_PATH = "ingredientes.json"

# Construimos las URLs para acceder a los archivos JSON del repositorio
MENU_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{MENU_PATH}"
ING_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{ING_PATH}"

# Solicitamos los archivos desde GitHub
menu_response = requests.get(MENU_URL)
ing_response = requests.get(ING_URL)

# Verificamos si la solicitud fue exitosa (código 200)
if menu_response.status_code == 200 and ing_response.status_code == 200:
    # Convertimos las respuestas a formato JSON
    menu_data = menu_response.json()
    ing_data = ing_response.json()

    # Mostramos el contenido de ambos archivos de manera legible
    print("--- MENU.JSON ---")
    print(json.dumps(menu_data, indent=4))
    print("\n--- INGREDIENTES.JSON ---")
    print(json.dumps(ing_data, indent=4))
else:
    print(f"Error al obtener los datos.")
    print(f"Estado Menú: {menu_response.status_code} (Razón: {menu_response.reason})")
    print(f"Estado Ingredientes: {ing_response.status_code} (Razón: {ing_response.reason})")