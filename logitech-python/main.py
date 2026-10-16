# Matriz de envíos cargada al iniciar. Cada fila contiene los campos del paquete.
matriz_envios = []


# Solicita los datos de un envío, convierte las opciones del menú y valida
# que los campos sean correctos y que el ID todavía no exista.
def pedir_paquete():
    while True:
        print("\nIngrese los datos del envío:")
        paquete_id = input("ID del paquete: ").strip()

        print("Destino: 1) Nacional  2) Internacional")
        opcion_destino = input("Seleccione destino: ").strip()
        if opcion_destino == "1":
            destino = "Nacional"
        elif opcion_destino == "2":
            destino = "Internacional"
        else:
            destino = opcion_destino

        peso = input("Peso en kilogramos: ").strip()

        print("Servicio: 1) Estandar  2) Express")
        opcion_servicio = input("Seleccione servicio: ").strip()
        if opcion_servicio == "1":
            servicio = "Estandar"
        elif opcion_servicio == "2":
            servicio = "Express"
        else:
            servicio = opcion_servicio

        seguro = input("¿Requiere seguro? (s/n): ").strip().lower()
        requiere_seguro = seguro == "s" or seguro == "si" or seguro == "sí"

        paquete = [
            paquete_id,
            destino,
            peso,
            servicio,
            requiere_seguro,
            date.today().isoformat(),
            0.0,
        ]

        try:
            paquete = validar_paquete(paquete)
            for fila in matriz_envios:
                if fila[ID] == paquete[ID]:
                    raise ValueError("Ya existe un envío con ese ID.")
            return paquete
        except ValueError as error:
            print("Formulario inválido:", error)
            print("Vuelva a ingresar los datos.\n")


# Calcula la tarifa del envío validado y lo guarda tanto en la matriz en memoria
# como en el archivo CSV. Informa si el ID ya estaba registrado.
def registrar_envio():
    print("\n--- Registrar envío ---")
    paquete = pedir_paquete()
    paquete[TARIFA] = calcular_tarifa_envio(paquete)
    try:
        if guardar_envio(matriz_envios, paquete):
            print("Envío guardado. Tarifa: Q{:.2f}".format(paquete[TARIFA]))
        else:
            print("No se guardó: ya existe un envío con ese ID.")
    except (OSError, csv.Error) as error:
        print("No se pudo guardar el envío:", error)


# Imprime las filas recibidas en forma de tabla para que el historial sea legible.
def mostrar_envios(envios):
    if not envios:
        print("No hay envíos que mostrar.")
        return

    print("\n{:<16} {:<12} {:<16} {:>10} {:<12} {:<8} {:>12}".format(
        "ID", "Fecha", "Destino", "Peso (kg)", "Servicio", "Seguro", "Tarifa"
    ))
    print("-" * 92)
    for envio in envios:
        if envio[SEGURO]:
            seguro = "Sí"
        else:
            seguro = "No"
        print("{:<16} {:<12} {:<16} {:>10.2f} {:<12} {:<8} Q{:>10.2f}".format(
            envio[ID],
            envio[FECHA],
            envio[DESTINO],
            float(envio[PESO_KG]),
            envio[SERVICIO],
            seguro,
            float(envio[TARIFA]),
        ))


# Solicita filtros opcionales de ID, destino y servicio, y muestra las coincidencias.
def ver_historial():
    print("\n--- Historial de envíos ---")
    texto_id = input("Filtrar por ID (Enter para todos): ").strip()
    destino = input("Destino (Nacional/Internacional o Enter): ").strip()
    servicio = input("Servicio (Estandar/Express o Enter): ").strip()

    if destino != "Nacional" and destino != "Internacional":
        destino = ""
    if servicio != "Estandar" and servicio != "Express":
        servicio = ""

    mostrar_envios(buscar_envios(matriz_envios, texto_id, destino, servicio))


# Recibe varias filas en formato separado por punto y coma, calcula cada tarifa,
# muestra válidos e inválidos y pregunta si se deben guardar los válidos.
def procesar_lote_terminal():
    print("\n--- Procesar lote ---")
    print("Formato por línea: ID;destino;kg;servicio;seguro(s/n)")
    print("Ejemplo: ENV-01;Nacional;3;Estandar;no")
    print("Presione Enter en una línea vacía para terminar.")

    paquetes = []
    while True:
        linea = input("> ").strip()
        if linea == "":
            break

        partes = linea.split(";")
        if len(partes) != 5:
            paquetes.append([])
        else:
            seguro = partes[4].strip().lower()
            requiere_seguro = seguro == "s" or seguro == "si" or seguro == "sí"
            paquetes.append([
                partes[0].strip(),
                partes[1].strip(),
                partes[2].strip(),
                partes[3].strip(),
                requiere_seguro,
                date.today().isoformat(),
                0.0,
            ])

    validos, invalidos, estadisticas = procesar_lote(paquetes)
    print("\nEnvíos válidos:", estadisticas[0])
    print("Ingresos: Q{:.2f}".format(estadisticas[1]))
    print("Promedio: Q{:.2f}".format(estadisticas[2]))
    print("Nacionales: {} | Internacionales: {}".format(estadisticas[3], estadisticas[4]))

    for envio in validos:
        print("{}: Q{:.2f}".format(envio[ID], envio[TARIFA]))
    for invalido in invalidos:
        print("Línea {} inválida: {}".format(invalido[0], invalido[1]))

    respuesta = input("¿Guardar los envíos válidos? (s/n): ").strip().lower()
    if respuesta == "s" or respuesta == "si" or respuesta == "sí":
        guardados = 0
        for envio in validos:
            if guardar_envio(matriz_envios, envio):
                guardados = guardados + 1
            else:
                print("ID duplicado, no guardado:", envio[ID])
        print("Envíos guardados:", guardados)


# Compara cada tarifa almacenada con la tarifa actual y muestra diferencias;
# esta operación solo informa y no modifica la matriz.
def auditar_envios():
    print("\n--- Auditoría ---")
    total, correctos, incorrectos, diferencias, informe = generar_informe_auditoria(matriz_envios)
    print(informe)
    for diferencia in diferencias:
        print(diferencia)

    if total == 0:
        eficiencia = 0
    else:
        eficiencia = correctos * 100 / total
    print("Eficiencia de tarifas: {:.1f}%".format(eficiencia))


# Calcula y presenta el conteo de envíos, ingresos, promedio y distribuciones.
def mostrar_resumen():
    datos = obtener_estadisticas(matriz_envios)
    print("\n--- Resumen ---")
    print("Envíos: {}".format(datos[0]))
    print("Ingresos: Q{:.2f}".format(datos[1]))
    print("Promedio: Q{:.2f}".format(datos[2]))
    print("Nacionales: {} | Internacionales: {}".format(datos[3], datos[4]))
    print("Estandar: {} | Express: {}".format(datos[5], datos[6]))


# Prepara el archivo, carga sus filas en la matriz y repite el menú hasta que
# el usuario elija salir.
def ejecutar_menu():
    global matriz_envios
    crear_archivo_envios()
    matriz_envios = cargar_envios()

    while True:
        print("\n=== SISTEMA DE ENVÍOS ===")
        print("1. Registrar envío")
        print("2. Ver historial")
        print("3. Procesar lote")
        print("4. Auditar tarifas")
        print("5. Ver resumen")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_envio()
        elif opcion == "2":
            ver_historial()
        elif opcion == "3":
            procesar_lote_terminal()
        elif opcion == "4":
            auditar_envios()
        elif opcion == "5":
            mostrar_resumen()
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida. Seleccione una opción del menú.")


# Ejecuta el menú solo cuando se inicia este archivo directamente.
if __name__ == "__main__":
    ejecutar_menu()
