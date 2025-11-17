
import requests
import json
from modelos import Ingrediente, HotDog 

class CargadorDatos:
    """
    Se encarga de leer los JSON (remotos y locales) y crear objetos.
    """
    def __init__(self, url_menu, url_ingredientes):
        self.url_menu = url_menu
        self.url_ingredientes = url_ingredientes

    def cargar_ingredientes_desde_api(self):
       
        try:
            resp = requests.get(self.url_ingredientes)
            resp.raise_for_status()
            data_categorias = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fatal al cargar ingredientes desde la API: {e}")
            return {}
        except json.JSONDecodeError:
            print(f"Error fatal: La respuesta de ingredientes no es un JSON válido.")
            return {}

        ingredientes_db = {}
        
        for categoria_data in data_categorias:
            categoria_nombre = categoria_data["Categoria"]
            
            for item in categoria_data["Opciones"]:

                id_ = item["nombre"]
                nombre = item["nombre"]
                
                tipo = item.get("tipo", item.get("base"))
                
                longitud = item.get("tamaño")

                ing = Ingrediente(
                    id_=id_,
                    nombre=nombre,
                    categoria=categoria_nombre,
                    tipo=tipo,
                    longitud=longitud
                )
                ingredientes_db[ing.id] = ing

        return ingredientes_db

    def cargar_menu_desde_api(self, ingredientes_db):
       
        try:
            resp = requests.get(self.url_menu)
            resp.raise_for_status()
            data_menu = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fatal al cargar menú desde la API: {e}")
            return {}
        except json.JSONDecodeError:
            print(f"Error fatal: La respuesta del menú no es un JSON válido.")
            return {}

        hotdogs = {}

        for item in data_menu:
            id_ = item["nombre"]
            nombre = item["nombre"]

            try:

                pan = ingredientes_db[item["Pan"]]
                salchicha = ingredientes_db[item["Salchicha"]]

                toppings = [ingredientes_db[t] for t in item["toppings"]]
                
                lista_salsas_nombres = item.get("salsas", item.get("Salsas", []))
                salsas = [ingredientes_db[s] for s in lista_salsas_nombres]

                acompanante_nombre = item["Acompañante"]
                acompanante = ingredientes_db.get(acompanante_nombre) if acompanante_nombre else None

                
                hd = HotDog(
                    id_=id_,
                    nombre=nombre,
                    pan=pan,
                    salchicha=salchicha,
                    toppings=toppings,
                    salsas=salsas,
                    acompanante=acompanante
                )
                hotdogs[hd.id] = hd

            except KeyError as e:
            
                print(f"Advertencia: No se pudo crear el hot dog '{nombre}'.")
                print(f"Motivo: El ingrediente '{e.args[0]}' no se encuentra en ingredientes.json.")

        return hotdogs