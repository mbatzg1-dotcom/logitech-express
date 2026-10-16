# Logitech Express

Sistema algorítmico para automatizar la gestión de envíos de **LogiTech Express**. El proyecto aborda el procesamiento
de paquetes, el cálculo de tarifas y la auditoría de tiempos de entrega, reduciendo errores manuales y facilitando el
análisis de las operaciones.

> **Objetivo:** desarrollar un sistema robusto y modular que automatice el cálculo de tarifas, la validación de paquetes
> y la generación de estadísticas operativas.

## Contenido

- [Estructura del proyecto](#estructura-del-proyecto)
- [Requerimientos](#requerimientos)
    - [Módulo 1: Registro y tarificación](#módulo-1-registro-y-tarificación-individual)
    - [Módulo 2: Procesamiento por lotes](#módulo-2-procesamiento-por-lotes-y-estadísticas)
    - [Módulo 3: Diagnóstico y auditoría](#módulo-3-diagnóstico-y-auditoría-de-eficiencia)
- [Diagrama de flujo](#diagrama-de-flujo)

## Estructura del proyecto

| Ruta               | Contenido                                                       |
|--------------------|-----------------------------------------------------------------|
| `doc/`             | Documentación técnica, diagramas de flujo y manuales de usuario |
| `logitech-c++/`    | Código fuente en C++                                            |
| `logitech-python/` | Código fuente en Python                                         |
| `README.md`        | Descripción del proyecto, requerimientos y enlaces a recursos   |

## Requerimientos

### Módulo 1: Registro y tarificación individual

#### Ingreso de datos

Solicitar la siguiente información para cada envío:

- ID del paquete.
- Tipo de destino: nacional o internacional.
- Peso en kg.
- Tipo de servicio: estándar o express.
- Si requiere seguro.

#### Validación

- Usar un bucle `while` para garantizar que el peso sea estrictamente positivo (`> 0`).
- Validar que las opciones seleccionadas en los menús sean válidas.

#### Cálculo de la tarifa

Crear una función `calcular_tarifa()` que determine el costo total con estas reglas:

| Concepto         | Regla                                                        |
|------------------|--------------------------------------------------------------|
| Tarifa base      | Q50.00 para destino nacional; Q250.00 para internacional     |
| Recargo por peso | Si supera los 10 kg, sumar Q50.00 por cada kg adicional      |
| Servicio express | Aumentar un 30 % sobre la tarifa base y el recargo acumulado |
| Seguro opcional  | Aumentar un 5 % sobre el total calculado hasta ese momento   |

### Módulo 2: Procesamiento por lotes y estadísticas

Simular un turno de trabajo en el que el operador procese varios paquetes consecutivamente en una sola sesión iterativa.

Durante la sesión, calcular:

- El monto total facturado.
- El peso promedio procesado.
- El paquete con el mayor costo.
- La cantidad de envíos express solicitados.

**Descuento corporativo:** aplicar un descuento del 10 % a las tarifas de cada paquete si el total antes del descuento supera Q1,500.00
**o** si se procesan 10 paquetes o más.

### Módulo 3: Diagnóstico y auditoría de eficiencia

Recibir las horas de tránsito estimadas y reales de una lista de entregas, y determinar si cada servicio cumplió con el
indicador **SLA** (*Service Level Agreement*).

## Diagrama de flujo

[Ver los diagramas de flujo del programa C++](logitech-c++/README.md#diagramas-de-flujo)
