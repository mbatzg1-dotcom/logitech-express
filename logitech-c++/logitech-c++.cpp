#include <iostream>
#include <string>

using namespace std;

// Declaracion de funciones
void Menu();
void limpiarConsola();

void RegistrarPaquete(int NumeroPaquete, int id[],
    string destino[], double peso[],
    string tipo_servicio[], string seguro[], double tarifaBase [], double total[],
    int nuevoId, string nuevoDestino, double nuevoPeso,
    string nuevoServicio, string nuevoSeguro, double nuevoTarifaBase, double nuevoTotal);

int main()
{
    // Constantes
    const int MaximoPaquetes = 10; // cantidad maxima de paquetes a resgistar

    // Variables flexibles de menu
	int opcion, menuOpcion, subOpcion, contador = 0;
	string guardar, SubOpcion_String = "";

	// Variables para arreglo bidimensional de registro de paqutes
	int id[MaximoPaquetes];
	string destino[MaximoPaquetes];
	double peso[MaximoPaquetes];
	string tipo_servicio[MaximoPaquetes];
	string seguro[MaximoPaquetes];
	double tarifaBase[MaximoPaquetes];
	double total[MaximoPaquetes];

	int id_Temporal = 0;
	string destino_Temporal = "";
	double peso_Temporal = 0.0;
	string tipo_servicio_Temporal = "";
	string seguro_Temporal = "";

	// Variables para cotizaciones
	double Recargos = 0.0;
	double tarifaBase_Temporal = 0.0;
	double total_Temporal = 0.0;

    do {
    	Menu();
        cout << "Bienvenido al Sistema de paqueteria de Logitech Express" << endl;
    	cout << "Selecciona una opcion: " << endl;
    	cin >> menuOpcion;
    	switch(menuOpcion)
		{
			case 1: // Ingreso Modulo 1
				limpiarConsola();
				do {
                    cout << "Modulo 1 - Sistema de Registro y Tarificacion" << endl;
                    cout << "----------------------------------------------------" << endl;
                    cout << "Este modulo le permite ingresar los detalles de su paquete y calcular su tarifa." << endl;
                    cout << " " << endl;
                    cout << "Seleccione una opcion:" << endl;
                    cout << "----------------------------------------------------" << endl;
                    cout << "1- Ingresar nuevo paquete" << endl;
                    cout << "2- Menu Principal" << endl;
					cin >> opcion;
					// Validar la opcion ingresada
					if (opcion == 1) {
					    cout << "----------------------------------------------------" << endl;
						cout << "- Ingrese el ID del paquete: " << endl;
						cin >> id_Temporal;
						do {
						    cout << "Ingrese el destino: " << endl;
							cout << "1 - Internacional" << endl;
							cout << "2 - Nacional" << endl;
						    cin >> subOpcion;
						    if (subOpcion == 1)
						    {
								destino_Temporal =  "Internacional";
								tarifaBase_Temporal = 250;
							}
					        else if (subOpcion == 2)
							{
							    destino_Temporal =  "Nacional";
								tarifaBase_Temporal = 50;
							}
						    else {
						        cout << "- Valor incorrecto! Intente de nuevo \n." << endl;
							}
						} while(subOpcion != 1 && subOpcion != 2);

						do {
						    cout << "Ingrese el peso del paquete (lbs) : " << endl;
							cin >> peso_Temporal;
							if (peso_Temporal > 10) {
							    // Si Peso supera 10 lb entonces + Q50.00 por cada libra adicional
							    Recargos = (peso_Temporal - 10) * 50.00;
							}
						} while (peso_Temporal <= 0);

						do {
						    cout << "Ingrese el tipo de servicio: " << endl;
							cout << "1 - Estandar" << endl;
							cout << "2 - Express" << endl;
						    cin >> subOpcion;
						    if (subOpcion == 1)
						    {
								tipo_servicio_Temporal =  "Estandar";
								total_Temporal = tarifaBase_Temporal + Recargos;
							}
					        else if (subOpcion == 2)
							{
							    // Si es Express: +30% sobre base + recargo acumulado
							    tipo_servicio_Temporal =  "Express";
								total_Temporal = (tarifaBase_Temporal + Recargos) * 1.30;
							}
						    else {
						        cout << "- Valor incorrecto! Intente de nuevo \n." << endl;
							}
						} while(subOpcion != 1 && subOpcion != 2);

						do {
						    cout << "Desea contratar seguro? (s/n): " << endl;
							cin >> SubOpcion_String;
							if (SubOpcion_String == "s" || SubOpcion_String == "S") {
							    seguro_Temporal = "Con Seguro";
								// Si tiene seguro: +5% sobre el subtotal calculado
								total_Temporal = total_Temporal * 1.05;
							}
							else if (SubOpcion_String == "n" || SubOpcion_String == "N") {
							    seguro_Temporal = "Sin Seguro";
							}
							else {
							    cout << "- Valor incorrecto! Intente de nuevo \n" << endl;
							}
						} while (SubOpcion_String != "s" && SubOpcion_String != "S" &&
						SubOpcion_String != "n" && SubOpcion_String != "N");

						cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" << endl;
						cout << "Destino: " << destino_Temporal << endl;
						cout << "Servicio: " << tipo_servicio_Temporal << endl;
						cout << "Tarifa base: Q" << tarifaBase_Temporal << endl;
						cout << "Recargo por peso: Q" << Recargos << endl;
						cout << "Seguro: " << seguro_Temporal << endl;
						cout << "TOTAL A PAGAR: Q" << total_Temporal << endl;
						cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" << endl;
						cout << "Desea guardar este presupuesto? (s/n): ";
						cin >> guardar;
						if (guardar == "s" || guardar == "S") {
						    // Realizando Guardado de paqueteria en Arreglo
                            if (contador < MaximoPaquetes) {
                                RegistrarPaquete(
                                    contador, id, destino, peso,
                                    tipo_servicio, seguro, tarifaBase, total,
                                    id_Temporal, destino_Temporal, peso_Temporal,
                                    tipo_servicio_Temporal, seguro_Temporal,
                                    tarifaBase_Temporal, total_Temporal
                                );
                                contador++; // conservando la posiciones de paquetes registardos
                                cout << "Presupuesto guardado." << endl;
                            }
                            else {
                                cout << "No hay espacio para registrar mas paquetes." << endl;
                            }
						}
						// Reiniciando varibales temporales
						id_Temporal = 0;
						destino_Temporal = "";
						peso_Temporal = 0.0;
						tipo_servicio_Temporal = "";
						seguro_Temporal = "";

						Recargos = 0.0;
						tarifaBase_Temporal = 0.0;
						total_Temporal = 0.0;

						SubOpcion_String = "";
						guardar = "";
					}
					else if (opcion != 1 && opcion != 2) {
						cout << "Opcion invalida! Intente de nuevo." << endl;
					}
				} while (opcion != 2);
				limpiarConsola();
				break;
			case 2: // Ingreso Modulo 2
				limpiarConsola();
				break;
			case 3: // Ingreso Modulo 3
				limpiarConsola();
				break;
			case 4: // Salida del sistema
                limpiarConsola();
                cout << "Saliendo del sistema..." << endl;
                break;
			default:
				limpiarConsola();
				cout << "-! Selecciona una opcion valida" << endl;
				break;
		}
	} while (menuOpcion != 4);
	return 0;
}

// Definiciones de funciones
void Menu() {
    cout << "Seleccione una opcion:" << endl;
	cout << "----------------------------------------------------" << endl;
	cout << "1 - Registrar y Consultar tarifas" << endl;
	cout << "2 - Revision de lotes y estadisticas" << endl;
	cout << "3 - Auditoria y Diagnostico de eficiencia" << endl;
	cout << "4 - Salir del sistema" << endl;
	cout << "----------------------------------------------------" << endl;
}

void limpiarConsola() {
    // Código ANSI para borrar la pantalla y mover el cursor al inicio
    cout << "\033[2J\033[1;1H";
}

void RegistrarPaquete(int NumeroPaquete, int id[], string destino[],
    double peso[], string tipo_servicio[], string seguro[], double tarifaBase[], double total[],
    int nuevoId, string nuevoDestino, double nuevoPeso,
    string nuevoServicio, string nuevoSeguro, double nuevoTarifaBase, double nuevoTotal)
{
    // Registrando datos en arreglos undimensionales
    id[NumeroPaquete] = nuevoId;
    destino[NumeroPaquete] = nuevoDestino;
    peso[NumeroPaquete] = nuevoPeso;
    tipo_servicio[NumeroPaquete] = nuevoServicio;
    seguro[NumeroPaquete] = nuevoSeguro;
    tarifaBase[NumeroPaquete] = nuevoTarifaBase;
    total[NumeroPaquete] = nuevoTotal;
}
