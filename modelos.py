class Ingrediente:
    """
    Representa un ingrediente (pan, salchicha, topping, salsa, acompañante, etc.).
    """
    def __init__(self, id_, nombre, categoria, tipo, longitud=None):
        self.id = id_
        self.nombre = nombre
        self.categoria = categoria  
        self.tipo = tipo            
        self.longitud = longitud     

    def __str__(self):
        return f"{self.nombre} ({self.categoria}, {self.tipo})"


class HotDog:
    """
    Representa un hot dog del menú.
    """
    def __init__(self, id_, nombre, pan, salchicha, toppings, salsas, acompanante=None):
        self.id = id_
        self.nombre = nombre
        self.pan = pan                  
        self.salchicha = salchicha     
        self.toppings = toppings or []  
        self.salsas = salsas or []     
        self.acompanante = acompanante  

    def ingredientes_totales(self):
        """
        Devuelve todos los ingredientes usados en ese hot dog.
        """
        ingredientes = [self.pan, self.salchicha] + self.toppings + self.salsas
        if self.acompanante is not None:
            ingredientes.append(self.acompanante)
        return ingredientes

    def __str__(self):
        return f"HotDog #{self.id}: {self.nombre}"

    def to_dict(self):
        """
        Convierte el objeto HotDog a un diccionario simple (serializable a JSON),
        usando los 'nombres' (IDs) de los ingredientes.
        """
        return {
            "nombre": self.nombre,
            "Pan": self.pan.id,
            "Salchicha": self.salchicha.id,
            "toppings": [t.id for t in self.toppings],
            "salsas": [s.id for s in self.salsas],
            "Acompañante": self.acompanante.id if self.acompanante else None
        }


class Inventario:
    """
    Maneja las existencias de ingredientes (por id de ingrediente).
    """
    def __init__(self):
        
        self.existencias = {}

    def obtener_cantidad(self, id_ingrediente):
        """
        Devuelve la cantidad de un ingrediente. Si no existe, devuelve 0.
        """
        return self.existencias.get(id_ingrediente, 0)

    def set_cantidad(self, id_ingrediente, cantidad):
        """
        Establece la cantidad total de un ingrediente.
        """
        if cantidad < 0:
            cantidad = 0
        self.existencias[id_ingrediente] = cantidad
        return True

    def restar_cantidad(self, id_ingrediente, cantidad_a_restar):
        """
        Resta una cantidad del stock. Devuelve False si no hay suficiente.
        """
        cantidad_actual = self.obtener_cantidad(id_ingrediente)
        if cantidad_actual < cantidad_a_restar:
            return False 
        
        self.existencias[id_ingrediente] = cantidad_actual - cantidad_a_restar
        return True

    def agregar_cantidad(self, id_ingrediente, cantidad_a_agregar):
        """
        Agrega una cantidad al stock existente.
        """
        if cantidad_a_agregar < 0:
            return False 
            
        cantidad_actual = self.obtener_cantidad(id_ingrediente)
        self.existencias[id_ingrediente] = cantidad_actual + cantidad_a_agregar
        return True