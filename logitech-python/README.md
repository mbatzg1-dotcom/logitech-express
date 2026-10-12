# Logitech Express - Python
# Sistema de Registro y Tarificación de Envíos

Aplicación básica de consola hecha con Python 3. Los envíos se guardan en un archivo CSV y no necesita instalar paquetes externos para ejecutarse.

El programa usa funciones, condicionales, ciclos, diccionarios y bibliotecas estándar de Python. Incluye registro individual, consulta de historial, procesamiento de lotes, auditoría de tarifas y resumen estadístico.

## Reglas de cálculo

1. Base nacional: Q50.00.
2. Base internacional: Q250.00.
3. El peso debe ser mayor que cero.
4. El peso se convierte a libras: 1 kg = 2.20462 lb.
5. Recargo por peso: si la cantidad de libras supera 10, se calcula con `ceil(peso_libras - 10)` y cada libra adicional cuesta Q50.00.
6. Servicio Express: aplica 30 % sobre la tarifa base más el recargo por peso.
7. Seguro: agrega 5 % sobre el subtotal calculado si `requiere_seguro` es verdadero.
8. El total final se redondea a dos decimales.

## Ejecutar desde terminal

Se requiere Python 3. No se crea entorno virtual y no es necesario instalar dependencias para ejecutar la aplicación.

```bash
cd /ruta/al/proyecto/logitech-python
python3 main.py
```

En macOS o Linux también se puede iniciar con el script incluido:

```bash
chmod +x run.sh
./run.sh
```

En Windows, desde PowerShell:

```bash
cd C:\ruta\al\proyecto\logitech-python
py main.py
```

El archivo `data/envios.csv` se crea automáticamente al iniciar. Se puede abrir con un editor de texto o una hoja de cálculo.

## Ejecutar pruebas opcionales

Las pruebas usan `unittest`, que ya viene incluido con Python:

```bash
python3 -m unittest discover -s tests -v
```
