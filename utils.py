def validar_entrada(mensaje, tipo=int, min_val=None, max_val=None):
    """Valida la entrada del usuario"""
    while True:
        try:
            valor = tipo(input(mensaje))
            if min_val is not None and valor < min_val:
                print(f"El valor debe ser al menos {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"El valor debe ser como máximo {max_val}")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")


def mostrar_matriz(matriz, etiquetas):
    """Muestra una matriz de forma legible con etiquetas"""
    # Calcular el ancho máximo de las etiquetas
    max_ancho = max(len(str(etiqueta)) for etiqueta in etiquetas)

    # Imprimir encabezado
    print(" " * (max_ancho + 2), end="")
    for etiqueta in etiquetas:
        print(f"{str(etiqueta):>{max_ancho + 2}}", end="")
    print()

    # Imprimir filas
    for i in range(len(matriz)):
        print(f"{str(etiquetas[i]):>{max_ancho + 2}}:", end="")
        for j in range(len(matriz[i])):
            print(f"{matriz[i][j]:>{max_ancho + 2}}", end="")
        print()


def generar_etiquetas(num_nodos):
    """Genera etiquetas para los nodos (A, B, ..., Z, AA, AB, ...)"""
    etiquetas = []
    for i in range(num_nodos):
        etiqueta = ""
        n = i
        while n >= 0:
            etiqueta = chr(65 + (n % 26)) + etiqueta
            n = n // 26 - 1
            if n < 0:
                break
        etiquetas.append(etiqueta)
    return etiquetas


def indice_a_letra(indice, etiquetas):
    """Convierte un índice a su etiqueta correspondiente"""
    return etiquetas[indice]


def letra_a_indice(letra, etiquetas):
    """Convierte una etiqueta a su índice correspondiente"""
    return etiquetas.index(letra)