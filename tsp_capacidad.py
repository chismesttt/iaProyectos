import random
import math
from collections import deque
from utils import generar_etiquetas, indice_a_letra, mostrar_matriz


class TSPCapacidad:
    def __init__(self, num_nodos=12, capacidad_camion=100, demandas=None):
        self.num_nodos = num_nodos
        self.etiquetas = generar_etiquetas(num_nodos)
        self.capacidad_camion = capacidad_camion
        self.distancias = self.generar_distancias()
        if demandas is None:
            self.demandas = self.generar_demandas()
        else:
            self.demandas = demandas
        self.mejor_ruta_indices = None
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')
        self.entregas_realizadas = []
        self.regresos_almacen = []  # Para registrar los viajes de regreso al almacén

    def generar_distancias(self):
        """Genera una matriz de distancias aleatorias entre nodos (en km)"""
        distancias = [[0] * self.num_nodos for _ in range(self.num_nodos)]
        for i in range(self.num_nodos):
            for j in range(i + 1, self.num_nodos):
                dist = random.randint(10, 500)
                distancias[i][j] = dist
                distancias[j][i] = dist
        return distancias

    def generar_demandas(self):
        """Genera demandas aleatorias para cada nodo (excepto el almacén)"""
        demandas = [0]  # El almacén (nodo 0) no tiene demanda
        for i in range(1, self.num_nodos):
            # Demanda entre 5 y 30
            demanda = random.randint(5, 30)
            demandas.append(demanda)
        return demandas

    def distancia_total(self, ruta_indices):
        """Calcula la distancia total de una ruta (dada en índices)"""
        total = 0
        for i in range(len(ruta_indices) - 1):
            total += self.distancias[ruta_indices[i]][ruta_indices[i + 1]]
        return total

    def obtener_ruta_optima_a_almacen(self, nodo_actual):
        """Obtiene la ruta óptima desde un nodo hasta el almacén (A)"""
        # En este caso, como no hay restricciones adicionales, la ruta óptima es directa
        # Pero en una implementación más compleja, podríamos usar Dijkstra o Floyd-Warshall
        # Para este ejemplo, asumimos que la ruta directa es la óptima
        return [nodo_actual, 0]

    def resolver_greedy(self):
        """Resuelve el TSP con capacidad usando un algoritmo greedy"""
        ruta_indices = [0]  # Empezamos en el almacén
        carga_actual = self.capacidad_camion
        distancia_total = 0
        entregas = []
        demandas_pendientes = self.demandas.copy()
        nodos_visitados = [False] * self.num_nodos
        nodos_visitados[0] = True

        while not all(d == 0 for d in demandas_pendientes[1:]):
            actual = ruta_indices[-1]
            mejor_siguiente = None
            mejor_distancia = float('inf')

            # Buscar el nodo más cercano con demanda pendiente
            for nodo in range(1, self.num_nodos):
                if demandas_pendientes[nodo] > 0 and not nodos_visitados[nodo]:
                    if self.distancias[actual][nodo] < mejor_distancia:
                        mejor_distancia = self.distancias[actual][nodo]
                        mejor_siguiente = nodo

            if mejor_siguiente is None:
                # No hay nodos accesibles, regresar al almacén por la ruta óptima
                if actual != 0:
                    ruta_optima = self.obtener_ruta_optima_a_almacen(actual)
                    # Eliminar el primer nodo (actual) porque ya está en la ruta
                    ruta_regreso = ruta_optima[1:]

                    # Añadir la ruta de regreso a la ruta principal
                    ruta_indices.extend(ruta_regreso)

                    # Calcular la distancia del regreso
                    distancia_regreso = 0
                    for i in range(len(ruta_optima) - 1):
                        distancia_regreso += self.distancias[ruta_optima[i]][ruta_optima[i + 1]]
                    distancia_total += distancia_regreso

                    # Registrar el regreso al almacén
                    self.regresos_almacen.append({
                        'nodo_inicio': indice_a_letra(actual, self.etiquetas),
                        'ruta': [indice_a_letra(i, self.etiquetas) for i in ruta_optima],
                        'distancia': distancia_regreso
                    })

                    # Recargar el camión
                    carga_actual = self.capacidad_camion
                continue

            # Verificar si podemos entregar en el nodo seleccionado
            if carga_actual >= demandas_pendientes[mejor_siguiente]:
                # Entrega completa
                cantidad_entregada = demandas_pendientes[mejor_siguiente]
                demandas_pendientes[mejor_siguiente] = 0
                nodos_visitados[mejor_siguiente] = True
            else:
                # Entrega parcial
                cantidad_entregada = carga_actual
                demandas_pendientes[mejor_siguiente] -= carga_actual

            # Actualizar carga y ruta
            carga_actual -= cantidad_entregada
            ruta_indices.append(mejor_siguiente)
            distancia_total += mejor_distancia

            # Registrar entrega
            entregas.append({
                'nodo': indice_a_letra(mejor_siguiente, self.etiquetas),
                'cantidad': cantidad_entregada,
                'carga_restante': carga_actual
            })

            # Si la carga es 0, regresar al almacén por la ruta óptima
            if carga_actual == 0:
                ruta_optima = self.obtener_ruta_optima_a_almacen(mejor_siguiente)
                # Eliminar el primer nodo (mejor_siguiente) porque ya está en la ruta
                ruta_regreso = ruta_optima[1:]

                # Añadir la ruta de regreso a la ruta principal
                ruta_indices.extend(ruta_regreso)

                # Calcular la distancia del regreso
                distancia_regreso = 0
                for i in range(len(ruta_optima) - 1):
                    distancia_regreso += self.distancias[ruta_optima[i]][ruta_optima[i + 1]]
                distancia_total += distancia_regreso

                # Registrar el regreso al almacén
                self.regresos_almacen.append({
                    'nodo_inicio': indice_a_letra(mejor_siguiente, self.etiquetas),
                    'ruta': [indice_a_letra(i, self.etiquetas) for i in ruta_optima],
                    'distancia': distancia_regreso
                })

                # Recargar el camión
                carga_actual = self.capacidad_camion

        # Regresar al almacén si no estamos allí
        if ruta_indices[-1] != 0:
            ruta_optima = self.obtener_ruta_optima_a_almacen(ruta_indices[-1])
            # Eliminar el primer nodo porque ya está en la ruta
            ruta_regreso = ruta_optima[1:]

            # Añadir la ruta de regreso a la ruta principal
            ruta_indices.extend(ruta_regreso)

            # Calcular la distancia del regreso
            distancia_regreso = 0
            for i in range(len(ruta_optima) - 1):
                distancia_regreso += self.distancias[ruta_optima[i]][ruta_optima[i + 1]]
            distancia_total += distancia_regreso

            # Registrar el regreso al almacén
            self.regresos_almacen.append({
                'nodo_inicio': indice_a_letra(ruta_indices[-1], self.etiquetas),
                'ruta': [indice_a_letra(i, self.etiquetas) for i in ruta_optima],
                'distancia': distancia_regreso
            })

        self.mejor_ruta_indices = ruta_indices
        self.mejor_distancia = distancia_total
        self.mejor_ruta = [indice_a_letra(i, self.etiquetas) for i in ruta_indices]
        self.entregas_realizadas = entregas
        return self.mejor_ruta, distancia_total, entregas

    def resolver_busqueda_local(self, max_iteraciones=100):
        """Resuelve el TSP con capacidad usando búsqueda local"""
        # Primero obtener una solución inicial con el método greedy
        self.resolver_greedy()
        mejor_ruta_indices = self.mejor_ruta_indices.copy()
        mejor_distancia = self.mejor_distancia
        mejor_entregas = self.entregas_realizadas.copy()
        mejor_regresos = self.regresos_almacen.copy()

        for _ in range(max_iteraciones):
            # Generar una solución vecina
            nueva_ruta_indices = self.generar_vecino(mejor_ruta_indices)

            # Evaluar la nueva solución
            nueva_distancia, nuevas_entregas, nuevos_regresos = self.evaluar_ruta(nueva_ruta_indices)

            # Si es mejor, actualizar
            if nueva_distancia < mejor_distancia:
                mejor_ruta_indices = nueva_ruta_indices
                mejor_distancia = nueva_distancia
                mejor_entregas = nuevas_entregas
                mejor_regresos = nuevos_regresos

        self.mejor_ruta_indices = mejor_ruta_indices
        self.mejor_distancia = mejor_distancia
        self.mejor_ruta = [indice_a_letra(i, self.etiquetas) for i in mejor_ruta_indices]
        self.entregas_realizadas = mejor_entregas
        self.regresos_almacen = mejor_regresos
        return self.mejor_ruta, mejor_distancia, mejor_entregas

    def generar_vecino(self, ruta_indices):
        """Genera una solución vecina intercambiando dos nodos"""
        nueva_ruta_indices = ruta_indices.copy()

        # Encontrar dos nodos de entrega (no el almacén) para intercambiar
        indices = [i for i, nodo in enumerate(ruta_indices) if nodo != 0]
        if len(indices) < 2:
            return nueva_ruta_indices

        i, j = random.sample(indices, 2)
        nueva_ruta_indices[i], nueva_ruta_indices[j] = nueva_ruta_indices[j], nueva_ruta_indices[i]

        return nueva_ruta_indices

    def evaluar_ruta(self, ruta_indices):
        """Evalúa una ruta calculando la distancia y las entregas realizadas"""
        distancia_total = 0
        carga_actual = self.capacidad_camion
        entregas = []
        regresos = []
        demandas_pendientes = self.demandas.copy()

        # Simular entregas
        for i in range(len(ruta_indices) - 1):
            nodo_actual = ruta_indices[i]
            siguiente_nodo = ruta_indices[i + 1]

            # Si estamos en un nodo de entrega
            if nodo_actual != 0 and demandas_pendientes[nodo_actual] > 0:
                if carga_actual >= demandas_pendientes[nodo_actual]:
                    cantidad_entregada = demandas_pendientes[nodo_actual]
                    demandas_pendientes[nodo_actual] = 0
                else:
                    cantidad_entregada = carga_actual
                    demandas_pendientes[nodo_actual] -= cantidad_entregada

                carga_actual -= cantidad_entregada

                entregas.append({
                    'nodo': indice_a_letra(nodo_actual, self.etiquetas),
                    'cantidad': cantidad_entregada,
                    'carga_restante': carga_actual
                })

            # Si llegamos al almacén, recargar
            if siguiente_nodo == 0:
                carga_actual = self.capacidad_camion
                # Registrar el regreso al almacén
                if nodo_actual != 0:
                    ruta_optima = self.obtener_ruta_optima_a_almacen(nodo_actual)
                    distancia_regreso = 0
                    for j in range(len(ruta_optima) - 1):
                        distancia_regreso += self.distancias[ruta_optima[j]][ruta_optima[j + 1]]

                    regresos.append({
                        'nodo_inicio': indice_a_letra(nodo_actual, self.etiquetas),
                        'ruta': [indice_a_letra(idx, self.etiquetas) for idx in ruta_optima],
                        'distancia': distancia_regreso
                    })

            distancia_total += self.distancias[nodo_actual][siguiente_nodo]

        return distancia_total, entregas, regresos

    def mostrar_informacion_viaje(self):
        """Muestra la información del viaje antes de empezar"""
        print("\n=== INFORMACIÓN DEL VIAJE ===")
        print(f"Número de nodos: {self.num_nodos}")
        print(f"Capacidad del camión: {self.capacidad_camion} unidades")
        print("\nMatriz de distancias (km):")
        mostrar_matriz(self.distancias, self.etiquetas)

        print("\nDemandas por nodo:")
        for i, demanda in enumerate(self.demandas):
            if i == 0:
                print(f"Almacén (Nodo {self.etiquetas[i]}): {demanda}")
            else:
                print(f"Nodo {self.etiquetas[i]}: {demanda}")

    def mostrar_resultados(self):
        """Muestra los resultados de la solución"""
        print("\n=== RESULTADOS DEL VIAJE ===")
        print("\nMejor ruta encontrada:")
        print(" -> ".join(self.mejor_ruta))
        print(f"Distancia total: {self.mejor_distancia:.2f} km")

        print("\nEntregas realizadas:")
        for entrega in self.entregas_realizadas:
            print(
                f"  - Nodo {entrega['nodo']}: {entrega['cantidad']} unidades (Carga restante: {entrega['carga_restante']})")

        print("\nRegresos al almacén (rutas óptimas):")
        for regreso in self.regresos_almacen:
            print(f"  - Desde {regreso['nodo_inicio']}: {' -> '.join(regreso['ruta'])} ({regreso['distancia']:.2f} km)")

        # Verificar si todas las demandas fueron satisfechas
        demandas_pendientes = self.demandas.copy()
        for entrega in self.entregas_realizadas:
            nodo_idx = self.etiquetas.index(entrega['nodo'])
            demandas_pendientes[nodo_idx] -= entrega['cantidad']

        pendientes = [f"{self.etiquetas[i]}({d})" for i, d in enumerate(demandas_pendientes) if d > 0]
        if pendientes:
            print(f"\n⚠️ Quedan demandas pendientes: {', '.join(pendientes)}")
        else:
            print("\n✅ Todas las demandas han sido satisfechas")

        # Verificar que la ruta comienza y termina en el almacén
        if self.mejor_ruta[0] == 'A' and self.mejor_ruta[-1] == 'A':
            print("\n✅ La ruta comienza y termina en el almacén (A)")
        else:
            print("\n⚠️ La ruta no cumple con el requisito de regresar al almacén")