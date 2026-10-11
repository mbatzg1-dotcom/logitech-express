// logitech-c++.cpp: define el punto de entrada de la aplicación.
//

#include "logitech-c++.h"

using namespace std;

// Declaracion de funciones
void Menu();
void limpiarConsola();


int main()
{
	int opcion = 0;
	int id = 0;
	int internacional = 0;
	int peso = 0;
	int express = 0;
	int tarifa = 0;
	int total = 0;
	int opcion = 0;
    cout << "Bienvenido al Sistema de paqueteria de LogiTech!" << endl; 
    do {
    	Menu();
    	cout << "Selecciona una opcion: " << endl;
    	cin >> opcion;
    	switch(opcion)
		{
			case 1: // Ingreso Modulo 1
				limpiarConsola();
				// 1. Solicitar al usuario que ingrese el ID del paquete, el peso, si es internacional o no, y si es express o no.
				cout << "Bienvenido a Logitech Express" << endl;
				cout << "En este programa, puede ingresar los detalles de su paquete y calcular la tarifa correspondiente." << endl;
				cout << "Ingrese los detalles de su paquete a continuacion:" << endl;
				do {
					// Ingresar nuevo paquete
					cout << "Ingrese 1 para ingresar un nuevo paquete, o 5 para salir y calcular la tarifa del paquete: " << endl;
					cout << "Ingrese 5 para salir y calcular la tarifa del paquete: " << endl;
					cin >> opcion;
					// Validar la opcion ingresada
					if (opcion == 1) {
						cout << "Ingrese el ID del paquete: " << endl;
						cin >> id;
						cout << "Ingrese el peso del paquete: " << endl;
						cin >> peso;
						cout << "Ingrese 1 si es internacional, 0 si no lo es: " << endl;
						cin >> internacional;
						cout << "Ingrese 1 si es express, 0 si no lo es: " << endl;
						cin >> express;
						}
						if (opcion != 1 && opcion != 5) {
							cout << "Opcion invalida. Por favor, ingrese 1 para ingresar un nuevo paquete, o 5 para salir y calcular la tarifa del paquete." << endl;
							}
						
				} while (opcion != 5);
					cout << "Ingrese la tarifa del paquete: " << endl;
					cin >> tarifa;
				break;
			case 2: // Ingreso Modulo 2
				limpiarConsola();
				break;
			case 3: // Ingreso Modulo3
				limpiarConsola();
				break;
			case 4: // Salida del sistema
                limpiarConsola();
                cout << "Saliendo del sistema..." << endl;
                break;
			default:
				limpiarConsola();
				cout << "Selecciona una opcion valida" << endl;
				break;
		} 
	} while (opcion != 4);
	return 0;
}

// Definiciones de funciones
void Menu() {
	cout <<"----------------------------------------------------" << endl;
	cout << "1- Registrar y Consultar tarifas" << endl;
	cout << "2- Revision de lotes y estadisticas" << endl;
	cout << "3- Auditoria y Diagnostico de eficiencia" << endl;
	cout << "4- Salir del sistema" << endl;
	cout <<"----------------------------------------------------" << endl;
}

void limpiarConsola() {
    // Código ANSI para borrar la pantalla y mover el cursor al inicio
    cout << "\033[2J\033[1;1H";
}
