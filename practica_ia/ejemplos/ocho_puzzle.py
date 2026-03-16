"""
Problema del 8-Puzzle
======================
El 8-puzzle es un tablero de 3x3 con 8 fichas numeradas del 1 al 8 y una
casilla vacia. El objetivo es llegar al estado meta moviendo las fichas.

Estado meta por defecto:
    1 2 3
    4 5 6
    7 8 _

Las fichas se representan como una tupla de 9 elementos (lectura izquierda-derecha,
arriba-abajo), donde 0 representa la casilla vacia.

Ejemplo:
    (1, 2, 3, 4, 5, 6, 7, 8, 0)  ->  estado meta
    (1, 2, 3, 4, 0, 6, 7, 5, 8)  ->  estado intermedio
"""

META_DEFAULT = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVIMIENTOS = {
    "arriba": -3,
    "abajo": 3,
    "izquierda": -1,
    "derecha": 1,
}

# Posiciones donde NO se puede mover el hueco a la izquierda (columna 0)
_NO_IZQUIERDA = {0, 3, 6}
# Posiciones donde NO se puede mover el hueco a la derecha (columna 2)
_NO_DERECHA = {2, 5, 8}


class OchoPuzzle:
    """
    Formulacion del problema 8-puzzle compatible con BFS, DFS, A* y Greedy.
    """

    def __init__(self, estado_inicio, meta=None):
        """
        Parametros
        ----------
        estado_inicio : tuple de 9 enteros
            Configuracion inicial del tablero (0 = casilla vacia).
        meta : tuple de 9 enteros, opcional
            Estado objetivo. Por defecto META_DEFAULT.
        """
        self._inicio = tuple(estado_inicio)
        self._meta = tuple(meta) if meta else META_DEFAULT

    # ------------------------------------------------------------------
    # Interfaz requerida por los algoritmos de busqueda
    # ------------------------------------------------------------------

    def estado_inicial(self):
        return self._inicio

    def estado_meta(self):
        return self._meta

    def es_meta(self, estado):
        return estado == self._meta

    def acciones(self, estado):
        hueco = estado.index(0)
        posibles = []

        if hueco not in _NO_IZQUIERDA and hueco + MOVIMIENTOS["izquierda"] >= 0:
            posibles.append("izquierda")
        if hueco not in _NO_DERECHA and hueco + MOVIMIENTOS["derecha"] <= 8:
            posibles.append("derecha")
        if hueco + MOVIMIENTOS["arriba"] >= 0:
            posibles.append("arriba")
        if hueco + MOVIMIENTOS["abajo"] <= 8:
            posibles.append("abajo")

        return posibles

    def resultado(self, estado, accion):
        lista = list(estado)
        hueco = lista.index(0)
        destino = hueco + MOVIMIENTOS[accion]
        lista[hueco], lista[destino] = lista[destino], lista[hueco]
        return tuple(lista)

    def costo_accion(self, estado, accion):
        return 1

    # ------------------------------------------------------------------
    # Heuristicas admisibles para A* y Greedy
    # ------------------------------------------------------------------

    def heuristica_piezas_mal_colocadas(self, estado):
        """Cuenta las piezas que no estan en su posicion meta (excluye el hueco)."""
        return sum(
            1
            for i, ficha in enumerate(estado)
            if ficha != 0 and ficha != self._meta[i]
        )

    def heuristica_distancia_manhattan(self, estado):
        """Suma de distancias Manhattan de cada pieza a su posicion meta."""
        distancia = 0
        meta_pos = {ficha: idx for idx, ficha in enumerate(self._meta)}
        for idx, ficha in enumerate(estado):
            if ficha == 0:
                continue
            fila_actual, col_actual = divmod(idx, 3)
            fila_meta, col_meta = divmod(meta_pos[ficha], 3)
            distancia += abs(fila_actual - fila_meta) + abs(col_actual - col_meta)
        return distancia

    # ------------------------------------------------------------------
    # Utilidades de visualizacion
    # ------------------------------------------------------------------

    @staticmethod
    def imprimir_estado(estado):
        """Imprime el tablero de forma legible."""
        simbolos = [str(f) if f != 0 else "_" for f in estado]
        print("+-------+")
        for fila in range(3):
            inicio = fila * 3
            print("| {} {} {} |".format(*simbolos[inicio : inicio + 3]))
        print("+-------+")

    @staticmethod
    def imprimir_solucion(solucion, estado_inicio, problema):
        """Imprime el tablero en cada paso de la solucion."""
        if solucion is None:
            print("No se encontro solucion.")
            return

        print(f"Solucion en {len(solucion)} pasos:\n")
        estado = estado_inicio
        OchoPuzzle.imprimir_estado(estado)

        for paso, accion in enumerate(solucion, start=1):
            estado = problema.resultado(estado, accion)
            print(f"Paso {paso}: mover '{accion}'")
            OchoPuzzle.imprimir_estado(estado)
