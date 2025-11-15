# sistema.py

from Proyecto.modelos import Inventario
from Proyecto.cargador_datos import CargadorDatos
from Proyecto.gestores import GestorIngredientes, GestorInventario, GestorMenu, SimuladorVentas

class SistemaHotDog:
    """
    Clase principal que coordina todos los módulos.
    """
    def __init__(self, url_menu, url_ingredientes):
        # 1. Cargar datos desde la API
        self.cargador = CargadorDatos(url_menu, url_ingredientes)
        ingredientes = self.cargador.cargar_ingredientes_desde_api()
        hotdogs = self.cargador.cargar_menu_desde_api(ingredientes)

        # 2. Crear gestores
        self.gestor_ingredientes = GestorIngredientes(ingredientes)
        self.inventario = Inventario()
        self.gestor_inventario = GestorInventario(self.inventario, self.gestor_ingredientes)
        self.gestor_menu = GestorMenu(self.gestor_ingredientes, self.gestor_inventario)
        self.gestor_menu.hotdogs = hotdogs  # cargamos los hot dogs iniciales

        self.simulador = SimuladorVentas(self.gestor_menu, self.gestor_inventario)

        # TODO: más adelante: cargar estado desde JSON local (ventas previas, inventario, etc.)

    def guardar_estado(self):
        """
        Guarda en un JSON local el estado del sistema (ingredientes, inventario, menú, ventas...).
        """
        # TODO: implementar con json.dump()
        pass

    def ejecutar(self):
        """
        Menú principal de la aplicación.
        """
        while True:
            print("\n=== Sistema Hot Dog CCS ===")
            print("1. Gestión de ingredientes")
            print("2. Gestión de inventario")
            print("3. Gestión del menú")
            print("4. Simular un día de ventas")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.menu_ingredientes()
            elif opcion == "2":
                self.menu_inventario()
            elif opcion == "3":
                self.menu_menu()
            elif opcion == "4":
                self.menu_simulacion()
            elif opcion == "0":
                print("Guardando estado y saliendo...")
                self.guardar_estado()
                break
            else:
                print("Opción inválida, intente de nuevo.")

    def menu_ingredientes(self):
        # TODO: mostrar submenú:
        # 1) listar por categoría
        # 2) listar por categoría y tipo
        # 3) agregar
        # 4) eliminar
        # etc.
        pass

    def menu_inventario(self):
        # TODO: opciones para ver inventario, buscar ingrediente, actualizar existencia...
        pass

    def menu_menu(self):
        # TODO: opciones para listar hot dogs, agregar nuevo, eliminar, etc.
        pass

    def menu_simulacion(self):
        # TODO: llamar a self.simulador.simular_dia()
        pass
