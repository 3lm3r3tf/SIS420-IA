# SIS420-IA — Practica de Inteligencia Artificial

Implementacion de algoritmos clasicos de Inteligencia Artificial para la materia SIS420.

## Contenido

### Algoritmos de Busqueda

| Algoritmo | Tipo | Completo | Optimo |
|---|---|---|---|
| BFS | No informado | Sí | Sí (costo uniforme) |
| DFS | No informado | No | No |
| A* | Informado | Sí | Sí (heuristica admisible) |
| Greedy Best-First | Informado | No | No |
| Hill Climbing | Busqueda local | No | No |

### Problema de Ejemplo

**8-Puzzle**: tablero de 3×3 con 8 fichas numeradas y una casilla vacía.  
Se aplican todos los algoritmos para comparar su comportamiento.

## Estructura del Proyecto

```
practica_ia/
├── busqueda/
│   ├── bfs.py           # Busqueda en Anchura
│   ├── dfs.py           # Busqueda en Profundidad
│   ├── a_star.py        # Busqueda A*
│   ├── greedy.py        # Busqueda Avara
│   └── hill_climbing.py # Escalada de Colinas
└── ejemplos/
    └── ocho_puzzle.py   # Problema 8-Puzzle
main.py                  # Demostracion
tests/
└── test_algoritmos.py   # Pruebas unitarias
```

## Uso

```bash
# Ejecutar la demostracion
python main.py

# Ejecutar pruebas
python -m pytest tests/ -v
```

## Ejemplo de Salida

```
PRACTICA DE INTELIGENCIA ARTIFICIAL - SIS420
Problema 8-Puzzle

Estado inicial:       Estado meta:
+-------+             +-------+
| 1 2 3 |             | 1 2 3 |
| 4 _ 6 |    --->     | 4 5 6 |
| 7 5 8 |             | 7 8 _ |
+-------+             +-------+

BFS - Busqueda en Anchura
  Pasos: 2  |  Acciones: ['abajo', 'derecha']

A* con Heuristica Manhattan
  Pasos: 2  |  Acciones: ['abajo', 'derecha']
```