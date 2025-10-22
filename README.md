# Problema del Viajante (TSP) - Solución con Métodos de Búsqueda

## Integrantes
- Yohan Michel Pérez Monzon
- Jose Carlos Ledesma Linares

## Descripción del Problema
El Problema del Viajante (TSP, por sus siglas en inglés) es un problema clásico de optimización combinatoria que consiste en encontrar la ruta más corta posible que visite un conjunto de ciudades exactamente una vez y regrese al punto de partida. Este problema es NP-duro, lo que significa que no existe un algoritmo eficiente que encuentre la solución óptima para instancias grandes en tiempo polinomial.

En este proyecto se implementa una solución que aborda dos variantes del problema: la versión genérica del TSP y una variante con restricciones de capacidad, donde un camión con capacidad limitada debe entregar mercancías en varios nodos, regresando al almacén cuando se queda sin stock.

## Estado Actual de la Solución
El proyecto ha sido implementado completamente en Python y ofrece una solución funcional para ambas variantes del TSP. Se han implementado múltiples algoritmos de búsqueda que permiten resolver instancias de diferentes tamaños, desde problemas pequeños hasta instancias con hasta 1000 nodos. La solución incluye una interfaz de consola interactiva que permite al usuario configurar los parámetros del problema, seleccionar el algoritmo de resolución y visualizar los resultados detallados, incluyendo las rutas óptimas, distancias totales y, en la variante con capacidad, el registro de entregas y regresos al almacén.

## Características Principales

### TSP Genérico
- Implementación de tres algoritmos de búsqueda:
  - Fuerza Bruta (para instancias pequeñas, n ≤ 10)
  - Vecino más cercano (algoritmo voraz)
  - Búsqueda local 2-opt (mejora de soluciones)
- Generación de instancias con distancias aleatorias
- Visualización de matrices de distancias y resultados

### TSP con Capacidad
- Modelado de un camión con capacidad limitada
- Gestión de entregas completas y parciales
- Regreso óptimo al almacén cuando el camión se queda sin stock
- Dos algoritmos de resolución:
  - Algoritmo Greedy adaptado
  - Búsqueda Local con restricciones de capacidad
- Registro detallado de entregas y regresos al almacén

### Características Generales
- Sistema de etiquetado de nodos escalable (A, B, ..., Z, AA, AB, ...)
- Manejo de hasta 1000 nodos con etiquetas únicas
- Estimación de tiempos de ejecución según el algoritmo seleccionado
- Posibilidad de cancelar ejecuciones prolongadas
- Generación de informes detallados de las soluciones


