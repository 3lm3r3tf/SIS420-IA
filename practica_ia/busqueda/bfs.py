"""
Busqueda en Anchura (BFS - Breadth-First Search)
=================================================
Algoritmo de busqueda no informada que explora todos los nodos vecinos
al nivel actual antes de pasar al siguiente nivel.

Complejidad temporal: O(b^d)  donde b = factor de ramificacion, d = profundidad de la solucion
Complejidad espacial: O(b^d)
Completo: Si (si el espacio de estados es finito)
Optimo:   Si (cuando el costo por paso es uniforme)
"""

from collections import deque


def bfs(problema):
    """
    Busqueda en anchura (BFS).

    Parametros
    ----------
    problema : objeto que implementa:
        - estado_inicial()     -> estado de inicio
        - es_meta(estado)      -> True si el estado es la solucion
        - acciones(estado)     -> lista de acciones aplicables
        - resultado(estado, accion) -> nuevo estado

    Retorna
    -------
    list | None
        Lista de acciones que llevan al estado meta, o None si no existe solucion.
    """
    estado_inicio = problema.estado_inicial()

    if problema.es_meta(estado_inicio):
        return []

    frontera = deque()
    frontera.append((estado_inicio, []))
    explorados = set()
    explorados.add(estado_inicio)

    while frontera:
        estado, camino = frontera.popleft()

        for accion in problema.acciones(estado):
            nuevo_estado = problema.resultado(estado, accion)

            if nuevo_estado not in explorados:
                nuevo_camino = camino + [accion]

                if problema.es_meta(nuevo_estado):
                    return nuevo_camino

                explorados.add(nuevo_estado)
                frontera.append((nuevo_estado, nuevo_camino))

    return None
