import requests
import json



USERNAME = "FernandoSapient"

REPOSITORY = "BPTSP05_2526-1"
BRANCH = "main"
MENU_PATH = "menu.json"
ING_PATH = "ingredientes.json"

MENU_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{MENU_PATH}"
ING_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{ING_PATH}"


menu_response = requests.get(MENU_URL)
ing_response = requests.get(ING_URL)


if menu_response.status_code == 200 and ing_response.status_code == 200:
 
    menu_data = menu_response.json()
    ing_data = ing_response.json()

   
    print("--- MENU.JSON ---")
    print(json.dumps(menu_data, indent=4))
    print("\n--- INGREDIENTES.JSON ---")
    print(json.dumps(ing_data, indent=4))
else:
    print(f"Error al obtener los datos.")
    print(f"Estado Menú: {menu_response.status_code} (Razón: {menu_response.reason})")
    print(f"Estado Ingredientes: {ing_response.status_code} (Razón: {ing_response.reason})")