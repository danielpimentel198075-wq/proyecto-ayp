# gestores.py

from modelos import Ingrediente, Inventario, HotDog

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


# (En gestores.py)

class GestorInventario:
    """
    Módulo de Gestión de Inventario.
    """
    def __init__(self, inventario, gestor_ingredientes):
        self.inventario = inventario  # Objeto Inventario
        self.gestor_ingredientes = gestor_ingredientes

    def inicializar_inventario_con_cero(self):
        """
        Asegura que todos los ingredientes de la API existan en el inventario,
        al menos con 0 existencias. No sobrescribe si ya hay un valor.
        """
        todos_los_ing_ids = self.gestor_ingredientes.ingredientes.keys()
        for id_ing in todos_los_ing_ids:
            # Si el ingrediente no está en existencias, lo añade con 0
            if self.inventario.obtener_cantidad(id_ing) == 0 and id_ing not in self.inventario.existencias:
                 self.inventario.set_cantidad(id_ing, 0)

    def buscar_existencia(self, id_ingrediente):
        """
        Devuelve la cantidad de un ingrediente.
        """
        return self.inventario.obtener_cantidad(id_ingrediente)

    def restar_existencia(self, id_ingrediente, cantidad):
        """
        Resta stock de un ingrediente (usado para ventas).
        Devuelve True/False si fue exitoso.
        """
        # Usamos el método de la clase Inventario
        return self.inventario.restar_cantidad(id_ingrediente, cantidad)

    def agregar_existencia(self, id_ingrediente, cantidad):
        """
        Agrega stock a un ingrediente (usado para reponer).
        """
        # Usamos el método de la clase Inventario
        return self.inventario.agregar_cantidad(id_ingrediente, cantidad)
    
    def set_existencia_total(self, id_ingrediente, cantidad):
        """
        Establece el stock total de un ingrediente (usado por el admin).
        Devuelve True/False si fue exitoso (False si el ingrediente no existe).
        """
        # Verificamos que el ingrediente exista en la base de datos
        if not self.gestor_ingredientes.obtener_por_id(id_ingrediente):
            return False
            
        return self.inventario.set_cantidad(id_ingrediente, cantidad)

    def obtener_inventario_completo(self):
        """
        Devuelve una lista de tuplas (Ingrediente, cantidad)
        para todos los ingredientes en el inventario.
        """
        lista_inventario = []
        # Iteramos sobre las existencias {id: cant} del inventario
        for id_ing, cantidad in self.inventario.existencias.items():
            # Buscamos el objeto Ingrediente completo
            ing = self.gestor_ingredientes.obtener_por_id(id_ing)
            if ing:
                lista_inventario.append((ing, cantidad))
        # Ordenamos por categoría y luego por nombre
        lista_inventario.sort(key=lambda item: (item[0].categoria, item[0].nombre))
        return lista_inventario

    def obtener_inventario_bajo_stock(self, umbral=10):
        """
        Devuelve una lista de (Ingrediente, cantidad) para
        items con stock <= umbral.
        """
        lista_bajos = []
        for ing, cantidad in self.obtener_inventario_completo():
            if cantidad <= umbral:
                lista_bajos.append((ing, cantidad))
        return lista_bajos


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
