# gestores.py
import random
from modelos import Ingrediente, Inventario, HotDog

class GestorIngredientes:
    """
    Módulo de Gestión de Ingredientes.
    Trabaja sobre un dict {id: Ingrediente}.
    """
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes  # dict

    def listar_por_categoria(self, categoria):
        # Limpiamos el input del usuario (con .strip()) antes de comparar
        categoria_limpia = categoria.strip().lower() 
        
        return [ing for ing in self.ingredientes.values()
                if ing.categoria.strip().lower() == categoria_limpia]

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


# (En gestores.py)

class GestorMenu:
    """
    Módulo de Gestión del Menú de Hot Dogs.
    """
    def __init__(self, gestor_ingredientes, gestor_inventario):
        self.gestor_ingredientes = gestor_ingredientes
        self.gestor_inventario = gestor_inventario
        self.hotdogs = {}  # dict {id: HotDog}

    def validar_hotdog(self, hotdog):
        """
        Valida un hot dog según las reglas del negocio.
        Devuelve (True, "OK") o (False, "Mensaje de error").
        """
        # 1. Validar que el Pan y la Salchicha tienen longitud
        if hotdog.pan.longitud is None or hotdog.salchicha.longitud is None:
            return (False, f"El pan '{hotdog.pan.nombre}' o la salchicha '{hotdog.salchicha.nombre}' no tienen una longitud definida.")

        # 2. Validar longitud Pan vs Salchicha (Regla del PDF)
        if hotdog.pan.longitud < hotdog.salchicha.longitud:
            return (False, f"Error: El pan ({hotdog.pan.longitud}p) es más corto que la salchicha ({hotdog.salchicha.longitud}p).")

        # 3. Validar que los ingredientes existen (aunque si los creamos bien, ya existen)
        for ing in hotdog.ingredientes_totales():
            if not self.gestor_ingredientes.obtener_por_id(ing.id):
                return (False, f"El ingrediente '{ing.id}' no existe.")
        
        return (True, "Hot dog válido.")

    def agregar_hotdog(self, hotdog):
        """
        Agrega un nuevo hot dog al menú después de validarlo.
        Devuelve (True, "OK") o (False, "Mensaje de error").
        """
        # 1. Validar si el ID (nombre) ya existe
        if hotdog.id in self.hotdogs:
            return (False, f"Error: Ya existe un hot dog con el nombre (ID) '{hotdog.id}'.")

        # 2. Validar reglas de negocio (longitud, etc.)
        es_valido, mensaje = self.validar_hotdog(hotdog)
        if not es_valido:
            return (False, mensaje)

        # 3. Si todo está OK, lo agregamos
        self.hotdogs[hotdog.id] = hotdog
        return (True, "Hot dog agregado exitosamente.")

    def eliminar_hotdog(self, id_hotdog):
        """
        Elimina un hot dog del menú.
        Devuelve True si se eliminó, False si no existía.
        """
        if id_hotdog in self.hotdogs:
            del self.hotdogs[id_hotdog]
            return True
        return False

    def listar_hotdogs(self):
        return list(self.hotdogs.values())

    def obtener_hotdog_por_id(self, id_hotdog):
        return self.hotdogs.get(id_hotdog)

    def hay_inventario_para_hotdog(self, hotdog):
        """
        Revisa si hay al menos 1 unidad de cada ingrediente del hot dog.
        Devuelve (False, Ingrediente_Faltante) si no hay.
        """
        for ing in hotdog.ingredientes_totales():
            if self.gestor_inventario.buscar_existencia(ing.id) <= 0:
                # Devolvemos el ingrediente que falta para un mensaje más claro
                return (False, ing) 
        return (True, None) # Hay inventario


# (En gestores.py)

class SimuladorVentas:
    """
    Módulo de simulación de un día de ventas.
    """
    def __init__(self, gestor_menu, gestor_inventario):
        self.gestor_menu = gestor_menu
        self.gestor_inventario = gestor_inventario
        self.estadisticas = {} # Para el bono

    def simular_dia(self, num_clientes):
        """
        Implementa el algoritmo de simulación.
        Recibe el número de clientes (N) y devuelve un reporte.
        """
        # Reiniciamos las estadísticas para esta simulación
        self.estadisticas = {
            "ventas_exitosas": 0,
            "ventas_fallidas_stock": 0,
            "ventas_fallidas_validez": 0,
            "hotdogs_vendidos": {}, # {"simple": 5, "ingles": 2}
            "ingredientes_faltantes": {} # {"weiner": 3, "ketchup": 8}
        }

        # Obtenemos la lista de hot dogs disponibles UNA SOLA VEZ
        lista_hotdogs_menu = self.gestor_menu.listar_hotdogs()

        if not lista_hotdogs_menu:
            print("Error de simulación: No hay hot dogs en el menú.")
            return None

        # --- Bucle de simulación (N clientes) ---
        for _ in range(num_clientes):
            # 1. Cliente elija un hot dog al azar
            hotdog_elegido = random.choice(lista_hotdogs_menu)
            hd_nombre = hotdog_elegido.nombre

            # 2. Validar reglas de negocio (Pan vs Salchicha)
            es_valido, _ = self.gestor_menu.validar_hotdog(hotdog_elegido)
            if not es_valido:
                self.estadisticas["ventas_fallidas_validez"] += 1
                continue # El cliente se va molesto porque el hot dog no es válido

            # 3. Validar inventario
            hay_stock, ing_faltante = self.gestor_menu.hay_inventario_para_hotdog(hotdog_elegido)
            
            if hay_stock:
                # 4. ¡Venta Exitosa!
                # Restamos 1 de cada ingrediente del inventario
                for ing in hotdog_elegido.ingredientes_totales():
                    # Restar_existencia ya maneja la lógica de restar 1
                    self.gestor_inventario.restar_existencia(ing.id, 1) 
                
                # Actualizar estadísticas de éxito
                self.estadisticas["ventas_exitosas"] += 1
                self.estadisticas["hotdogs_vendidos"][hd_nombre] = self.estadisticas["hotdogs_vendidos"].get(hd_nombre, 0) + 1
            
            else:
                # 5. Venta Fallida (Falta de Stock)
                self.estadisticas["ventas_fallidas_stock"] += 1
                
                # Registramos qué ingrediente faltó
                if ing_faltante:
                    self.estadisticas["ingredientes_faltantes"][ing_faltante.nombre] = self.estadisticas["ingredientes_faltantes"].get(ing_faltante.nombre, 0) + 1

        # 6. Devolver el reporte
        return self.estadisticas