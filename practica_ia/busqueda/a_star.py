"""
Busqueda A* (A-Star Search)
============================
Algoritmo de busqueda informada que combina el costo del camino recorrido g(n)
con la estimacion heuristica h(n) para encontrar el camino optimo.

f(n) = g(n) + h(n)

Complejidad temporal: O(b^d)  en el peor caso
Complejidad espacial: O(b^d)  (mantiene todos los nodos en memoria)
Completo: Si (con heuristica admisible)
Optimo:   Si (con heuristica admisible y consistente)
"""

import heapq


def a_star(problema, heuristica):
    """
    Busqueda A*.

    Parametros
    ----------
    problema : objeto que implementa:
        - estado_inicial()          -> estado de inicio
        - es_meta(estado)           -> True si el estado es la solucion
        - acciones(estado)          -> lista de acciones aplicables
        - resultado(estado, accion) -> nuevo estado
        - costo_accion(estado, accion) -> costo numerico de aplicar la accion
    heuristica : callable
        Funcion h(estado) que estima el costo al estado meta.
        Debe ser admisible (nunca sobreestima el costo real).

    Retorna
    -------
    tuple(list, float) | tuple(None, None)
        (lista de acciones, costo total) o (None, None) si no hay solucion.
    """
    estado_inicio = problema.estado_inicial()
    h_inicio = heuristica(estado_inicio)

    # (f, g, contador, estado, camino)
    contador = 0
    frontera = [(h_inicio, 0, contador, estado_inicio, [])]
    heapq.heapify(frontera)

    explorados = {}

    while frontera:
        f, g, _, estado, camino = heapq.heappop(frontera)

        if problema.es_meta(estado):
            return camino, g

        if estado in explorados and explorados[estado] <= g:
            continue
        explorados[estado] = g

        for accion in problema.acciones(estado):
            nuevo_estado = problema.resultado(estado, accion)
            costo_paso = problema.costo_accion(estado, accion)
            nuevo_g = g + costo_paso

            if nuevo_estado in explorados and explorados[nuevo_estado] <= nuevo_g:
                continue

            nuevo_h = heuristica(nuevo_estado)
            nuevo_f = nuevo_g + nuevo_h
            contador += 1
            heapq.heappush(
                frontera,
                (nuevo_f, nuevo_g, contador, nuevo_estado, camino + [accion]),
            )

    return None, None
