"""
Sistema de Gestión y Diagnóstico de Operaciones 'LogiTech Express'
Moneda Oficial: Quetzales (Q / GTQ)
 - Moneda explicitada como Quetzales (Q / GTQ) en todas las salidas y diálogos.
 - Servicio Express deshabilitado para envíos Internacionales.
"""

MONEDA_SIMBOLO = "Q"
MONEDA_NOMBRE = "Quetzales"


def calcular_tarifa(destino: int, peso: float, servicio: int, seguro: int) -> float:
    """
    Calcula la tarifa final de un paquete en Quetzales (Q) según las reglas V3.
    - Tarifa Base: Q50.00 (Nacional) / Q250.00 (Internacional)
    - Recargo peso: Q50.00 por lb adicional si es mayor a 10 lbs.
    - Servicio Express (+30%): Exclusivo para destino Nacional (destino == 1).
    - Seguro (+5%): Aplicable opcionalmente sobre el acumulado.
    """
    tarifa_base = 50.0 if destino == 1 else 250.0
    recargo_peso = (peso - 10.0) * 50.0 if peso > 10.0 else 0.0
    
    subtotal1 = tarifa_base + recargo_peso
    
    # Restricción: Servicio Express (+30%) exclusivo para envíos Nacionales
    if destino == 1 and servicio == 2:
        incremento_express = subtotal1 * 0.30
    else:
        incremento_express = 0.0
    
    subtotal2 = subtotal1 + incremento_express
    monto_seguro = subtotal2 * 0.05 if seguro == 1 else 0.0
    
    return subtotal2 + monto_seguro


def leer_entero_valido(prompt: str, min_val: int, max_val: int) -> int:
    """Lee un entero desde la consola asegurando que esté en el rango [min_val, max_val]."""
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Error: Ingrese un entero entre {min_val} y {max_val}.")
        except ValueError:
            print("Error: Entrada no válida. Debe ingresar un número entero.")


def leer_float_positivo(prompt: str) -> float:
    """Lee un número flotante positivo (> 0)."""
    while True:
        try:
            val = float(input(prompt))
            if val > 0:
                return val
            print("Error: El valor debe ser estrictamente mayor a 0.")
        except ValueError:
            print("Error: Entrada no válida. Ingrese un número decimal válido.")


def modulo_tarificacion_individual():
    """Módulo 1: Registro y Tarificación Individual de Envíos en Quetzales."""
    print("\n--- REGISTRO INDIVIDUAL DE ENVÍO (MONEDA: QUETZALES - Q) ---")
    paquete_id = input("Ingrese ID del paquete: ").strip()
    destino = leer_entero_valido(
        f"Tipo de destino (1. Nacional [{MONEDA_SIMBOLO}50.00], 2. Internacional [{MONEDA_SIMBOLO}250.00]): ", 1, 2
    )
    peso = leer_float_positivo("Ingrese el peso en lbs (>0): ")
    
    # Restricción Express para envíos Internacionales
    if destino == 2:
        print("Nota: El servicio Express no está disponible para envíos internacionales. Se asignará servicio Estándar.")
        servicio = 1
    else:
        servicio = leer_entero_valido("Tipo de servicio (1. Estándar, 2. Express [+30%]): ", 1, 2)
        
    seguro = leer_entero_valido("Requiere seguro opcional [+5%] (1. Sí, 2. No): ", 1, 2)

    costo = calcular_tarifa(destino, peso, servicio, seguro)
    print("\n" + "="*50)
    print(f"Paquete ID: {paquete_id}")
    print(f"Tipo Destino: {'Nacional' if destino == 1 else 'Internacional'}")
    print(f"Tipo Servicio: {'Estándar' if servicio == 1 else 'Express'}")
    print(f"Costo Total Calculado: {MONEDA_SIMBOLO}{costo:.2f} {MONEDA_NOMBRE}")
    print("="*50 + "\n")


def modulo_procesamiento_lotes():
    """Módulo 2: Procesamiento por Lotes y Estadísticas en Quetzales (Q)."""
    print("\n--- PROCESAMIENTO POR LOTES (TURNO - MONEDA: QUETZALES) ---")
    cantidad = leer_entero_valido("Ingrese la cantidad de paquetes a procesar: ", 1, 10000)

    total_facturado = 0.0
    suma_peso = 0.0
    max_costo = -1.0
    id_max_costo = ""
    cant_express = 0

    for i in range(1, cantidad + 1):
        print(f"\n--- Paquete {i} de {cantidad} ---")
        paquete_id = input("ID del Paquete: ").strip()
        destino = leer_entero_valido(f"Destino (1. Nacional [{MONEDA_SIMBOLO}50], 2. Internacional [{MONEDA_SIMBOLO}250]): ", 1, 2)
        peso = leer_float_positivo("Peso en lbs (>0): ")
        
        # Restricción Express para envíos Internacionales
        if destino == 2:
            print("Nota: Servicio Express no disponible para envíos Internacionales (asignado Estándar).")
            servicio = 1
        else:
            servicio = leer_entero_valido("Servicio (1. Estándar, 2. Express): ", 1, 2)
            
        seguro = leer_entero_valido("Seguro (1. Sí, 2. No): ", 1, 2)

        costo = calcular_tarifa(destino, peso, servicio, seguro)
        total_facturado += costo
        suma_peso += peso

        if servicio == 2:
            cant_express += 1
        if costo > max_costo:
            max_costo = costo
            id_max_costo = paquete_id

    # Descuento Corporativo (Si supera Q1,500.00 Quetzales o más de 10 paquetes)
    aplica_descuento = (total_facturado > 1500.0 or cantidad > 10)
    descuento = total_facturado * 0.10 if aplica_descuento else 0.0
    gran_total = total_facturado - descuento

    print("\n" + "="*50)
    print("     RESUMEN DEL TURNO OPERATIVO (QUETZALES - GTQ)   ")
    print("="*50)
    print(f"Paquetes Procesados: {cantidad}")
    print(f"Monto Bruto Facturado: {MONEDA_SIMBOLO}{total_facturado:.2f} {MONEDA_NOMBRE}")
    if aplica_descuento:
        print(f"Descuento Corporativo (10%): -{MONEDA_SIMBOLO}{descuento:.2f} {MONEDA_NOMBRE}")
    else:
        print("Descuento Corporativo: N/A")
    print(f"Monto Neto a Cobrar: {MONEDA_SIMBOLO}{gran_total:.2f} {MONEDA_NOMBRE}")
    print(f"Peso Promedio Procesado: {suma_peso / cantidad:.2f} lbs")
    print(f"Envíos Express Solicitados: {cant_express}")
    print(f"Paquete de Mayor Costo: {id_max_costo} ({MONEDA_SIMBOLO}{max_costo:.2f} {MONEDA_NOMBRE})")
    print("="*50 + "\n")


def modulo_auditoria_sla():
    """Módulo 3: Diagnóstico y Auditoría de Eficiencia (SLA)."""
    print("\n--- AUDITORÍA DE TIEMPOS DE ENTREGA (SLA) ---")
    n = leer_entero_valido("Ingrese número de entregas a auditar: ", 1, 1000)

    cumplidos = 0
    for i in range(1, n + 1):
        print(f"\nEntrega #{i}:")
        estimadas = leer_float_positivo("  Horas estimadas: ")
        reales = leer_float_positivo("  Horas reales tomadas: ")

        if reales <= estimadas:
            print("  -> ESTADO: CUMPLIDO (A tiempo)")
            cumplidos += 1
        else:
            print(f"  -> ESTADO: INCUMPLIDO (Retraso de {reales - estimadas:.1f} hrs)")

    porcentaje = (cumplidos / n) * 100.0
    print("\n" + "-"*45)
    print("RESULTADO AUDITORÍA SLA:")
    print(f"Entregas dentro de SLA: {cumplidos} de {n}")
    print(f"Porcentaje de Efectividad Operativa: {porcentaje:.1f}%")
    print("-" * 45 + "\n")


def main():
    while True:
        print("=============================================")
        print("   SISTEMA LOGITECH EXPRESS - MENÚ (V3)      ")
        print("   Moneda Oficial: Quetzales (Q / GTQ)       ")
        print("=============================================")
        print("1. Tarificación de Envío Individual")
        print("2. Procesamiento por Lotes y Estadísticas")
        print("3. Auditoría de Tiempos de Entrega (SLA)")
        print("4. Salir del Sistema")
        print("=============================================")
        
        opcion = leer_entero_valido("Seleccione una opción: ", 1, 4)
        if opcion == 1:
            modulo_tarificacion_individual()
        elif opcion == 2:
            modulo_procesamiento_lotes()
        elif opcion == 3:
            modulo_auditoria_sla()
        elif opcion == 4:
            print("\nSaliendo del sistema LogiTech Express. ¡Buen turno!")
            break


if __name__ == "__main__":
    main()
