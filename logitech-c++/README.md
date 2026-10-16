# LogiTech Express

Programa de consola en C++ para registrar paquetes, calcular tarifas y auditar entregas según su SLA.

## Compilar y ejecutar

Desde esta carpeta, compila con un compilador compatible con C++11:

```bash
g++ -std=c++11 logitech-v1.cpp -o logitech-express
```

En Windows, ejecuta:

```powershell
.\logitech-express.exe
```

## Funciones

- Registrar paquetes individualmente o en lote, consultar tarifas y ver estadísticas.
- Auditar entregas comparando las horas estimadas con las reales.

## Reglas principales

- Tarifa base: Q50 para destino nacional y Q250 para internacional.
- Por cada kilogramo por encima de 10 kg se agregan Q50.
- Express multiplica la tarifa por 1.30; el seguro la multiplica por 1.05.
- Se aplica un descuento de 10% a cada tarifa si hay 10 o más paquetes o si el total antes del descuento supera Q1500.
- Una entrega cumple el SLA si las horas reales son menores o iguales a las estimadas.

## Diagramas de flujo

Los diagramas están escritos en Mermaid, formato que draw.io puede importar como diagramas editables. Reflejan la lógica actual del programa; los diagramas anteriores en `../doc/diagrama` contienen reglas distintas.

### Menú principal

```mermaid
flowchart TD
    A([Inicio]) --> B[Mostrar menú]
    B --> C[Leer opción]
    C --> D{Opción}
    D -->|1| E[Registrar paquetes o consultar tarifas]
    D -->|2| F[Mostrar estadísticas del lote]
    D -->|3| G[Auditar entregas y mostrar diagnóstico SLA]
    D -->|4| H([Salir])
    D -->|Otra| I[Mostrar opción inválida]
    E --> B
    F --> B
    G --> B
    I --> B
```

### Registro y cálculo de tarifas

```mermaid
flowchart TD
    A([Módulo de paquetes]) --> B{Acción}
    B -->|Registrar individual| C[Leer datos del paquete]
    C --> D{Datos válidos?}
    D -->|No| C
    D -->|Sí| E[Guardar paquete]
    E --> B
    B -->|Registrar lote| F[Leer cantidad de paquetes]
    F --> G{Cantidad mayor que cero?}
    G -->|No| B
    G -->|Sí| H[Leer datos del siguiente paquete]
    H --> I{Datos válidos?}
    I -->|No| H
    I -->|Sí| J[Guardar paquete]
    J --> K{Quedan paquetes del lote?}
    K -->|Sí| H
    K -->|No| B
    B -->|Consultar tarifas| L{Hay paquetes registrados?}
    L -->|No| B
    L -->|Sí| M[Calcular tarifa base:<br/>nacional Q50 o internacional Q250]
    M --> N{Peso mayor a 10 kg?}
    N -->|Sí| O[Sumar Q50 por cada kg excedente]
    N -->|No| P{¿Express?}
    O --> P
    P -->|Sí| Q[Multiplicar por 1.30]
    P -->|No| R{¿Seguro?}
    Q --> R
    R -->|Sí| S[Multiplicar por 1.05]
    R -->|No| T[Conservar tarifa calculada]
    S --> U{¿10 o más paquetes<br/>o total mayor a Q1500?}
    T --> U
    U -->|Sí| V[Aplicar 10% de descuento<br/>a cada tarifa]
    U -->|No| W[Conservar tarifas]
    V --> X[Mostrar tarifas]
    W --> X
    X --> B
    B -->|Volver al menú| Y([Fin del módulo])
```

### Estadísticas del lote

```mermaid
flowchart TD
    A([Elegir estadísticas]) --> B{Hay paquetes registrados?}
    B -->|No| C[Informar que no hay paquetes]
    B -->|Sí| D[Calcular tarifas y aplicar descuento<br/>si corresponde]
    D --> E[Sumar tarifas y pesos;<br/>buscar mayor tarifa y contar express]
    E --> F[Mostrar total, peso promedio,<br/>mayor costo y envíos express]
    C --> G([Volver al menú])
    F --> G
```

### Auditoría SLA

```mermaid
flowchart TD
    A([Iniciar auditoría]) --> B[Leer cantidad de entregas]
    B --> C{Cantidad válida?}
    C -->|No| D[Informar cantidad inválida]
    C -->|Sí| E[Leer horas estimadas y reales]
    E --> F{Ambos valores positivos<br/>y lectura válida?}
    F -->|No| E
    F -->|Sí| G{¿Horas reales ≤ estimadas?}
    G -->|Sí| H[Marcar CUMPLE]
    G -->|No| I[Marcar NO CUMPLE]
    H --> J[Calcular desviación:<br/>reales - estimadas]
    I --> J
    J --> K{¿Faltan entregas?}
    K -->|Sí| E
    K -->|No| L[Calcular porcentaje de cumplimiento<br/>y desviación promedio]
    L --> M[Mostrar resultados y diagnóstico]
    D --> N([Volver al menú])
    M --> N
```
