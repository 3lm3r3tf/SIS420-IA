"""
Busqueda en Profundidad (DFS - Depth-First Search)
===================================================
Algoritmo de busqueda no informada que explora tan profundo como sea posible
a lo largo de cada rama antes de retroceder.

Complejidad temporal: O(b^m)  donde b = factor de ramificacion, m = profundidad maxima
Complejidad espacial: O(b*m)
Completo: No (puede caer en ciclos; Si se usa limite de profundidad)
Optimo:   No
"""


def dfs(problema, limite=None):
    """
    Busqueda en profundidad (DFS) con limite opcional.

    Parametros
    ----------
    problema : objeto que implementa:
        - estado_inicial()     -> estado de inicio
        - es_meta(estado)      -> True si el estado es la solucion
        - acciones(estado)     -> lista de acciones aplicables
        - resultado(estado, accion) -> nuevo estado
    limite : int, opcional
        Profundidad maxima de busqueda. Si es None, no hay limite.

    Retorna
    -------
    list | None
        Lista de acciones que llevan al estado meta, o None si no existe solucion.
    """
    estado_inicio = problema.estado_inicial()
    return _dfs_recursivo(problema, estado_inicio, [], set(), limite)


def _dfs_recursivo(problema, estado, camino, visitados, limite):
    if problema.es_meta(estado):
        return camino

    if limite is not None and len(camino) >= limite:
        return None

    visitados.add(estado)

    for accion in problema.acciones(estado):
        nuevo_estado = problema.resultado(estado, accion)

        if nuevo_estado not in visitados:
            resultado = _dfs_recursivo(
                problema, nuevo_estado, camino + [accion], visitados, limite
            )
            if resultado is not None:
                visitados.discard(estado)
                return resultado

    visitados.discard(estado)
    return None
