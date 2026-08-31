"""
Busqueda de Escalada (Hill Climbing)
=====================================
Algoritmo de busqueda local que en cada paso se mueve al vecino con el
mejor valor de la funcion objetivo. No mantiene un arbol de busqueda,
solo recuerda el estado actual.

Tipo:       Busqueda local
Completo:   No (puede quedarse en optimos locales, mesetas o crestas)
Optimo:     No
Memoria:    O(b)  solo el estado actual y sus vecinos
"""

import random


def hill_climbing(problema_local, max_iteraciones=1000):
    """
    Busqueda de escalada (Hill Climbing).

    Parametros
    ----------
    problema_local : objeto que implementa:
        - estado_inicial()          -> estado de inicio
        - vecinos(estado)           -> lista de estados vecinos
        - valor(estado)             -> valor numerico del estado (mayor = mejor)
    max_iteraciones : int
        Numero maximo de iteraciones para evitar ciclos infinitos.

    Retorna
    -------
    tuple(estado, float)
        (mejor estado encontrado, su valor).
    """
    estado_actual = problema_local.estado_inicial()
    valor_actual = problema_local.valor(estado_actual)

    for _ in range(max_iteraciones):
        vecinos = problema_local.vecinos(estado_actual)
        if not vecinos:
            break

        mejor_vecino = max(vecinos, key=problema_local.valor)
        mejor_valor = problema_local.valor(mejor_vecino)

        if mejor_valor <= valor_actual:
            break

        estado_actual = mejor_vecino
        valor_actual = mejor_valor

    return estado_actual, valor_actual


def hill_climbing_estocastico(problema_local, max_iteraciones=1000):
    """
    Variante estocastica: elige aleatoriamente entre los vecinos mejores,
    lo que ayuda a escapar de algunos optimos locales.

    Parametros
    ----------
    problema_local : objeto que implementa:
        - estado_inicial()     -> estado de inicio
        - vecinos(estado)      -> lista de estados vecinos
        - valor(estado)        -> valor numerico del estado (mayor = mejor)
    max_iteraciones : int
        Numero maximo de iteraciones.

    Retorna
    -------
    tuple(estado, float)
        (mejor estado encontrado, su valor).
    """
    estado_actual = problema_local.estado_inicial()
    valor_actual = problema_local.valor(estado_actual)

    for _ in range(max_iteraciones):
        vecinos = problema_local.vecinos(estado_actual)
        mejores = [v for v in vecinos if problema_local.valor(v) > valor_actual]

        if not mejores:
            break

        estado_actual = random.choice(mejores)
        valor_actual = problema_local.valor(estado_actual)

    return estado_actual, valor_actual
