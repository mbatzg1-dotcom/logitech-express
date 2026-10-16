# Herramientas estándar y funciones de las capas de datos y negocio.
from datetime import date
import csv

from app.database.connection import (
    crear_archivo_envios,
    guardar_envio,
    listar_envios,
    buscar_envios,
    obtener_estadisticas,
)

from app.services.auditoria import generar_informe_auditoria
from app.services.procesamiento_lotes import procesar_lote
from app.services.tarificacion import calcular_tarifa_envio, validar_paquete


# Solicita los datos del paquete en consola y los devuelve en un diccionario.
def pedir_paquete():
    paquete = {}
    paquete["paquete_id"] = input("ID del paquete: ").strip()
    print("Destino: 1) Nacional  2) Internacional")
    destino = input("Seleccione destino: ").strip()
    if destino == "1":
        paquete["destino"] = "Nacional"
    elif destino == "2":
        paquete["destino"] = "Internacional"
    else:
        paquete["destino"] = destino

    paquete["peso_kg"] = input("Peso en kilogramos: ").strip()
    print("Servicio: 1) Estandar  2) Express")
    servicio = input("Seleccione servicio: ").strip()
    if servicio == "1":
        paquete["servicio"] = "Estandar"
    elif servicio == "2":
        paquete["servicio"] = "Express"
    else:
        paquete["servicio"] = servicio

    seguro = input("¿Requiere seguro? (s/n): ").strip().lower()
    paquete["requiere_seguro"] = seguro in ("s", "si", "sí", "1")
    paquete["fecha_registro"] = date.today().isoformat()
    return paquete


# Valida, calcula y guarda un envío ingresado individualmente.
def registrar_envio():
    print("\n--- Registrar envío ---")
    paquete = pedir_paquete()
    try:
        paquete = validar_paquete(paquete)
        paquete["tarifa_final"] = float(calcular_tarifa_envio(paquete))
        if guardar_envio(paquete):
            print("Envío guardado. Tarifa: Q{:.2f}".format(paquete["tarifa_final"]))
        else:
            print("Error: ya existe un paquete con ese ID.")
    except ValueError as error:
        print("Datos inválidos:", error)
    except (OSError, csv.Error) as error:
        print("No se pudo guardar el envío:", error)


# Imprime los envíos en formato de tabla para facilitar su lectura.
def mostrar_envios(envios):
    if not envios:
        print("No hay envíos que mostrar.")
        return
    print("\n{:<16} {:<12} {:<16} {:>10} {:<12} {:<8} {:>12}".format(
        "ID", "Fecha", "Destino", "Peso (kg)", "Servicio", "Seguro", "Tarifa"
    ))
    print("-" * 92)
    for envio in envios:
        seguro = "Sí" if envio["requiere_seguro"] else "No"
        print("{:<16} {:<12} {:<16} {:>10.2f} {:<12} {:<8} Q{:>10.2f}".format(
            envio["paquete_id"],
            envio["fecha_registro"],
            envio["destino"],
            float(envio["peso_kg"]),
            envio["servicio"],
            seguro,
            float(envio["tarifa_final"]),
        ))


# Pide filtros y muestra los registros encontrados en el archivo CSV.
def ver_historial():
    print("\n--- Historial de envíos ---")
    texto_id = input("Filtrar por ID (Enter para todos): ").strip()
    destino = input("Destino (Enter para todos): ").strip()
    servicio = input("Servicio (Enter para todos): ").strip()
    if destino not in ("Nacional", "Internacional"):
        destino = ""
    if servicio not in ("Estandar", "Express"):
        servicio = ""
    try:
        mostrar_envios(buscar_envios(texto_id, destino, servicio))
    except (OSError, csv.Error, ValueError) as error:
        print("No se pudo consultar el historial:", error)


# Lee varias líneas, calcula las tarifas y permite guardar los registros válidos.
def procesar_lote_terminal():
    print("\n--- Procesar lote ---")
    print("Ingrese datos separados por punto y coma:")
    print("ID;destino;kg;servicio;seguro(s/n). Línea vacía para terminar.")
    paquetes = []
    while True:
        linea = input("> ").strip()
        if not linea:
            break
        partes = linea.split(";")
        if len(partes) != 5:
            paquetes.append({})
            continue
        paquetes.append({
            "paquete_id": partes[0].strip(),
            "destino": partes[1].strip(),
            "peso_kg": partes[2].strip(),
            "servicio": partes[3].strip(),
            "requiere_seguro": partes[4].strip().lower() in ("s", "si", "sí", "1"),
        })

    resultado = procesar_lote(paquetes)
    print("\nEnvíos calculados:", resultado["total_envios"])
    print("Ingresos: Q{:.2f}".format(resultado["ingresos_totales"]))
    print("Tarifa promedio: Q{:.2f}".format(resultado["tarifa_promedio"]))
    print("Nacionales: {} | Internacionales: {}".format(
        resultado["nacionales"], resultado["internacionales"]
    ))
    for envio in resultado["registros_validos"]:
        print("{}: Q{:.2f}".format(envio["paquete_id"], envio["tarifa_final"]))

    for invalido in resultado["registros_invalidos"]:
        print("Línea {} inválida: {}".format(invalido["indice"], invalido["error"]))

    if input("¿Guardar los envíos válidos? (s/n): ").strip().lower() in ("s", "si", "sí"):
        guardados = 0
        for envio in resultado["registros_validos"]:
            envio["fecha_registro"] = date.today().isoformat()
            try:
                if guardar_envio(envio):
                    guardados += 1
                else:
                    print("ID duplicado, no guardado:", envio["paquete_id"])
            except (OSError, csv.Error) as error:
                print("Error al guardar {}: {}".format(envio["paquete_id"], error))
        print("Envíos guardados:", guardados)


# Compara las tarifas almacenadas con el cálculo actual y reporta diferencias.
def auditar_envios():
    print("\n--- Auditoría ---")
    try:
        informe = generar_informe_auditoria(listar_envios())
        print(informe["informe"])
        if informe["diferencias"]:
            for diferencia in informe["diferencias"]:
                print(diferencia)
        estadisticas = obtener_estadisticas()
        total = estadisticas["total_envios"]
        if total:
            eficiencia = informe["correctos"] * 100 / total
        else:
            eficiencia = 0
        print("Eficiencia de tarifas: {:.1f}%".format(eficiencia))
    except (OSError, csv.Error, ValueError) as error:
        print("No se pudo completar la auditoría:", error)


# Muestra cantidades e ingresos acumulados que se obtienen de la base de datos.
def mostrar_resumen():
    try:
        datos = obtener_estadisticas()
        print("\n--- Resumen ---")
        print("Envíos: {}".format(datos["total_envios"]))
        print("Ingresos: Q{:.2f}".format(datos["ingresos_totales"]))
        print("Promedio: Q{:.2f}".format(datos["tarifa_promedio"]))
        print("Nacionales: {} | Internacionales: {}".format(
            datos["nacionales"], datos["internacionales"]
        ))
        print("Estándar: {} | Express: {}".format(datos["estandar"], datos["express"]))
    except (OSError, csv.Error, ValueError) as error:
        print("No se pudo obtener el resumen:", error)


# Inicializa la base y mantiene el menú hasta que el usuario elija salir.
def ejecutar_menu():
    crear_archivo_envios()
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


# Este bloque inicia el programa solamente cuando se ejecuta main.py directamente.
if __name__ == "__main__":
    ejecutar_menu()
