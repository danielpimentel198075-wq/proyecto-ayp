# modelos.py

class Ingrediente:
    """
    Representa un ingrediente (pan, salchicha, topping, salsa, acompañante, etc.).
    """
    def __init__(self, id_, nombre, categoria, tipo, longitud=None):
        self.id = id_
        self.nombre = nombre
        self.categoria = categoria   # Ej: "Pan", "Salchicha", "Topping"
        self.tipo = tipo             # Ej: "integral", "de papa", etc.
        self.longitud = longitud     # Solo relevante para pan/salchicha

    def __str__(self):
        return f"{self.nombre} ({self.categoria}, {self.tipo})"


class HotDog:
    """
    Representa un hot dog del menú.
    """
    def __init__(self, id_, nombre, pan, salchicha, toppings, salsas, acompanante=None):
        self.id = id_
        self.nombre = nombre
        self.pan = pan                  # Ingrediente
        self.salchicha = salchicha      # Ingrediente
        self.toppings = toppings or []  # lista[Ingrediente]
        self.salsas = salsas or []      # lista[Ingrediente]
        self.acompanante = acompanante  # Ingrediente o None

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


class Inventario:
    """
    Maneja las existencias de ingredientes (por id de ingrediente).
    """
    def __init__(self):
        # dict: {id_ingrediente: cantidad}
        self.existencias = {}

    def obtener_cantidad(self, id_ingrediente):
        return self.existencias.get(id_ingrediente, 0)

    def actualizar_cantidad(self, id_ingrediente, nueva_cantidad):
        self.existencias[id_ingrediente] = nueva_cantidad

    def agregar(self, id_ingrediente, cantidad):
        actual = self.obtener_cantidad(id_ingrediente)
        self.existencias[id_ingrediente] = actual + cantidad
