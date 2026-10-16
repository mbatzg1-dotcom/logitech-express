//
// Created by Standard on 15/10/2026.
//

#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

/**
 * Valida que todos los valores del paquete sean positivos.
 * @param paquete Vector de entrada:
 * 0: id
 * 1: destino( 1 = nacional, 2 = internacional)
 * 2: peso
 * 3: express( 1 = si, 2 = no)
 * 4: seguro( 1 = si, 2 = no)
 * 5: tarifa
 * @return true si todos los valores recibidos son positivos; false si alguno no lo es.
 **/
bool validar(const std::vector<float> &paquete) {
    for (const float col: paquete) if (col <= 0) return false;
    return true;
}

/**
 * Calcula la tarifa de envío del paquete.
 * @param paquete Vector de entrada:
 * 0: id
 * 1: destino( 1 = nacional, 2 = internacional)
 * 2: peso
 * 3: express( 1 = si, 2 = no)
 * 4: seguro( 1 = si, 2 = no)
 * 5: tarifa
 * @return Vector con la tarifa calculada en el último elemento.
 **/
std::vector<float> tarifa(const std::vector<float> &paquete) {
    // Copia del paquete para no modificar el original
    // El vector de entrada tiene 6 elementos, el último es la tarifa que se calculará
    std::vector<float> paq = paquete;

    // Tarifa base por destino (nacional = 50, internacional = 250)
    if (paquete[1] == 1)paq[5] = 50;
    else if (paquete[1] == 2) paq[5] = 250;
    else paq[5] = 0;

    // Tarifa adicional por peso (si el peso es mayor a 10kg, se cobra 50 por cada kg adicional)
    if (paquete[2] > 10) {
        float dif = paquete[2] - 10;
        paq[5] = paq[5] + (dif * 50); // suma 50 por cada kg adicional
    }
    // Tarifa adicional por express (si es express, se incrementa la tarifa en un 30%)
    if (paquete[3] == 1) paq[5] = paq[5] * 1.3f;

    // Tarifa adicional por seguro (si tiene seguro, se incrementa la tarifa en un 5%)
    if (paquete[4] == 1) paq[5] = paq[5] * 1.05f;

    return paq;
}

/**
 * Calcula la tarifa de un lote de paquetes.
 * @param paquetes Vector de paquetes, cada paquete es un vector de 6 elementos.
 * @return Copia del lote con la tarifa calculada en el último elemento de cada paquete.
 */
std::vector<std::vector<float> > lote(const std::vector<std::vector<float> > &paquetes) {
    // Vector de salida con las tarifas calculadas para cada paquete
    std::vector<std::vector<float> > tarifas;

    // Calcula la tarifa para cada paquete y la agrega al vector de salida
    for (const auto &paquete: paquetes) {
        tarifas.push_back(tarifa(paquete));
    }

    return tarifas;
}

/**
 * Aplica un descuento del 10% si hay al menos 10 paquetes o el total de las tarifas supera Q1500.
 * @param paquetes Vector de paquetes, cada paquete es un vector de 6 elementos.
 * @return Copia del lote con las tarifas calculadas y el descuento aplicado si corresponde.
 */
std::vector<std::vector<float> > descuento(const std::vector<std::vector<float> > &paquetes) {
    // Calcula las tarifas de los paquetes
    std::vector<std::vector<float> > tarifas = lote(paquetes);

    // Calcula el monto total de envio
    float total = 0;
    for (const auto &tarifa: tarifas) total += tarifa[5];

    // Aplica el descuento si se cumplen las condiciones
    if (paquetes.size() >= 10 || total > 1500) {
        for (auto &tarifa: tarifas) tarifa[5] = tarifa[5] * 0.9f;
    }

    return tarifas;
}

/**
 * Calcula estadísticas de un lote de paquetes.
 * @param paquetes Vector de paquetes, cada paquete es un vector de 6 elementos.
 * @return Vector de cuatro valores: [total facturado, peso promedio, mayor costo,
 * cantidad de envíos express].
 */
std::vector<float> estadisticas(const std::vector<std::vector<float> > &paquetes) {
    // Vector de salida con las estadísticas
    std::vector<float> stats(4, 0);

    // Calcula las estadísticas
    for (const auto &paquete: paquetes) {
        // Suma el costo total
        stats[0] += paquete[5];
        // Suma el peso total
        stats[1] += paquete[2];
        // Actualiza el mayor costo
        if (paquete[5] > stats[2]) stats[2] = paquete[5];
        // Cuenta la cantidad de envíos express
        if (paquete[3] == 1) stats[3]++;
    }
    // Calcula el peso promedio
    stats[1] /= paquetes.size();

    return stats;
}

/**
 * Calcula si una entrega cumple con el SLA y la desviación en horas.
 * @param entrega Vector de entrada:
 * 0: id
 * 1: horas estimadas
 * 2: horas reales
 * 3: cumple SLA (1 = si, 2 = no)
 * 4: desviación en horas (real - estimada)
 * @return Vector con la información de la entrega y el resultado del SLA.
 */
std::vector<float> sla(const std::vector<float> &entrega) {
    // Copia del vector de entrada para no modificar el original
    std::vector<float> ent = entrega;

    // Calcula si cumple SLA y la desviación en horas
    ent[3] = (entrega[2] <= entrega[1]) ? 1.0f : 2.0f;

    // Calcula la desviación en horas (real - estimada)
    ent[4] = entrega[2] - entrega[1];
    return ent;
}

/**
 * Audita un lote de entregas y calcula el SLA para cada una.
 * @param entregas Vector de entregas; cada una contiene cinco posiciones: id, horas estimadas,
 * horas reales, resultado SLA y desviación.
 * @return Vector de entregas con la información del SLA calculada.
 */
std::vector<std::vector<float> > auditoria(const std::vector<std::vector<float> > &entregas) {
    // Vector de salida con los resultados de la auditoria
    std::vector<std::vector<float> > resultado;

    // Calcula el SLA para cada entrega y lo agrega al vector de salida
    for (const auto &entrega: entregas) resultado.push_back(sla(entrega));

    return resultado;
}

/**
 * Calcula el diagnostico de eficiencia de un lote de entregas auditadas.
 * @param auditadas Vector de entregas auditadas, cada entrega es un vector de 5 elementos.
 * @return Vector de cuatro valores: [cantidad que cumplen, cantidad que no cumplen,
 * porcentaje de cumplimiento, desviación promedio en horas].
 */
std::vector<float> diagnostico(const std::vector<std::vector<float> > &auditadas) {
    // Vector de salida con el diagnostico
    std::vector<float> diag(4, 0);

    // Si no hay entregas auditadas, devuelve el vector con ceros
    if (auditadas.empty()) return diag;
    for (const auto &entrega: auditadas) {
        // Cuenta las entregas que cumplen y las que no cumplen
        if (entrega[3] == 1) diag[0]++;

            // Si no cumple, incrementa el contador de entregas que no cumplen
        else diag[1]++;

        // Suma la desviación en horas para calcular el promedio después
        diag[3] += entrega[4];
    }

    // Calcula el porcentaje de cumplimiento y la desviación promedio
    const auto total = static_cast<float>(auditadas.size());
    // Porcentaje de cumplimiento = (entregas que cumplen / total) * 100
    diag[2] = diag[0] * 100 / total;
    // Desviación promedio = (suma de desviaciones / total)
    diag[3] /= total;

    return diag;
}

/**
 * Punto de extensión para limpiar la consola; actualmente no realiza ninguna acción.
 */
void limpiarConsola() {
    // system("cls");
}

/**
 * Muestra las opciones principales del sistema en la consola.
 */
void menu() {
    std::cout << "----------------------------------------------------\n"
            << "1- Registrar y Consultar tarifas\n"
            << "2- Revision de lotes y estadisticas\n"
            << "3- Auditoria y Diagnostico de eficiencia\n"
            << "4- Salir del sistema\n"
            << "----------------------------------------------------\n";
}

/**
 * Lee un valor flotante desde la entrada estándar y lo asigna a la referencia proporcionada.
 * @param valor Referencia a un float donde se almacenará el valor leído.
 * @return true si la lectura fue exitosa, false si hubo un error de entrada.
 */
bool leer(float &valor) {
    if (std::cin >> valor) return true;
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return false;
}

/**
 * Lee los datos de un paquete desde la entrada estándar y los almacena en un vector.
 * @param paquete Vector donde se almacenarán los datos del paquete.
 * @return true si todos los datos fueron leídos correctamente y son válidos, false en caso contrario.
 */
bool leerPaquete(std::vector<float> &paquete) {
    paquete.assign(6, 0);
    std::cout << "ID del paquete: ";
    const bool ok1 = leer(paquete[0]);
    std::cout << "Destino (1 = nacional, 2 = internacional): ";
    const bool ok2 = leer(paquete[1]);
    std::cout << "Peso (kg): ";
    const bool ok3 = leer(paquete[2]);
    std::cout << "Express (1 = si, 2 = no): ";
    const bool ok4 = leer(paquete[3]);
    std::cout << "Seguro (1 = si, 2 = no): ";
    const bool ok5 = leer(paquete[4]);

    return ok1 && ok2 && ok3 && ok4 && ok5 &&
           validar({paquete[0], paquete[1], paquete[2], paquete[3], paquete[4]}) &&
           (paquete[1] == 1 || paquete[1] == 2) &&
           (paquete[3] == 1 || paquete[3] == 2) &&
           (paquete[4] == 1 || paquete[4] == 2);
}

/**
 * Registra paquetes individuales o por lote y permite consultar sus tarifas.
 * Los paquetes válidos se agregan al vector recibido.
 * @param paquetes Vector donde se almacenan los paquetes registrados.
 */
void modulo1(std::vector<std::vector<float> > &paquetes) {
    int opcion = 0;
    do {
        std::cout << "1- Registrar paquete individual\n2- Registrar lote de paquetes\n"
                << "3- Consultar tarifas\n5- Volver al menu\nOpcion: ";
        float op = 0;
        if (!leer(op)) op = -1;
        opcion = static_cast<int>(op);

        if (opcion == 1) {
            std::vector<float> paquete;
            if (leerPaquete(paquete)) {
                paquetes.push_back(paquete);
                std::cout << "Paquete registrado.\n";
            } else {
                std::cout << "Datos invalidos, paquete descartado.\n";
            }
        } else if (opcion == 2) {
            float n = 0;
            std::cout << "Cantidad de paquetes a procesar: ";
            if (!leer(n) || n < 1) {
                std::cout << "Cantidad invalida.\n";
                continue;
            }
            const int total = static_cast<int>(n);
            for (int i = 1; i <= total; ++i) {
                std::vector<float> paquete;
                std::cout << "--- Paquete " << i << " de " << total << " ---\n";
                if (leerPaquete(paquete)) {
                    paquetes.push_back(paquete);
                } else {
                    std::cout << "Datos invalidos, intente de nuevo.\n";
                    --i;
                }
            }
            std::cout << "Lote registrado: " << paquetes.size() << " paquetes.\n";
        } else if (opcion == 3) {
            if (paquetes.empty()) {
                std::cout << "No hay paquetes registrados.\n";
                continue;
            }
            std::cout << std::fixed << std::setprecision(2);
            std::cout << std::left << std::setw(10) << "Paquete" << std::right << std::setw(12) << "Tarifa" << "\n";
            for (const auto &p: descuento(paquetes))
                std::cout << std::left << std::setw(10) << static_cast<int>(p[0])
                        << std::right << std::setw(12) << p[5] << "\n";
        } else if (opcion != 5) {
            std::cout << "Opcion invalida.\n";
        }
    } while (opcion != 5);
}

/**
 * Muestra las estadísticas de los paquetes registrados.
 * @param paquetes Paquetes registrados; si está vacío, se informa que no hay datos.
 */
void modulo2(const std::vector<std::vector<float> > &paquetes) {
    if (paquetes.empty()) {
        std::cout << "No hay paquetes registrados. Use el modulo 1.\n";
        return;
    }
    const auto lotes = descuento(paquetes);
    const auto stats = estadisticas(lotes);
    std::cout << std::fixed << std::setprecision(2)
            << "Total facturado: Q" << stats[0] << "\n"
            << "Peso promedio: " << stats[1] << "\n"
            << "Mayor costo: Q" << stats[2] << "\n"
            << "Envios express: " << static_cast<int>(stats[3]) << "\n";
}

/**
 * Solicita datos de entregas, audita su cumplimiento del SLA y muestra el diagnóstico.
 */
void modulo3() {
    float n = 0;
    std::cout << "Cantidad de entregas a auditar: ";
    if (!leer(n) || n < 1) {
        std::cout << "Cantidad invalida.\n";
        return;
    }
    std::vector<std::vector<float> > entregas;
    for (int i = 1; i <= static_cast<int>(n); ++i) {
        std::vector<float> entrega(5, 0);
        entrega[0] = static_cast<float>(i);
        std::cout << "Entrega " << i << " - horas estimadas: ";
        const bool ok1 = leer(entrega[1]);
        std::cout << "Entrega " << i << " - horas reales: ";
        const bool ok2 = leer(entrega[2]);
        if (!ok1 || !ok2 || entrega[1] <= 0 || entrega[2] <= 0) {
            std::cout << "Valores invalidos, intente de nuevo.\n";
            --i;
            continue;
        }
        entregas.push_back(entrega);
    }
    const auto auditadas = auditoria(entregas);
    std::cout << std::fixed << std::setprecision(2);
    for (const auto &e: auditadas)
        std::cout << "Entrega " << static_cast<int>(e[0]) << ": " << std::left << std::setw(10)
                << (e[3] == 1 ? "CUMPLE" : "NO CUMPLE") << std::right
                << " (desv. " << std::showpos << e[4] << std::noshowpos << "h)\n";
    const auto diag = diagnostico(auditadas);
    std::cout << "Cumplimiento SLA: " << diag[2] << "%\n"
            << "Desviacion promedio: " << diag[3] << "h\n";
}

/**
 * Punto de entrada: ejecuta el menú principal hasta que se elige salir.
 * @param argc Cantidad de argumentos de línea de comandos (no utilizados).
 * @param argv Argumentos de línea de comandos (no utilizados).
 * @return 0 al finalizar normalmente.
 */
int main(int argc, char *argv[]) {
    std::vector<std::vector<float> > paquetes;
    int opcion = 0;

    std::cout << "Bienvenido al Sistema de paqueteria de LogiTech!\n";
    do {
        menu();
        std::cout << "Selecciona una opcion: ";
        float op = 0;
        opcion = leer(op) ? static_cast<int>(op) : 0;
        limpiarConsola();

        switch (opcion) {
            case 1:
                modulo1(paquetes);
                break;
            case 2:
                modulo2(paquetes);
                break;
            case 3:
                modulo3();
                break;
            case 4:
                std::cout << "Saliendo del sistema...\n";
                break;
            default:
                std::cout << "Selecciona una opcion valida\n";
                break;
        }
    } while (opcion != 4);

    return 0;
}
