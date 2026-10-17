# Creado el 15/10/2026


"""
Valida que todos los valores del paquete sean positivos.
@param paquete Vector de entrada:
0: id
1: destino (1 = nacional, 2 = internacional)
2: peso
3: express (1 = si, 2 = no)
4: seguro (1 = si, 2 = no)
5: tarifa
@return True si todos los valores recibidos son positivos; False si alguno no lo es.
"""
def validar(paquete):
    for col in paquete:
        if col <= 0:
            return False
    return True


"""
Calcula la tarifa de envío del paquete.
@param paquete Vector de entrada:
0: id
1: destino (1 = nacional, 2 = internacional)
2: peso
3: express (1 = si, 2 = no)
4: seguro (1 = si, 2 = no)
5: tarifa
@return Vector con la tarifa calculada en el último elemento.
"""
def tarifa(paquete):
    # Copia del paquete para no modificar el original
    # El vector de entrada tiene 6 elementos, el último es la tarifa que se calculará
    paq = paquete.copy()

    # Tarifa base por destino (nacional = 50, internacional = 250)
    if paquete[1] == 1:
        paq[5] = 50
    elif paquete[1] == 2:
        paq[5] = 250
    else:
        paq[5] = 0

    # Tarifa adicional por peso (si el peso es mayor a 10kg, se cobra 50 por cada kg adicional)
    if paquete[2] > 10:
        dif = paquete[2] - 10
        paq[5] = paq[5] + (dif * 50)  # suma 50 por cada kg adicional

    # Tarifa adicional por express (si es express, se incrementa la tarifa en un 30%)
    if paquete[3] == 1:
        paq[5] = paq[5] * 1.3

    # Tarifa adicional por seguro (si tiene seguro, se incrementa la tarifa en un 5%)
    if paquete[4] == 1:
        paq[5] = paq[5] * 1.05

    return paq


"""
Calcula la tarifa de un lote de paquetes.
@param paquetes Lista de paquetes, cada paquete es una lista de 6 elementos.
@return Copia del lote con la tarifa calculada en el último elemento de cada paquete.
"""
def lote(paquetes):
    # Lista de salida con las tarifas calculadas para cada paquete
    tarifas = []

    # Calcula la tarifa para cada paquete y la agrega a la lista de salida
    for paquete in paquetes:
        tarifas.append(tarifa(paquete))

    return tarifas


"""
Aplica un descuento del 10% si hay al menos 10 paquetes o el total de las tarifas supera Q1500.
@param paquetes Lista de paquetes, cada paquete es una lista de 6 elementos.
@return Copia del lote con las tarifas calculadas y el descuento aplicado si corresponde.
"""
def descuento(paquetes):
    # Calcula las tarifas de los paquetes
    tarifas = lote(paquetes)

    # Calcula el monto total de envio
    total = 0
    for tarifa_paquete in tarifas:
        total += tarifa_paquete[5]

    # Aplica el descuento si se cumplen las condiciones
    if len(paquetes) >= 10 or total > 1500:
        for tarifa_paquete in tarifas:
            tarifa_paquete[5] = tarifa_paquete[5] * 0.9

    return tarifas


"""
Calcula estadísticas de un lote de paquetes.
@param paquetes Lista de paquetes, cada paquete es una lista de 6 elementos.
@return Lista de cuatro valores: [total facturado, peso promedio, mayor costo,
cantidad de envíos express].
"""
def estadisticas(paquetes):
    # Lista de salida con las estadísticas
    stats = [0, 0, 0, 0]

    # Calcula las estadísticas
    for paquete in paquetes:
        # Suma el costo total
        stats[0] += paquete[5]
        # Suma el peso total
        stats[1] += paquete[2]
        # Actualiza el mayor costo
        if paquete[5] > stats[2]:
            stats[2] = paquete[5]
        # Cuenta la cantidad de envíos express
        if paquete[3] == 1:
            stats[3] += 1

    # Calcula el peso promedio
    if len(paquetes) > 0:
        stats[1] /= len(paquetes)

    return stats


"""
Calcula si una entrega cumple con el SLA y la desviación en horas.
@param entrega Lista de entrada:
0: id
1: horas estimadas
2: horas reales
3: cumple SLA (1 = si, 2 = no)
4: desviación en horas (real - estimada)
@return Lista con la información de la entrega y el resultado del SLA.
"""
def sla(entrega):
    # Copia de la lista de entrada para no modificar el original
    ent = entrega.copy()

    # Calcula si cumple SLA y la desviación en horas
    if entrega[2] <= entrega[1]:
        ent[3] = 1.0
    else:
        ent[3] = 2.0

    # Calcula la desviación en horas (real - estimada)
    ent[4] = entrega[2] - entrega[1]
    return ent


"""
Audita un lote de entregas y calcula el SLA para cada una.
@param entregas Lista de entregas; cada una contiene cinco posiciones: id, horas estimadas,
horas reales, resultado SLA y desviación.
@return Lista de entregas con la información del SLA calculada.
"""
def auditoria(entregas):
    # Lista de salida con los resultados de la auditoria
    resultado = []

    # Calcula el SLA para cada entrega y lo agrega a la lista de salida
    for entrega in entregas:
        resultado.append(sla(entrega))

    return resultado


"""
Calcula el diagnostico de eficiencia de un lote de entregas auditadas.
@param auditadas Lista de entregas auditadas, cada entrega es una lista de 5 elementos.
@return Lista de cuatro valores: [cantidad que cumplen, cantidad que no cumplen,
porcentaje de cumplimiento, desviación promedio en horas].
"""
def diagnostico(auditadas):
    # Lista de salida con el diagnostico
    diag = [0, 0, 0, 0]

    # Si no hay entregas auditadas, devuelve la lista con ceros
    if len(auditadas) == 0:
        return diag

    for entrega in auditadas:
        # Cuenta las entregas que cumplen y las que no cumplen
        if entrega[3] == 1:
            diag[0] += 1
        else:
            # Si no cumple, incrementa el contador de entregas que no cumplen
            diag[1] += 1

        # Suma la desviación en horas para calcular el promedio después
        diag[3] += entrega[4]

    # Calcula el porcentaje de cumplimiento y la desviación promedio
    total = len(auditadas)
    # Porcentaje de cumplimiento = (entregas que cumplen / total) * 100
    diag[2] = diag[0] * 100 / total
    # Desviación promedio = (suma de desviaciones / total)
    diag[3] /= total

    return diag


"""
Punto de extensión para limpiar la consola; actualmente no realiza ninguna acción.
"""
def limpiarConsola():
    # os.system("cls")
    pass


"""
Muestra las opciones principales del sistema en la consola.
"""
def menu():
    print("----------------------------------------------------")
    print("1- Registrar y Consultar tarifas")
    print("2- Revision de lotes y estadisticas")
    print("3- Auditoria y Diagnostico de eficiencia")
    print("4- Salir del sistema")
    print("----------------------------------------------------")


"""
Lee un valor numérico desde la entrada estándar.
@return El valor leído; si hubo un error de entrada, devuelve None.
"""
def leer():
    try:
        valor = float(input())
        return valor
    except ValueError:
        return None


"""
Lee los datos de un paquete desde la entrada estándar y los almacena en una lista.
@param paquete Lista donde se almacenarán los datos del paquete.
@return True si todos los datos fueron leídos correctamente y son válidos, False en caso contrario.
"""
def leerPaquete(paquete):
    paquete.clear()
    paquete.extend([0, 0, 0, 0, 0, 0])

    print("ID del paquete: ", end="")
    valor = leer()
    ok1 = valor is not None
    if ok1:
        paquete[0] = valor

    print("Destino (1 = nacional, 2 = internacional): ", end="")
    valor = leer()
    ok2 = valor is not None
    if ok2:
        paquete[1] = valor

    print("Peso (kg): ", end="")
    valor = leer()
    ok3 = valor is not None
    if ok3:
        paquete[2] = valor

    print("Express (1 = si, 2 = no): ", end="")
    valor = leer()
    ok4 = valor is not None
    if ok4:
        paquete[3] = valor

    print("Seguro (1 = si, 2 = no): ", end="")
    valor = leer()
    ok5 = valor is not None
    if ok5:
        paquete[4] = valor

    return (ok1 and ok2 and ok3 and ok4 and ok5 and
            validar([paquete[0], paquete[1], paquete[2], paquete[3], paquete[4]]) and
            (paquete[1] == 1 or paquete[1] == 2) and
            (paquete[3] == 1 or paquete[3] == 2) and
            (paquete[4] == 1 or paquete[4] == 2))


"""
Registra paquetes individuales o por lote y permite consultar sus tarifas.
Los paquetes válidos se agregan a la lista recibida.
@param paquetes Lista donde se almacenan los paquetes registrados.
"""
def modulo1(paquetes):
    opcion = 0
    while opcion != 5:
        print("1- Registrar paquete individual")
        print("2- Registrar lote de paquetes")
        print("3- Consultar tarifas")
        print("5- Volver al menu")
        print("Opcion: ", end="")
        op = leer()
        if op is None:
            op = -1
        opcion = int(op)

        if opcion == 1:
            paquete = []
            if leerPaquete(paquete):
                paquetes.append(paquete)
                print("Paquete registrado.")
            else:
                print("Datos invalidos, paquete descartado.")

        elif opcion == 2:
            print("Cantidad de paquetes a procesar: ", end="")
            n = leer()
            if n is None or n < 1:
                print("Cantidad invalida.")
                continue

            total = int(n)
            i = 1
            while i <= total:
                paquete = []
                print("--- Paquete", i, "de", total, "---")
                if leerPaquete(paquete):
                    paquetes.append(paquete)
                    i += 1
                else:
                    print("Datos invalidos, intente de nuevo.")

            print("Lote registrado:", len(paquetes), "paquetes.")

        elif opcion == 3:
            if len(paquetes) == 0:
                print("No hay paquetes registrados.")
                continue

            print(f"{'Paquete':<10}{'Tarifa':>12}")
            for p in descuento(paquetes):
                print(f"{int(p[0]):<10}{p[5]:>12.2f}")

        elif opcion != 5:
            print("Opcion invalida.")


"""
Muestra las estadísticas de los paquetes registrados.
@param paquetes Paquetes registrados; si está vacío, se informa que no hay datos.
"""
def modulo2(paquetes):
    if len(paquetes) == 0:
        print("No hay paquetes registrados. Use el modulo 1.")
        return

    lotes = descuento(paquetes)
    stats = estadisticas(lotes)
    print(f"Total facturado: Q{stats[0]:.2f}")
    print(f"Peso promedio: {stats[1]:.2f}")
    print(f"Mayor costo: Q{stats[2]:.2f}")
    print("Envios express:", int(stats[3]))


"""
Solicita datos de entregas, audita su cumplimiento del SLA y muestra el diagnóstico.
"""
def modulo3():
    print("Cantidad de entregas a auditar: ", end="")
    n = leer()
    if n is None or n < 1:
        print("Cantidad invalida.")
        return

    entregas = []
    i = 1
    while i <= int(n):
        entrega = [0, 0, 0, 0, 0]
        entrega[0] = float(i)

        print("Entrega", i, "- horas estimadas: ", end="")
        horas_estimadas = leer()
        print("Entrega", i, "- horas reales: ", end="")
        horas_reales = leer()

        if (horas_estimadas is None or horas_reales is None or
                horas_estimadas <= 0 or horas_reales <= 0):
            print("Valores invalidos, intente de nuevo.")
            continue

        entrega[1] = horas_estimadas
        entrega[2] = horas_reales
        entregas.append(entrega)
        i += 1

    auditadas = auditoria(entregas)
    for e in auditadas:
        resultado = "CUMPLE" if e[3] == 1 else "NO CUMPLE"
        print(f"Entrega {int(e[0])}: {resultado:<10} (desv. {e[4]:+0.2f}h)")

    diag = diagnostico(auditadas)
    print(f"Cumplimiento SLA: {diag[2]:.2f}%")
    print(f"Desviacion promedio: {diag[3]:.2f}h")


"""
Punto de entrada: ejecuta el menú principal hasta que se elige salir.
"""
def main():
    paquetes = []
    opcion = 0

    print("Bienvenido al Sistema de paqueteria de LogiTech!")
    while opcion != 4:
        menu()
        print("Selecciona una opcion: ", end="")
        op = leer()
        opcion = int(op) if op is not None else 0
        limpiarConsola()

        if opcion == 1:
            modulo1(paquetes)
        elif opcion == 2:
            modulo2(paquetes)
        elif opcion == 3:
            modulo3()
        elif opcion == 4:
            print("Saliendo del sistema...")
        else:
            print("Selecciona una opcion valida")


main()
