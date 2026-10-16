// logitech-c++.cpp define el punto de entrada de la aplicación y liberias
#include <iostream>
#include <string>

using namespace std;

// Declaracion de funciones
void Menu();
void limpiarConsola();

void RegistrarPaquete(int NumeroPaquete, int id[],
    string destino[], double peso[],
    string tipo_servicio[], string seguro[],
    int nuevoId, string nuevoDestino, double nuevoPeso,
    string nuevoServicio, string nuevoSeguro);

int main()
{
    // Constantes
    const int MaximoPaquetes = 10; // cantidad maxima de paquetes a resgistar

    // Variables de menu y seleccion
	int opcion, menuOpcion, subOpcion, contador = 0;
	string guardar;

	// Variables para arreglo bidimensional de registro de paqutes
	int id[MaximoPaquetes];
	string destino[MaximoPaquetes];
	double peso[MaximoPaquetes];
	string tipo_servicio[MaximoPaquetes];
	string seguro[MaximoPaquetes];

	int id_Temporal = 0;
	string destino_Temporal;
	double peso_Temporal = 0;
	string tipo_servicio_Temporal;
	string seguro_Temporal;
	int tarifa = 0;
	double total = 0;

    do {
    	Menu();
        cout << "Bienvenido al Sistema de paqueteria de Logitech Express" << endl;
    	cout << "Selecciona una opcion: " << endl;
    	cin >> menuOpcion;
    	switch(menuOpcion)
		{
			case 1: // Ingreso Modulo 1
				limpiarConsola();
				cout << "Modulo 1 - Sistema de Registro y Tarificacion" << endl;
				cout << "----------------------------------------------------" << endl;
				cout << "Este modulo le permite ingresar los detalles de su paquete y calcular su tarifa." << endl;
				do {
                    cout << "Seleccione una opcion:" << endl;
                    cout << "1- Ingresar nuevo paquete" << endl;
                    cout << "2- Menu Principal" << endl;
					cin >> opcion;
					// Validar la opcion ingresada
					if (opcion == 1) {
					    cout << "----------------------------------------------------" << endl;
						cout << "- Ingrese el ID del paquete: " << endl;
						cin >> id_Temporal;
						do {
						    cout << "Ingrese 1 si es Internacional o 2 si es Express." << endl;
						    cin >> subOpcion;
						    if (subOpcion == 1)
						    {
								tipo_servicio_Temporal =  "Internacional";
							}
					        else if (subOpcion == 2)
							{
							    tipo_servicio_Temporal =  "Express";
							}
						    else {
						        cout << "- Valor incorrecto! Intente de nuevo." << endl;
							}
						} while(subOpcion != 1 && subOpcion != 2);
						cout << "Ingrese el peso del paquete: " << endl;
						cin >> peso_Temporal;
						cout << "¿Desea guardar este presupuesto? (s/n): ";
						cin >> guardar;
						if (guardar == "s" || guardar == "S") {
                            if (contador < MaximoPaquetes) {
                                RegistrarPaquete(contador, id, destino, peso,
                                            tipo_servicio, seguro, id_Temporal,
                                            destino_Temporal, peso_Temporal,
                                            tipo_servicio_Temporal, seguro_Temporal);
                                contador++;
                                cout << "Presupuesto guardado." << endl;
                            }
                            else {
                                cout << "No hay espacio para registrar mas paquetes." << endl;
                            }
						}
						cout << "Ingrese el destino del paquete: " << endl;
						cin >> destino_Temporal;
						cout << "¿Desea contratar seguro? (s/n): " << endl;
						cin >> seguro_Temporal;
					}
					else if (opcion != 1 && opcion != 2) {
						cout << "Opcion invalida! Intente de nuevo." << endl;
					}
				} while (opcion != 2);
				cout << "Ingrese la tarifa del paquete: " << endl;
				cin >> tarifa;
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
	cout << "----------------------------------------------------" << endl;
	cout << "1- Registrar y Consultar tarifas" << endl;
	cout << "2- Revision de lotes y estadisticas" << endl;
	cout << "3- Auditoria y Diagnostico de eficiencia" << endl;
	cout << "4- Salir del sistema" << endl;
	cout << "----------------------------------------------------" << endl;
}

void limpiarConsola() {
    // Código ANSI para borrar la pantalla y mover el cursor al inicio
    cout << "\033[2J\033[1;1H";
}

void RegistrarPaquete(int NumeroPaquete, int id[], string destino[],
    double peso[], string tipo_servicio[], string seguro[],
    int nuevoId, string nuevoDestino, double nuevoPeso,
    string nuevoServicio, string nuevoSeguro)
{
    // Registrando datos en arreglo bidimensional
    id[NumeroPaquete] = nuevoId;
    destino[NumeroPaquete] = nuevoDestino;
    peso[NumeroPaquete] = nuevoPeso;
    tipo_servicio[NumeroPaquete] = nuevoServicio;
    seguro[NumeroPaquete] = nuevoSeguro;
}
