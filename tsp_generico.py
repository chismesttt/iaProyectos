import random
import math
from itertools import permutations
import time
from utils import generar_etiquetas, indice_a_letra, mostrar_matriz


class TSPGenerico:
    def __init__(self, num_nodos=12):
        self.num_nodos = num_nodos
        self.etiquetas = generar_etiquetas(num_nodos)
        self.distancias = self.generar_distancias()
        self.mejor_ruta_indices = None
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')

    def generar_distancias(self):
        """Genera una matriz de distancias aleatorias entre nodos (en km)"""
        distancias = [[0] * self.num_nodos for _ in range(self.num_nodos)]
        for i in range(self.num_nodos):
            for j in range(i + 1, self.num_nodos):
                # Distancia aleatoria entre 10 y 500 km
                dist = random.randint(10, 500)
                distancias[i][j] = dist
                distancias[j][i] = dist
        return distancias

    def distancia_total(self, ruta_indices):
        """Calcula la distancia total de una ruta (dada en índices)"""
        total = 0
        for i in range(len(ruta_indices)):
            total += self.distancias[ruta_indices[i]][ruta_indices[(i + 1) % len(ruta_indices)]]
        return total

    def resolver_fuerza_bruta(self):
        """Resuelve el TSP mediante fuerza bruta (solo para n <= 10)"""
        if self.num_nodos > 10:
            print("La fuerza bruta no es eficiente para más de 10 nodos.")
            return None, None

        nodos = list(range(self.num_nodos))
        mejor_ruta_indices = None
        mejor_distancia = float('inf')

        for perm in permutations(nodos[1:]):
            ruta_indices = [nodos[0]] + list(perm)
            distancia = self.distancia_total(ruta_indices)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_ruta_indices = ruta_indices

        # Asegurar que la ruta regrese al nodo inicial
        if mejor_ruta_indices[-1] != mejor_ruta_indices[0]:
            mejor_ruta_indices.append(mejor_ruta_indices[0])

        self.mejor_ruta_indices = mejor_ruta_indices
        self.mejor_distancia = mejor_distancia
        self.mejor_ruta = [indice_a_letra(i, self.etiquetas) for i in mejor_ruta_indices]
        return self.mejor_ruta, mejor_distancia

    def resolver_vecino_mas_cercano(self):
        """Resuelve el TSP usando el algoritmo del vecino más cercano"""
        visitados = [False] * self.num_nodos
        ruta_indices = [0]  # Empezamos en el nodo 0
        visitados[0] = True
        distancia_total = 0

        while len(ruta_indices) < self.num_nodos:
            actual = ruta_indices[-1]
            min_distancia = float('inf')
            siguiente_nodo = None

            for nodo in range(self.num_nodos):
                if not visitados[nodo] and self.distancias[actual][nodo] < min_distancia:
                    min_distancia = self.distancias[actual][nodo]
                    siguiente_nodo = nodo

            if siguiente_nodo is not None:
                ruta_indices.append(siguiente_nodo)
                visitados[siguiente_nodo] = True
                distancia_total += min_distancia

        # Regresar al nodo inicial
        if ruta_indices[-1] != ruta_indices[0]:
            ruta_indices.append(ruta_indices[0])
            distancia_total += self.distancias[ruta_indices[-2]][ruta_indices[-1]]

        self.mejor_ruta_indices = ruta_indices
        self.mejor_distancia = distancia_total
        self.mejor_ruta = [indice_a_letra(i, self.etiquetas) for i in ruta_indices]
        return self.mejor_ruta, distancia_total

    def resolver_2opt(self, max_iteraciones=1000):
        """Resuelve el TSP usando el algoritmo 2-opt"""
        # Generar una ruta inicial con vecino más cercano
        self.resolver_vecino_mas_cercano()
        ruta_indices = self.mejor_ruta_indices[:-1]  # Eliminar el último nodo (que es el inicial)
        mejor_distancia = self.mejor_distancia

        mejorado = True
        iteraciones = 0

        while mejorado and iteraciones < max_iteraciones:
            mejorado = False
            iteraciones += 1

            for i in range(1, len(ruta_indices) - 2):
                for j in range(i + 1, len(ruta_indices)):
                    if j - i == 1:
                        continue

                    # Crear nueva ruta intercambiando aristas
                    nueva_ruta_indices = ruta_indices[:]
                    nueva_ruta_indices[i:j] = ruta_indices[j - 1:i - 1:-1]  # Invertir el segmento

                    # Calcular nueva distancia
                    nueva_distancia = self.distancia_total(nueva_ruta_indices)

                    if nueva_distancia < mejor_distancia:
                        ruta_indices = nueva_ruta_indices
                        mejor_distancia = nueva_distancia
                        mejorado = True

            # Actualizar la mejor ruta
            ruta_indices_completa = ruta_indices + [ruta_indices[0]]
            self.mejor_ruta_indices = ruta_indices_completa
            self.mejor_distancia = mejor_distancia

        self.mejor_ruta = [indice_a_letra(i, self.etiquetas) for i in self.mejor_ruta_indices]
        return self.mejor_ruta, self.mejor_distancia

    def mostrar_informacion_problema(self):
        """Muestra la información del problema antes de resolver"""
        print("\n=== INFORMACIÓN DEL PROBLEMA TSP GENÉRICO ===")
        print(f"Número de nodos: {self.num_nodos}")
        print("\nMatriz de distancias (km):")
        mostrar_matriz(self.distancias, self.etiquetas)

    def mostrar_resultados(self):
        """Muestra los resultados de la solución"""
        print("\n=== RESULTADOS TSP GENÉRICO ===")
        print("\nMejor ruta encontrada:")
        print(" -> ".join(self.mejor_ruta))
        print(f"Distancia total: {self.mejor_distancia:.2f} km")

        # Verificar que la ruta comienza y termina en el mismo nodo
        if self.mejor_ruta[0] == self.mejor_ruta[-1]:
            print("\n✅ La ruta comienza y termina en el mismo nodo (A)")
        else:
            print("\n⚠️ La ruta no cumple con el requisito de regresar al punto de partida")