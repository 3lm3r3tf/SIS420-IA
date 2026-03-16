"""
Practica de Inteligencia Artificial - SIS420
=============================================
Demostracion de algoritmos de busqueda aplicados al problema 8-Puzzle.

Algoritmos incluidos:
  - BFS  : Busqueda en Anchura
  - DFS  : Busqueda en Profundidad
  - A*   : Busqueda A-Star con heuristica Manhattan
  - Greedy: Busqueda Avara con heuristica Manhattan

Uso:
    python main.py
"""

import time

from practica_ia.busqueda import a_star, bfs, dfs, greedy_best_first
from practica_ia.ejemplos import OchoPuzzle

# Estado inicial de ejemplo (dificultad media, ~5 movimientos optimos)
ESTADO_INICIO = (1, 2, 3, 4, 0, 6, 7, 5, 8)


def ejecutar_algoritmo(nombre, fn_busqueda, problema, *args):
    print(f"\n{'='*50}")
    print(f"  {nombre}")
    print(f"{'='*50}")

    inicio = time.perf_counter()
    resultado = fn_busqueda(problema, *args)
    elapsed = time.perf_counter() - inicio

    if isinstance(resultado, tuple):
        solucion, costo = resultado
    else:
        solucion = resultado
        costo = len(solucion) if solucion else None

    if solucion is None:
        print("No se encontro solucion.")
    else:
        print(f"Pasos: {len(solucion)}  |  Costo: {costo}  |  Tiempo: {elapsed:.4f}s")
        print(f"Acciones: {solucion}")

    return solucion


def main():
    print("\nPRACTICA DE INTELIGENCIA ARTIFICIAL - SIS420")
    print("Problema 8-Puzzle")
    print("\nEstado inicial:")

    problema = OchoPuzzle(ESTADO_INICIO)
    OchoPuzzle.imprimir_estado(ESTADO_INICIO)
    print("Estado meta:")
    OchoPuzzle.imprimir_estado(problema.estado_meta())

    # BFS
    solucion_bfs = ejecutar_algoritmo("BFS - Busqueda en Anchura", bfs, problema)

    # DFS con limite de profundidad 20
    ejecutar_algoritmo("DFS - Busqueda en Profundidad (limite=20)", dfs, problema, 20)

    # A* con heuristica Manhattan
    ejecutar_algoritmo(
        "A* con Heuristica Manhattan",
        a_star,
        problema,
        problema.heuristica_distancia_manhattan,
    )

    # A* con heuristica piezas mal colocadas
    ejecutar_algoritmo(
        "A* con Heuristica Piezas Mal Colocadas",
        a_star,
        problema,
        problema.heuristica_piezas_mal_colocadas,
    )

    # Greedy con heuristica Manhattan
    ejecutar_algoritmo(
        "Greedy Best-First con Heuristica Manhattan",
        greedy_best_first,
        problema,
        problema.heuristica_distancia_manhattan,
    )

    # Mostrar solucion paso a paso (BFS)
    if solucion_bfs:
        print("\n\nSolucion paso a paso (BFS):")
        OchoPuzzle.imprimir_solucion(solucion_bfs, ESTADO_INICIO, problema)


if __name__ == "__main__":
    main()
