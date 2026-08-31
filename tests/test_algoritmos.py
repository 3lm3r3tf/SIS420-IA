"""
Pruebas unitarias para los algoritmos de busqueda - SIS420 Practica IA
"""

import pytest

from practica_ia.busqueda import a_star, bfs, dfs, greedy_best_first
from practica_ia.busqueda.hill_climbing import hill_climbing
from practica_ia.ejemplos import OchoPuzzle


# ---------------------------------------------------------------------------
# Problema simple: grafo de nodos numerados
# ---------------------------------------------------------------------------

class ProblemaSimple:
    """
    Grafo de 6 nodos:
        0 -> 1, 2
        1 -> 3
        2 -> 3, 4
        3 -> 5  (meta)
        4 -> 5  (meta)
    """

    GRAFO = {
        0: [1, 2],
        1: [3],
        2: [3, 4],
        3: [5],
        4: [5],
        5: [],
    }

    def __init__(self, inicio=0, meta=5):
        self._inicio = inicio
        self._meta = meta

    def estado_inicial(self):
        return self._inicio

    def es_meta(self, estado):
        return estado == self._meta

    def acciones(self, estado):
        return list(self.GRAFO.get(estado, []))

    def resultado(self, estado, accion):
        return accion

    def costo_accion(self, estado, accion):
        return 1


# ---------------------------------------------------------------------------
# Heuristica trivial para el problema simple
# ---------------------------------------------------------------------------

def heuristica_trivial(estado):
    distancias = {0: 2, 1: 2, 2: 1, 3: 1, 4: 1, 5: 0}
    return distancias.get(estado, 0)


# ---------------------------------------------------------------------------
# Pruebas BFS
# ---------------------------------------------------------------------------

class TestBFS:
    def test_solucion_encontrada(self):
        problema = ProblemaSimple()
        solucion = bfs(problema)
        assert solucion is not None

    def test_estado_meta_inicial(self):
        problema = ProblemaSimple(inicio=5, meta=5)
        solucion = bfs(problema)
        assert solucion == []

    def test_sin_solucion(self):
        problema = ProblemaSimple(inicio=5, meta=0)
        solucion = bfs(problema)
        assert solucion is None

    def test_solucion_optima(self):
        problema = ProblemaSimple()
        solucion = bfs(problema)
        # El camino mas corto tiene 3 pasos: e.g. 0->1->3->5
        assert len(solucion) == 3


# ---------------------------------------------------------------------------
# Pruebas DFS
# ---------------------------------------------------------------------------

class TestDFS:
    def test_solucion_encontrada(self):
        problema = ProblemaSimple()
        solucion = dfs(problema)
        assert solucion is not None

    def test_con_limite_suficiente(self):
        problema = ProblemaSimple()
        solucion = dfs(problema, limite=10)
        assert solucion is not None

    def test_con_limite_insuficiente(self):
        problema = ProblemaSimple()
        solucion = dfs(problema, limite=1)
        assert solucion is None

    def test_estado_meta_inicial(self):
        problema = ProblemaSimple(inicio=5, meta=5)
        solucion = dfs(problema)
        assert solucion == []


# ---------------------------------------------------------------------------
# Pruebas A*
# ---------------------------------------------------------------------------

class TestAStar:
    def test_solucion_encontrada(self):
        problema = ProblemaSimple()
        solucion, costo = a_star(problema, heuristica_trivial)
        assert solucion is not None
        assert costo == 3

    def test_estado_meta_inicial(self):
        problema = ProblemaSimple(inicio=5, meta=5)
        solucion, costo = a_star(problema, lambda s: 0)
        assert solucion == []
        assert costo == 0

    def test_sin_solucion(self):
        problema = ProblemaSimple(inicio=5, meta=0)
        solucion, costo = a_star(problema, heuristica_trivial)
        assert solucion is None
        assert costo is None


# ---------------------------------------------------------------------------
# Pruebas Greedy
# ---------------------------------------------------------------------------

class TestGreedy:
    def test_solucion_encontrada(self):
        problema = ProblemaSimple()
        solucion = greedy_best_first(problema, heuristica_trivial)
        assert solucion is not None

    def test_estado_meta_inicial(self):
        problema = ProblemaSimple(inicio=5, meta=5)
        solucion = greedy_best_first(problema, lambda s: 0)
        assert solucion == []

    def test_sin_solucion(self):
        problema = ProblemaSimple(inicio=5, meta=0)
        solucion = greedy_best_first(problema, heuristica_trivial)
        assert solucion is None


# ---------------------------------------------------------------------------
# Pruebas Hill Climbing
# ---------------------------------------------------------------------------

class ProblemaLocal:
    """Funcion f(x) = -(x-5)^2 + 25, maximo en x=5."""

    def estado_inicial(self):
        return 0

    def vecinos(self, estado):
        return [estado - 1, estado + 1] if 0 < estado < 10 else (
            [estado + 1] if estado == 0 else [estado - 1]
        )

    def valor(self, estado):
        return -(estado - 5) ** 2 + 25


class TestHillClimbing:
    def test_encuentra_maximo(self):
        problema = ProblemaLocal()
        estado, valor = hill_climbing(problema)
        assert estado == 5
        assert valor == 25


# ---------------------------------------------------------------------------
# Pruebas 8-Puzzle
# ---------------------------------------------------------------------------

class TestOchoPuzzle:
    ESTADO_FACIL = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    META = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def test_bfs_resuelve_puzzle(self):
        problema = OchoPuzzle(self.ESTADO_FACIL)
        solucion = bfs(problema)
        assert solucion is not None
        assert len(solucion) == 1

    def test_a_star_manhattan_resuelve_puzzle(self):
        problema = OchoPuzzle(self.ESTADO_FACIL)
        solucion, costo = a_star(problema, problema.heuristica_distancia_manhattan)
        assert solucion is not None
        assert costo == 1

    def test_heuristica_manhattan_correcta(self):
        problema = OchoPuzzle(self.META)
        assert problema.heuristica_distancia_manhattan(self.META) == 0

    def test_heuristica_piezas_mal_colocadas(self):
        problema = OchoPuzzle(self.META)
        assert problema.heuristica_piezas_mal_colocadas(self.META) == 0

    def test_acciones_desde_esquina(self):
        problema = OchoPuzzle((0, 1, 2, 3, 4, 5, 6, 7, 8))
        acciones = problema.acciones((0, 1, 2, 3, 4, 5, 6, 7, 8))
        assert "derecha" in acciones
        assert "abajo" in acciones
        assert "izquierda" not in acciones
        assert "arriba" not in acciones

    def test_resultado_accion(self):
        problema = OchoPuzzle(self.ESTADO_FACIL)
        nuevo = problema.resultado(self.ESTADO_FACIL, "derecha")
        assert nuevo == self.META
