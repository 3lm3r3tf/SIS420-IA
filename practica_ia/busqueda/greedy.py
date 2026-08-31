"""
Busqueda Avara / Greedy Best-First Search
==========================================
Algoritmo de busqueda informada que expande el nodo que parece mas cercano
a la meta segun la funcion heuristica h(n), ignorando el costo acumulado g(n).

f(n) = h(n)

Complejidad temporal: O(b^m)  en el peor caso
Complejidad espacial: O(b^m)
Completo: No (puede caer en ciclos sin deteccion)
Optimo:   No
"""

import heapq


def greedy_best_first(problema, heuristica):
    """
    Busqueda avara (Greedy Best-First Search).

    Parametros
    ----------
    problema : objeto que implementa:
        - estado_inicial()          -> estado de inicio
        - es_meta(estado)           -> True si el estado es la solucion
        - acciones(estado)          -> lista de acciones aplicables
        - resultado(estado, accion) -> nuevo estado
    heuristica : callable
        Funcion h(estado) que estima el costo al estado meta.

    Retorna
    -------
    list | None
        Lista de acciones que llevan al estado meta, o None si no existe solucion.
    """
    estado_inicio = problema.estado_inicial()

    if problema.es_meta(estado_inicio):
        return []

    contador = 0
    frontera = [(heuristica(estado_inicio), contador, estado_inicio, [])]
    heapq.heapify(frontera)

    explorados = set()

    while frontera:
        _, _, estado, camino = heapq.heappop(frontera)

        if problema.es_meta(estado):
            return camino

        if estado in explorados:
            continue
        explorados.add(estado)

        for accion in problema.acciones(estado):
            nuevo_estado = problema.resultado(estado, accion)

            if nuevo_estado not in explorados:
                nuevo_camino = camino + [accion]
                h = heuristica(nuevo_estado)
                contador += 1
                heapq.heappush(frontera, (h, contador, nuevo_estado, nuevo_camino))

    return None
