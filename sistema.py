# sistema.py
import json
from modelos import Inventario
from cargador_datos import CargadorDatos
from gestores import GestorIngredientes, GestorInventario, GestorMenu, SimuladorVentas

class SistemaHotDog:
    """
    Clase principal que coordina todos los módulos.
    """
   # (En sistema.py)

    def __init__(self, url_menu, url_ingredientes):
        
        self.ARCHIVO_LOCAL = "estado_local.json" # Nombre de nuestro archivo de guardado

        # 1. Cargar datos desde la API
        self.cargador = CargadorDatos(url_menu, url_ingredientes)
        ingredientes = self.cargador.cargar_ingredientes_desde_api()
        hotdogs = self.cargador.cargar_menu_desde_api(ingredientes)

        # 2. Crear gestores
        self.gestor_ingredientes = GestorIngredientes(ingredientes)
        self.inventario = Inventario() # Creamos el inventario vacío
        self.gestor_inventario = GestorInventario(self.inventario, self.gestor_ingredientes)
        self.gestor_menu = GestorMenu(self.gestor_ingredientes, self.gestor_inventario)
        self.gestor_menu.hotdogs = hotdogs  # cargamos los hot dogs iniciales

        self.simulador = SimuladorVentas(self.gestor_menu, self.gestor_inventario)

        # 3. Cargar estado local (inventario)
        # Primero, nos aseguramos de que todos los ingredientes de la API estén en el inventario (con 0 stock)
        self.gestor_inventario.inicializar_inventario_con_cero()
        # Luego, cargamos las existencias guardadas del archivo local (si existe)
        self.cargar_estado()
        print(f"Sistema inicializado. Inventario cargado desde '{self.ARCHIVO_LOCAL}'.")


    def cargar_estado(self):
        """
        Carga el inventario desde el archivo JSON local.
        """
        try:
            with open(self.ARCHIVO_LOCAL, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Cargamos las existencias. self.inventario.existencias ya fue 
                # inicializado con ceros, esto actualiza los valores guardados.
                self.inventario.existencias.update(data.get("inventario", {}))
            print(f"Datos cargados desde '{self.ARCHIVO_LOCAL}'.")
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo '{self.ARCHIVO_LOCAL}'. Se usará un inventario nuevo.")
        except json.JSONDecodeError:
            print(f"Error: El archivo '{self.ARCHIVO_LOCAL}' está corrupto. No se pudo cargar el inventario.")

    def guardar_estado(self):
        """
        Guarda el estado actual del inventario en un JSON local.
        """
        try:
            # Preparamos los datos a guardar
            data_para_guardar = {
                "inventario": self.inventario.existencias
                # Aquí también podrías guardar hotdogs nuevos, etc.
            }

            with open(self.ARCHIVO_LOCAL, 'w', encoding='utf-8') as f:
                json.dump(data_para_guardar, f, indent=4, ensure_ascii=False)
            print(f"Inventario guardado exitosamente en '{self.ARCHIVO_LOCAL}'.")
        except IOError as e:
            print(f"Error al guardar el estado en '{self.ARCHIVO_LOCAL}': {e}")

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

    # (Esto va dentro de la clase SistemaHotDog en sistema.py)

    def menu_ingredientes(self):
        """
        Muestra el submenú para la gestión de ingredientes.
        """
        while True:
            print("\n--- Gestión de Ingredientes ---")
            print("1. Listar ingredientes por categoría")
            print("2. Listar ingredientes por categoría y tipo")
            print("3. Agregar nuevo ingrediente (Próximamente)")
            print("4. Eliminar ingrediente (Próximamente)")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                # Pedimos la categoría al usuario
                categoria = input("Ingrese la categoría a listar (ej: Pan, Salchicha, Salsa, toppings, Acompañante): ")
                # Llamamos al gestor para que haga la búsqueda
                resultados = self.gestor_ingredientes.listar_por_categoria(categoria)
                
                if not resultados:
                    print(f"\nNo se encontraron ingredientes para la categoría '{categoria}'.")
                else:
                    print(f"\n--- Ingredientes en '{categoria}' ---")
                    for ing in resultados:
                        # Esto usa el método __str__ de tu clase Ingrediente
                        print(f"- {ing}") 
            
            elif opcion == "2":
                categoria = input("Ingrese la categoría (ej: Pan, Salchicha...): ")
                tipo = input(f"Ingrese el tipo para '{categoria}' (ej: blanco, res, vegetal...): ")
                # Llamamos al gestor
                resultados = self.gestor_ingredientes.listar_por_categoria_y_tipo(categoria, tipo)

                if not resultados:
                    print(f"\nNo se encontraron ingredientes para '{categoria}' del tipo '{tipo}'.")
                else:
                    print(f"\n--- Ingredientes en '{categoria}' (Tipo: {tipo}) ---")
                    for ing in resultados:
                        print(f"- {ing}")

            elif opcion == "3":
                print("\nFunción para AGREGAR no implementada todavía.")
                # TODO: Implementar la lógica para agregar
                pass

            elif opcion == "4":
                print("\nFunción para ELIMINAR no implementada todavía.")
                # TODO: Implementar la lógica para eliminar
                pass

            elif opcion == "0":
                print("Volviendo al menú principal...")
                break # Rompe el "while True" y regresa al menú principal

            else:
                print("Opción inválida, intente de nuevo.")

    # (En sistema.py)

    def menu_inventario(self):
        """
        Muestra el submenú para la gestión de inventario.
        """
        while True:
            print("\n--- Gestión de Inventario ---")
            print("1. Mostrar inventario completo (con existencias)")
            print("2. Mostrar ingredientes con bajo stock (<= 10)")
            print("3. Actualizar existencias de un ingrediente")
            print("4. Agregar existencias (Reponer)")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                print("\n--- Inventario Completo ---")
                inventario_completo = self.gestor_inventario.obtener_inventario_completo()
                if not inventario_completo:
                    print("El inventario está vacío.")
                else:
                    for ing, cantidad in inventario_completo:
                        print(f"[{ing.categoria}] {ing.nombre}: {cantidad} unidades")
            
            elif opcion == "2":
                print("\n--- Ingredientes con Bajo Stock (<= 10) ---")
                bajos_en_stock = self.gestor_inventario.obtener_inventario_bajo_stock(10)
                if not bajos_en_stock:
                    print("No hay ingredientes con bajo stock.")
                else:
                    for ing, cantidad in bajos_en_stock:
                        print(f"[{ing.categoria}] {ing.nombre}: {cantidad} unidades")

            elif opcion == "3":
                id_ingrediente = input("Ingrese el nombre (ID) del ingrediente a actualizar (ej: 'simple', 'weiner'): ")
                
                try:
                    nueva_cantidad = int(input(f"Ingrese la nueva cantidad TOTAL para '{id_ingrediente}': "))
                    if nueva_cantidad < 0:
                        print("Error: La cantidad no puede ser negativa.")
                        continue 

                    # Usamos set_existencia_total para establecer el nuevo valor
                    exito = self.gestor_inventario.set_existencia_total(id_ingrediente, nueva_cantidad)
                    
                    if exito:
                        print(f"¡Éxito! Stock de '{id_ingrediente}' actualizado a {nueva_cantidad}.")
                    else:
                        print(f"Error: No se encontró un ingrediente con el ID '{id_ingrediente}'.")

                except ValueError:
                    print("Error: Debe ingresar un número entero para la cantidad.")

            elif opcion == "4":
                id_ingrediente = input("Ingrese el nombre (ID) del ingrediente a reponer (ej: 'simple', 'weiner'): ")
                
                try:
                    cantidad_a_agregar = int(input(f"Ingrese la cantidad que desea AGREGAR a '{id_ingrediente}': "))
                    if cantidad_a_agregar <= 0:
                        print("Error: La cantidad a agregar debe ser positiva.")
                        continue 

                    # Usamos agregar_existencia para sumar al valor actual
                    exito = self.gestor_inventario.agregar_existencia(id_ingrediente, cantidad_a_agregar)
                    
                    if exito:
                        cantidad_total = self.gestor_inventario.buscar_existencia(id_ingrediente)
                        print(f"¡Éxito! Stock de '{id_ingrediente}' actualizado a {cantidad_total}.")
                    else:
                        print(f"Error: No se encontró un ingrediente con el ID '{id_ingrediente}'.")

                except ValueError:
                    print("Error: Debe ingresar un número entero para la cantidad.")

            elif opcion == "0":
                print("Volviendo al menú principal...")
                break

            else:
                print("Opción inválida, intente de nuevo.")


    def menu_menu(self):
        # TODO: opciones para listar hot dogs, agregar nuevo, eliminar, etc.
        pass

    def menu_simulacion(self):
        # TODO: llamar a self.simulador.simular_dia()
        pass
