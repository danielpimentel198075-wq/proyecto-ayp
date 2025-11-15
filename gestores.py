# gestores.py

from Proyecto.modelos import Ingrediente, Inventario, HotDog

class GestorIngredientes:
    """
    Módulo de Gestión de Ingredientes.
    Trabaja sobre un dict {id: Ingrediente}.
    """
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes  # dict

    def listar_por_categoria(self, categoria):
        return [ing for ing in self.ingredientes.values()
                if ing.categoria.lower() == categoria.lower()]

    def listar_por_categoria_y_tipo(self, categoria, tipo):
        return [ing for ing in self.ingredientes.values()
                if ing.categoria.lower() == categoria.lower()
                and ing.tipo.lower() == tipo.lower()]

    def agregar_ingrediente(self, ingrediente):
        # TODO: validaciones (no repetir id, etc.)
        self.ingredientes[ingrediente.id] = ingrediente

    def eliminar_ingrediente(self, id_ingrediente):
        # TODO: aquí luego debes verificar si se usa en algún hot dog
        if id_ingrediente in self.ingredientes:
            del self.ingredientes[id_ingrediente]

    def obtener_por_id(self, id_ingrediente):
        return self.ingredientes.get(id_ingrediente)


class GestorInventario:
    """
    Módulo de Gestión de Inventario.
    """
    def __init__(self, inventario, gestor_ingredientes):
        self.inventario = inventario                # objeto Inventario
        self.gestor_ingredientes = gestor_ingredientes  # para validar ids

    def ver_todo(self):
        """
        Devuelve lista de tuplas (Ingrediente, cantidad).
        """
        resultado = []
        for id_ing, cant in self.inventario.existencias.items():
            ing = self.gestor_ingredientes.obtener_por_id(id_ing)
            resultado.append((ing, cant))
        return resultado

    def buscar_existencia(self, id_ingrediente):
        return self.inventario.obtener_cantidad(id_ingrediente)

    def actualizar_existencia(self, id_ingrediente, nueva_cantidad):
        # TODO: validar que el ingrediente exista
        if self.gestor_ingredientes.obtener_por_id(id_ingrediente) is None:
            # aquí luego el Sistema imprimirá un mensaje de error
            return False
        self.inventario.actualizar_cantidad(id_ingrediente, nueva_cantidad)
        return True


class GestorMenu:
    """
    Módulo de Gestión del Menú (hot dogs).
    """
    def __init__(self, gestor_ingredientes, gestor_inventario):
        self.hotdogs = {}  # dict {id: HotDog}
        self.gestor_ingredientes = gestor_ingredientes
        self.gestor_inventario = gestor_inventario

    def agregar_hotdog(self, hotdog):
        # TODO: aquí debes validar:
        # - pan y salchicha existen
        # - longitud pan vs longitud salchicha
        # - toppings/salsas existen
        self.hotdogs[hotdog.id] = hotdog

    def eliminar_hotdog(self, id_hotdog):
        # TODO: validar condiciones según el enunciado (tema inventario)
        if id_hotdog in self.hotdogs:
            del self.hotdogs[id_hotdog]

    def listar_hotdogs(self):
        return list(self.hotdogs.values())

    def hay_inventario_para_hotdog(self, hotdog):
        """
        Revisa si hay al menos 1 unidad de cada ingrediente del hot dog.
        """
        for ing in hotdog.ingredientes_totales():
            if self.gestor_inventario.buscar_existencia(ing.id) <= 0:
                return False
        return True


class SimuladorVentas:
    """
    Módulo de simulación de un día de ventas.
    """
    def __init__(self, gestor_menu, gestor_inventario):
        self.gestor_menu = gestor_menu
        self.gestor_inventario = gestor_inventario
        # aquí luego puedes tener estructuras para guardar estadísticas

    def simular_dia(self):
        """
        Implementa el algoritmo del PDF:
        - clientes aleatorios
        - hot dogs aleatorios
        - verificar inventario
        - actualizar inventario
        - registrar ventas
        """
        # TODO: usar random, recorrer clientes, imprimir resultados, guardar estadísticas
        pass
