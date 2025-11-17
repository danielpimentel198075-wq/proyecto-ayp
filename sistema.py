import json
import matplotlib.pyplot as plt
from modelos import Inventario, HotDog
from cargador_datos import CargadorDatos
from gestores import GestorIngredientes, GestorInventario, GestorMenu, SimuladorVentas

class SistemaHotDog:
    """
    Clase principal que coordina todos los módulos.
    """

    def __init__(self, url_menu, url_ingredientes):
        
        self.ARCHIVO_LOCAL = "estado_local.json" 

        self.cargador = CargadorDatos(url_menu, url_ingredientes)
        ingredientes_api = self.cargador.cargar_ingredientes_desde_api()
        hotdogs_api = self.cargador.cargar_menu_desde_api(ingredientes_api)

        self.gestor_ingredientes = GestorIngredientes(ingredientes_api)
        self.inventario = Inventario() 
        self.gestor_inventario = GestorInventario(self.inventario, self.gestor_ingredientes)
        
        self.gestor_menu = GestorMenu(self.gestor_ingredientes, self.gestor_inventario)
        
        self.simulador = SimuladorVentas(self.gestor_menu, self.gestor_inventario)

        self.gestor_inventario.inicializar_inventario_con_cero()
        

        hotdogs_locales = self.cargar_estado() 
        

        self.gestor_menu.hotdogs.update(hotdogs_api) 
    
        self.gestor_menu.hotdogs.update(hotdogs_locales)
        
        print(f"Sistema inicializado. {len(self.gestor_menu.hotdogs)} hot dogs cargados.")


    def cargar_estado(self):
        """
        Carga el inventario Y los hot dogs locales desde el JSON.
        Devuelve un dict de {id: HotDog} locales.
        """
        hotdogs_locales = {}
        try:
            with open(self.ARCHIVO_LOCAL, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
                self.inventario.existencias.update(data.get("inventario", {}))
                print(f"Inventario cargado desde '{self.ARCHIVO_LOCAL}'.")

               
                hotdogs_data_local = data.get("hotdogs_locales", [])
                
                db = self.gestor_ingredientes.ingredientes
                
                for item in hotdogs_data_local:
                    try:
                        pan = db[item["Pan"]]
                        salchicha = db[item["Salchicha"]]
                        toppings = [db[t] for t in item["toppings"]]
                        lista_salsas = item.get("salsas", item.get("Salsas", []))
                        salsas = [db[s] for s in lista_salsas]
                        acomp_nombre = item["Acompañante"]
                        acompanante = db.get(acomp_nombre) if acomp_nombre else None
                        
                        hd = HotDog(
                            id_=item["nombre"],
                            nombre=item["nombre"],
                            pan=pan,
                            salchicha=salchicha,
                            toppings=toppings,
                            salsas=salsas,
                            acompanante=acompanante
                        )
                        hotdogs_locales[hd.id] = hd
                    except KeyError as e:
                        print(f"Advertencia al cargar hot dog local '{item['nombre']}': No se encontró el ingrediente '{e.args[0]}'.")

        except FileNotFoundError:
            print(f"Advertencia: No se encontró '{self.ARCHIVO_LOCAL}'. Se usará un estado nuevo.")
        except json.JSONDecodeError:
            print(f"Error: El archivo '{self.ARCHIVO_LOCAL}' está corrupto. No se pudo cargar.")
        
        return hotdogs_locales

    def guardar_estado(self):
        """
        Guarda el inventario y los hot dogs locales en JSON.
        """
        try:
          
            hotdogs_serializados = [hd.to_dict() for hd in self.gestor_menu.hotdogs.values()]

            data_para_guardar = {
                "inventario": self.inventario.existencias,
                "hotdogs_locales": hotdogs_serializados 
            }

            with open(self.ARCHIVO_LOCAL, 'w', encoding='utf-8') as f:
                json.dump(data_para_guardar, f, indent=4, ensure_ascii=False)
            print(f"Estado (Inventario y Menú) guardado en '{self.ARCHIVO_LOCAL}'.")
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



    def menu_ingredientes(self):
        """
        Muestra el submenú para la consulta de ingredientes.
        """
        while True:
            print("\n--- Consulta de Ingredientes ---")
            print("1. Listar ingredientes por categoría")
            print("2. Listar ingredientes por categoría y tipo")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                categoria = input("Ingrese la categoría a listar (ej: Pan, Salchicha, Salsa, toppings, Acompañante): ")
                resultados = self.gestor_ingredientes.listar_por_categoria(categoria)
                
                if not resultados:
                    print(f"\nNo se encontraron ingredientes para la categoría '{categoria}'.")
                else:
                    print(f"\n--- Ingredientes en '{categoria}' ---")
                    for ing in resultados:
                        print(f"- {ing}") 
            
            elif opcion == "2":
                categoria = input("Ingrese la categoría (ej: Pan, Salchicha...): ")
                tipo = input(f"Ingrese el tipo para '{categoria}' (ej: blanco, res, vegetal...): ")
                resultados = self.gestor_ingredientes.listar_por_categoria_y_tipo(categoria, tipo)

                if not resultados:
                    print(f"\nNo se encontraron ingredientes para '{categoria}' del tipo '{tipo}'.")
                else:
                    print(f"\n--- Ingredientes en '{categoria}' (Tipo: {tipo}) ---")
                    for ing in resultados:
                        print(f"- {ing}")

            elif opcion == "0":
                print("Volviendo al menú principal...")
                break 

            else:
                print("Opción inválida, intente de nuevo.")

    
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
        """
        Muestra el submenú para la gestión del menú.
        """
        while True:
            print("\n--- Gestión del Menú ---")
            print("1. Listar todos los hot dogs")
            print("2. Ver detalle de un hot dog")
            print("3. Agregar nuevo hot dog al menú")
            print("4. Eliminar hot dog del menú")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._menu_listar_hotdogs()
            elif opcion == "2":
                self._menu_detalle_hotdog()
            elif opcion == "3":
                self._menu_agregar_hotdog()
            elif opcion == "4":
                self._menu_eliminar_hotdog()
            elif opcion == "0":
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción inválida, intente de nuevo.")

    def _menu_listar_hotdogs(self):
        print("\n--- Hot Dogs en el Menú ---")
        hotdogs = self.gestor_menu.listar_hotdogs()
        if not hotdogs:
            print("No hay hot dogs en el menú.")
            return
        
        hotdogs_ordenados = sorted(hotdogs, key=lambda h: h.nombre)
        
        for hd in hotdogs_ordenados:
            hay_stock, ing_faltante = self.gestor_menu.hay_inventario_para_hotdog(hd)
            disponible = "SÍ" if hay_stock else f"NO (Falta: {ing_faltante.nombre})"
            print(f"- {hd.nombre} (Disponible: {disponible})")

    def _menu_detalle_hotdog(self):
        id_hotdog = input("Ingrese el nombre (ID) del hot dog a ver: ")
        hd = self.gestor_menu.obtener_hotdog_por_id(id_hotdog)
        
        if not hd:
            print(f"Error: No se encontró un hot dog con el nombre '{id_hotdog}'.")
            return

        print(f"\n--- Detalle de '{hd.nombre}' ---")
        print(f"  Pan: {hd.pan.nombre}")
        print(f"  Salchicha: {hd.salchicha.nombre}")
        

        toppings_str = ", ".join([t.nombre for t in hd.toppings]) or "Ninguno"
        salsas_str = ", ".join([s.nombre for s in hd.salsas]) or "Ninguna"
        acomp_str = hd.acompanante.nombre if hd.acompanante else "Ninguno"
        
        print(f"  Toppings: {toppings_str}")
        print(f"  Salsas: {salsas_str}")
        print(f"  Acompañante: {acomp_str}")
        
      
        es_valido, mensaje = self.gestor_menu.validar_hotdog(hd)
        print(f"  Validación: {'Válido' if es_valido else f'Inválido ({mensaje})'}")

    def _menu_eliminar_hotdog(self):
        id_hotdog = input("Ingrese el nombre (ID) del hot dog a eliminar: ")
        if not self.gestor_menu.obtener_hotdog_por_id(id_hotdog):
                print(f"Error: No se encontró un hot dog con el nombre '{id_hotdog}'.")
                return
        
        confirm = input(f"¿Seguro que desea eliminar '{id_hotdog}'? (s/n): ").lower()
        if confirm == 's':
            exito = self.gestor_menu.eliminar_hotdog(id_hotdog)
            if exito:
                print(f"¡Éxito! Hot dog '{id_hotdog}' eliminado del menú.")
            else:
                
                print(f"Error: No se pudo eliminar '{id_hotdog}'.")

    def _menu_agregar_hotdog(self):
        print("\n--- Agregar Nuevo Hot Dog ---")
        id_hotdog = input("Ingrese el nombre (ID) para el nuevo hot dog (ej: 'especial de la casa'): ")
        
       
        def seleccionar_ingrediente(categoria):
            print(f"\nSeleccionando '{categoria}'...")
            opciones = self.gestor_ingredientes.listar_por_categoria(categoria)
            if not opciones:
                print(f"Error: No hay ingredientes en la categoría '{categoria}'.")
                return None
            
            opciones.sort(key=lambda ing: ing.nombre) 
            for i, ing in enumerate(opciones):
                print(f"  {i+1}. {ing.nombre} (Tipo: {ing.tipo})")
            
            while True:
                try:
                    sel = int(input(f"Seleccione un número (1-{len(opciones)}): "))
                    if 1 <= sel <= len(opciones):
                        return opciones[sel-1] 
                    else:
                        print("Número fuera de rango.")
                except ValueError:
                    print("Selección inválida.")
   

    
        pan = seleccionar_ingrediente("Pan")
        if not pan: return 

        
        salchicha = seleccionar_ingrediente("Salchicha")
        if not salchicha: return

       
        toppings = []
        while True:
            print(f"\nToppings actuales: {', '.join([t.nombre for t in toppings]) or 'Ninguno'}")
            opcion = input("¿Desea agregar un topping? (s/n): ").lower()
            if opcion != 's':
                break
            topping = seleccionar_ingrediente("toppings")
            if topping and topping not in toppings:
                toppings.append(topping)
            elif topping in toppings:
                print(f"'{topping.nombre}' ya fue agregado.")


        salsas = []
        while True:
            print(f"\nSalsas actuales: {', '.join([s.nombre for s in salsas]) or 'Ninguna'}")
            opcion = input("¿Desea agregar una salsa? (s/n): ").lower()
            if opcion != 's':
                break
            salsa = seleccionar_ingrediente("Salsa")
            if salsa and salsa not in salsas:
                salsas.append(salsa)
            elif salsa in salsas:
                print(f"'{salsa.nombre}' ya fue agregada.")

        acompanante = None
        if input("\n¿Desea agregar un acompañante? (s/n): ").lower() == 's':
            acompanante = seleccionar_ingrediente("Acompañante")
        
        nuevo_hotdog = HotDog(
            id_=id_hotdog,
            nombre=id_hotdog,
            pan=pan,
            salchicha=salchicha,
            toppings=toppings,
            salsas=salsas,
            acompanante=acompanante
        )

        exito, mensaje = self.gestor_menu.agregar_hotdog(nuevo_hotdog)
        
        if exito:
            print(f"\n¡ÉXITO! El hot dog '{id_hotdog}' fue creado y agregado al menú.")
            print("Podrá verlo en la lista y será guardado al salir del programa.")
        else:
            print(f"\nERROR AL CREAR: {mensaje}")

    def menu_simulacion(self):
        """
        Pide al usuario el número de clientes y ejecuta la simulación.
        """
        print("\n--- Simulación de un Día de Ventas ---")
        try:
            n_clientes = int(input("Ingrese el número de clientes para la simulación (N): "))
            if n_clientes <= 0:
                print("Error: El número de clientes debe ser positivo.")
                return
        except ValueError:
            print("Error: Debe ingresar un número entero.")
            return

        print(f"\nSimulando {n_clientes} clientes... ¡Esto puede tardar un momento!")
        
        reporte = self.simulador.simular_dia(n_clientes)
        
        if not reporte:
            print("No se pudo generar el reporte (quizás no hay hot dogs).")
            return

        print("--- ¡Simulación Completada! ---")
        print(f"\n=== Reporte de Ventas (N={n_clientes}) ===")
        print(f"Ventas Exitosas: {reporte['ventas_exitosas']}")
        print(f"Ventas Fallidas (por stock): {reporte['ventas_fallidas_stock']}")
        print(f"Ventas Fallidas (hot dog inválido): {reporte['ventas_fallidas_validez']}")
        print("---------------------------------")
   
        print("\n--- Hot Dogs Vendidos ---")
        if not reporte['hotdogs_vendidos']:
            print("No se vendió ningún hot dog.")
        else:
            vendidos_ordenados = sorted(reporte['hotdogs_vendidos'].items(), key=lambda item: item[1], reverse=True)
            for nombre, cantidad in vendidos_ordenados:
                print(f"- {nombre}: {cantidad} unidades")

        print("\n--- Ingredientes que Faltaron (Oportunidades perdidas) ---")
        if not reporte['ingredientes_faltantes']:
            print("No faltó ningún ingrediente durante las ventas fallidas.")
        else:
            faltantes_ordenados = sorted(reporte['ingredientes_faltantes'].items(), key=lambda item: item[1], reverse=True)
            for nombre, cantidad in faltantes_ordenados:
                print(f"- {nombre}: Faltó {cantidad} veces")
        
        print("\n¡Importante! El inventario ha sido actualizado.")
        print("Recuerde Guardar (Opción 0) si desea que los cambios persistan.")


        self._mostrar_grafico_ventas(reporte)

    def _mostrar_grafico_ventas(self, reporte):
        """
        Usa matplotlib para generar y mostrar los gráficos del reporte.
        """
        print("\nGenerando gráficas del reporte...")

        datos_ventas = reporte['hotdogs_vendidos']
        if not datos_ventas:
            print("No hay datos de ventas para graficar.")
        else:
         
            nombres = list(datos_ventas.keys())
            cantidades = list(datos_ventas.values())

            plt.figure(1, figsize=(10, 6)) 
            plt.bar(nombres, cantidades, color='green')
            plt.title('Hot Dogs Más Vendidos')
            plt.ylabel('Cantidad Vendida')
            plt.xlabel('Nombre del Hot Dog')
            plt.xticks(rotation=45, ha='right') 
            plt.tight_layout() 

        datos_faltantes = reporte['ingredientes_faltantes']
        if not datos_faltantes:
            print("No hay datos de ingredientes faltantes para graficar.")
        else:
            nombres_ing = list(datos_faltantes.keys())
            cantidades_ing = list(datos_faltantes.values())

            plt.figure(2, figsize=(10, 6)) 
            plt.bar(nombres_ing, cantidades_ing, color='red')
            plt.title('Ingredientes Faltantes (Oportunidades Perdidas)')
            plt.ylabel('Veces que Faltó')
            plt.xlabel('Nombre del Ingrediente')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

    
        if datos_ventas or datos_faltantes:
            print("Mostrando gráficas... Cierra las ventanas de las gráficas para continuar.")
            plt.show() 
        else:
            print("No se generaron gráficas por falta de datos.")