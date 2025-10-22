import os
import time
import random
from tsp_generico import TSPGenerico
from tsp_capacidad import TSPCapacidad
from utils import validar_entrada, mostrar_matriz, generar_etiquetas


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal del programa"""
    print("\n" + "=" * 60)
    print("      PROBLEMA DEL VIAJANTE (TSP)")
    print("=" * 60)
    print("1. TSP Genérico - Encuentra la ruta más corta visitando")
    print("   todos los nodos exactamente una vez y regresando al inicio")
    print("2. TSP con Capacidad de Camión - Un camión con capacidad")
    print("   limitada debe entregar mercancías en varios nodos")
    print("3. Salir")
    print("=" * 60)


def tsp_generico():
    """Función para el TSP genérico"""
    limpiar_pantalla()
    print("\n--- TSP GENÉRICO ---")
    print("\nEl Problema del Viajante (TSP) consiste en encontrar la ruta")
    print("más corta posible que visite un conjunto de nodos exactamente")
    print("una vez y regrese al nodo de partida.\n")

    # Opciones para el número de nodos
    print("Seleccione cómo determinar el número de nodos:")
    print("1. Ingresar manualmente (3-1000)")
    print("2. Generar aleatoriamente (3-1000)")
    opcion_nodos = validar_entrada("Opción: ", int, 1, 2)

    if opcion_nodos == 1:
        num_nodos = validar_entrada("Número de nodos (3-1000): ", int, 3, 1000)
    else:
        num_nodos = random.randint(3, 1000)
        print(f"\nSe ha generado aleatoriamente un problema con {num_nodos} nodos.")

    # Crear instancia del TSP genérico
    tsp = TSPGenerico(num_nodos)

    # Mostrar información del problema
    tsp.mostrar_informacion_problema()

    # Pausar hasta que el usuario presione Enter
    input("\nPresione Enter para continuar...")

    # Seleccionar algoritmo
    print("\nSeleccione el algoritmo de resolución:")
    print("1. Fuerza Bruta (solo para n ≤ 10)")
    print("2. Vecino más cercano")
    print("3. Búsqueda local 2-opt")

    algoritmo = validar_entrada("Opción: ", int, 1, 3)

    print("\nResolviendo el problema...")
    start_time = time.time()

    if algoritmo == 1:
        ruta, distancia = tsp.resolver_fuerza_bruta()
    elif algoritmo == 2:
        ruta, distancia = tsp.resolver_vecino_mas_cercano()
    else:
        ruta, distancia = tsp.resolver_2opt()

    end_time = time.time()

    # Mostrar resultados
    tsp.mostrar_resultados()
    print(f"\nTiempo de ejecución: {end_time - start_time:.4f} segundos")

    input("\nPresione Enter para continuar...")


def tsp_capacidad():
    """Función para el TSP con capacidad"""
    limpiar_pantalla()
    print("\n--- TSP CON CAPACIDAD DE CAMIÓN ---")
    print("\nEn esta variante, un camión con capacidad limitada debe entregar")
    print("mercancías en varios nodos. Si se queda sin stock, debe regresar")
    print("al almacén (nodo A) para recargar antes de continuar.\n")

    # Opciones para el número de nodos
    print("Seleccione cómo determinar el número de nodos:")
    print("1. Ingresar manualmente (3-1000)")
    print("2. Generar aleatoriamente (3-1000)")
    opcion_nodos = validar_entrada("Opción: ", int, 1, 2)

    if opcion_nodos == 1:
        num_nodos = validar_entrada("Número de nodos (3-1000): ", int, 3, 1000)
    else:
        num_nodos = random.randint(3, 1000)
        print(f"\nSe ha generado aleatoriamente un problema con {num_nodos} nodos.")

    # Solicitar capacidad del camión
    capacidad = validar_entrada("Capacidad del camión (10-500, por defecto 100): ", int, 10, 500) or 100

    # Preguntar cómo se generarán las demandas
    print("\n¿Cómo desea asignar las demandas de los nodos?")
    print("1. Ingresar manualmente")
    print("2. Generar aleatoriamente")
    opcion_demandas = validar_entrada("Opción: ", int, 1, 2)

    demandas = [0]  # El almacén (nodo 0) siempre tiene demanda 0

    if opcion_demandas == 1:
        # Ingresar demandas manualmente
        print("\nIngrese la demanda para cada nodo (unidades):")
        # Generar etiquetas temporales para mostrar al usuario
        etiquetas_temporales = generar_etiquetas(num_nodos)
        for i in range(1, num_nodos):
            etiqueta = etiquetas_temporales[i]
            demanda = validar_entrada(f"Nodo {etiqueta}: ", int, 1, 100)
            demandas.append(demanda)
    else:
        # Generar demandas aleatorias
        for i in range(1, num_nodos):
            demanda = random.randint(5, 30)
            demandas.append(demanda)

    # Crear instancia del TSP con capacidad
    tsp = TSPCapacidad(num_nodos, capacidad, demandas)

    # Mostrar información del viaje
    tsp.mostrar_informacion_viaje()

    # Pausar hasta que el usuario presione Enter
    input("\nPresione Enter para empezar el viaje...")

    # Seleccionar algoritmo
    print("\nSeleccione el algoritmo de resolución:")
    print("1. Algoritmo Greedy")
    print("2. Búsqueda Local")

    algoritmo = validar_entrada("Opción: ", int, 1, 2)

    print("\nResolviendo el problema...")
    start_time = time.time()

    if algoritmo == 1:
        ruta, distancia, entregas = tsp.resolver_greedy()
    else:
        ruta, distancia, entregas = tsp.resolver_busqueda_local()

    end_time = time.time()

    # Mostrar resultados
    tsp.mostrar_resultados()
    print(f"\nTiempo de ejecución: {end_time - start_time:.4f} segundos")

    input("\nPresione Enter para continuar...")


def main():
    """Función principal del programa"""
    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = validar_entrada("Seleccione una opción: ", int, 1, 3)

        if opcion == 1:
            tsp_generico()
        elif opcion == 2:
            tsp_capacidad()
        else:
            print("\n¡Gracias por usar el programa!")
            break


if __name__ == "__main__":
    main()