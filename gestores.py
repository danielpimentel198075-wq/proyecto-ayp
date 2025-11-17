import random
from modelos import Ingrediente, Inventario, HotDog

class GestorIngredientes:
    """
    Módulo de Gestión de Ingredientes.
    Trabaja sobre un dict {id: Ingrediente}.
    """
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes  

    def listar_por_categoria(self, categoria):

        categoria_limpia = categoria.strip().lower() 
        
        return [ing for ing in self.ingredientes.values()
                if ing.categoria.strip().lower() == categoria_limpia]

    def listar_por_categoria_y_tipo(self, categoria, tipo):
        return [ing for ing in self.ingredientes.values()
                if ing.categoria.lower() == categoria.lower()
                and ing.tipo.lower() == tipo.lower()]

    def agregar_ingrediente(self, ingrediente):

        self.ingredientes[ingrediente.id] = ingrediente

    def eliminar_ingrediente(self, id_ingrediente):

        if id_ingrediente in self.ingredientes:
            del self.ingredientes[id_ingrediente]

    def obtener_por_id(self, id_ingrediente):
        return self.ingredientes.get(id_ingrediente)




class GestorInventario:
    """
    Módulo de Gestión de Inventario.
    """
    def __init__(self, inventario, gestor_ingredientes):
        self.inventario = inventario 
        self.gestor_ingredientes = gestor_ingredientes

    def inicializar_inventario_con_cero(self):
        """
        Asegura que todos los ingredientes de la API existan en el inventario,
        al menos con 0 existencias. No sobrescribe si ya hay un valor.
        """
        todos_los_ing_ids = self.gestor_ingredientes.ingredientes.keys()
        for id_ing in todos_los_ing_ids:
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

        return self.inventario.restar_cantidad(id_ingrediente, cantidad)

    def agregar_existencia(self, id_ingrediente, cantidad):
        """
        Agrega stock a un ingrediente (usado para reponer).
        """

        return self.inventario.agregar_cantidad(id_ingrediente, cantidad)
    
    def set_existencia_total(self, id_ingrediente, cantidad):
        """
        Establece el stock total de un ingrediente (usado por el admin).
        Devuelve True/False si fue exitoso (False si el ingrediente no existe).
        """
        
        if not self.gestor_ingredientes.obtener_por_id(id_ingrediente):
            return False
            
        return self.inventario.set_cantidad(id_ingrediente, cantidad)

    def obtener_inventario_completo(self):
        """
        Devuelve una lista de tuplas (Ingrediente, cantidad)
        para todos los ingredientes en el inventario.
        """
        lista_inventario = []

        for id_ing, cantidad in self.inventario.existencias.items():

            ing = self.gestor_ingredientes.obtener_por_id(id_ing)
            if ing:
                lista_inventario.append((ing, cantidad))

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
    Módulo de Gestión del Menú de Hot Dogs.
    """
    def __init__(self, gestor_ingredientes, gestor_inventario):
        self.gestor_ingredientes = gestor_ingredientes
        self.gestor_inventario = gestor_inventario
        self.hotdogs = {}  

    def validar_hotdog(self, hotdog):
        """
        Valida un hot dog según las reglas del negocio.
        Devuelve (True, "OK") o (False, "Mensaje de error").
        """

        if hotdog.pan.longitud is None or hotdog.salchicha.longitud is None:
            return (False, f"El pan '{hotdog.pan.nombre}' o la salchicha '{hotdog.salchicha.nombre}' no tienen una longitud definida.")


        if hotdog.pan.longitud < hotdog.salchicha.longitud:
            return (False, f"Error: El pan ({hotdog.pan.longitud}p) es más corto que la salchicha ({hotdog.salchicha.longitud}p).")


        for ing in hotdog.ingredientes_totales():
            if not self.gestor_ingredientes.obtener_por_id(ing.id):
                return (False, f"El ingrediente '{ing.id}' no existe.")
        
        return (True, "Hot dog válido.")

    def agregar_hotdog(self, hotdog):
        """
        Agrega un nuevo hot dog al menú después de validarlo.
        Devuelve (True, "OK") o (False, "Mensaje de error").
        """
        
        if hotdog.id in self.hotdogs:
            return (False, f"Error: Ya existe un hot dog con el nombre (ID) '{hotdog.id}'.")

        
        es_valido, mensaje = self.validar_hotdog(hotdog)
        if not es_valido:
            return (False, mensaje)

       
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
                
                return (False, ing) 
        return (True, None) 



class SimuladorVentas:
    """
    Módulo de simulación de un día de ventas.
    """
    def __init__(self, gestor_menu, gestor_inventario):
        self.gestor_menu = gestor_menu
        self.gestor_inventario = gestor_inventario
        self.estadisticas = {} 

    def simular_dia(self, num_clientes):
        """
        Implementa el algoritmo de simulación.
        Recibe el número de clientes (N) y devuelve un reporte.
        """

        self.estadisticas = {
            "ventas_exitosas": 0,
            "ventas_fallidas_stock": 0,
            "ventas_fallidas_validez": 0,
            "hotdogs_vendidos": {}, 
            "ingredientes_faltantes": {} 
        }

        lista_hotdogs_menu = self.gestor_menu.listar_hotdogs()

        if not lista_hotdogs_menu:
            print("Error de simulación: No hay hot dogs en el menú.")
            return None

        for _ in range(num_clientes):
            
            hotdog_elegido = random.choice(lista_hotdogs_menu)
            hd_nombre = hotdog_elegido.nombre

            es_valido, _ = self.gestor_menu.validar_hotdog(hotdog_elegido)
            if not es_valido:
                self.estadisticas["ventas_fallidas_validez"] += 1
                continue 

           
            hay_stock, ing_faltante = self.gestor_menu.hay_inventario_para_hotdog(hotdog_elegido)
            
            if hay_stock:
                
                for ing in hotdog_elegido.ingredientes_totales():
                    
                    self.gestor_inventario.restar_existencia(ing.id, 1) 
                
                self.estadisticas["ventas_exitosas"] += 1
                self.estadisticas["hotdogs_vendidos"][hd_nombre] = self.estadisticas["hotdogs_vendidos"].get(hd_nombre, 0) + 1
            
            else:
               
                self.estadisticas["ventas_fallidas_stock"] += 1
                
                if ing_faltante:
                    self.estadisticas["ingredientes_faltantes"][ing_faltante.nombre] = self.estadisticas["ingredientes_faltantes"].get(ing_faltante.nombre, 0) + 1

        return self.estadisticas