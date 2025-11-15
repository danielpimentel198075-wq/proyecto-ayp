# cargador_datos.py

import requests
import json
from Proyecto.modelos import Ingrediente, HotDog

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
        un dict {id: Ingrediente}.
        """
        resp = requests.get(self.url_ingredientes)
        data = resp.json()

        ingredientes = {}
        # TODO: adapta esto a la estructura real del JSON
        for item in data:
            ing = Ingrediente(
                id_=item["id"],
                nombre=item["nombre"],
                categoria=item["categoria"],
                tipo=item["tipo"],
                longitud=item.get("longitud")
            )
            ingredientes[ing.id] = ing

        return ingredientes

    def cargar_menu_desde_api(self, ingredientes):
        """
        Lee el JSON del menú desde GitHub y devuelve
        un dict {id: HotDog} usando el dict de ingredientes.
        """
        resp = requests.get(self.url_menu)
        data = resp.json()

        hotdogs = {}
        # TODO: Aquí usas los IDs de ingredientes que vengan en el JSON de menú
        # para armar los objetos HotDog. Algo tipo:
        #
        # for item in data:
        #     pan = ingredientes[item["id_pan"]]
        #     salchicha = ingredientes[item["id_salchicha"]]
        #     toppings = [ingredientes[id_] for id_ in item["toppings"]]
        #     salsas = [ingredientes[id_] for id_ in item["salsas"]]
        #     ...
        #
        #     hd = HotDog(...)
        #     hotdogs[hd.id] = hd
        #
        return hotdogs

    # Más adelante puedes agregar:
    # - cargar_estado_local()
    # - guardar_estado_local()
