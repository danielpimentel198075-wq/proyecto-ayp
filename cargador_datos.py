# cargador_datos.py

import requests
import json
# Asegúrate que la ruta de importación sea correcta según tu estructura
from modelos import Ingrediente, HotDog 

class CargadorDatos:
    """
    Se encarga de leer los JSON (remotos y locales) y crear objetos.
    """
    def __init__(self, url_menu, url_ingredientes):
        self.url_menu = url_menu
        self.url_ingredientes = url_ingredientes

    def cargar_ingredientes_desde_api(self):
        """
        Lee el JSON de ingredientes desde GitHub y devuelve
        un dict {nombre_ingrediente: Objeto_Ingrediente}.
        """
        try:
            resp = requests.get(self.url_ingredientes)
            resp.raise_for_status() # Lanza un error si la petición falla (ej. 404)
            data_categorias = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fatal al cargar ingredientes desde la API: {e}")
            return {}
        except json.JSONDecodeError:
            print(f"Error fatal: La respuesta de ingredientes no es un JSON válido.")
            return {}

        ingredientes_db = {}
        
        # El JSON es una lista de categorías (Pan, Salchicha, etc.)
        for categoria_data in data_categorias:
            categoria_nombre = categoria_data["Categoria"]
            
            # Iteramos sobre las opciones dentro de esa categoría
            for item in categoria_data["Opciones"]:
                # Usamos el 'nombre' como ID, ya que así viene en el JSON
                id_ = item["nombre"]
                nombre = item["nombre"]
                
                # El 'tipo' varía (a veces es 'tipo', a veces 'base' para salsas)
                tipo = item.get("tipo", item.get("base"))
                
                # La 'longitud' solo existe para Pan y Salchicha (usa 'tamaño')
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
        """
        Lee el JSON del menú desde GitHub y devuelve
        un dict {nombre_hotdog: Objeto_HotDog}.
        
        Usa el 'ingredientes_db' (creado antes) para enlazar 
        los nombres de ingredientes con los objetos Ingrediente.
        """
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

        # El JSON es una lista de hot dogs
        for item in data_menu:
            id_ = item["nombre"]
            nombre = item["nombre"]

            try:
                # 1. Buscamos el OBJETO Ingrediente usando el nombre (string)
                pan = ingredientes_db[item["Pan"]]
                salchicha = ingredientes_db[item["Salchicha"]]

                # 2. Manejamos las listas de toppings y salsas
                # (convertimos lista de strings a lista de Objetos)
                toppings = [ingredientes_db[t] for t in item["toppings"]]
                
                # 3. Manejamos la inconsistencia 'salsas' vs 'Salsas'
                lista_salsas_nombres = item.get("salsas", item.get("Salsas", []))
                salsas = [ingredientes_db[s] for s in lista_salsas_nombres]

                # 4. Manejamos el acompañante (puede ser None/null)
                acompanante_nombre = item["Acompañante"]
                acompanante = ingredientes_db.get(acompanante_nombre) if acompanante_nombre else None

                # 5. Creamos el objeto HotDog
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
                # Este error saltará si menu.json pide un ingrediente 
                # que no existe en ingredientes.json (ej. "Pan": "baguette")
                print(f"Advertencia: No se pudo crear el hot dog '{nombre}'.")
                print(f"Motivo: El ingrediente '{e.args[0]}' no se encuentra en ingredientes.json.")

        return hotdogs