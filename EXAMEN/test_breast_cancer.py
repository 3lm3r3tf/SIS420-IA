"""
TEST BREAST CANCER WISCONSIN DATASET
Diagnóstico de cáncer de mama
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("BREAST CANCER WISCONSIN - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "breast_cancer_wisconsin"

# Cargar dataset
print("\n[1] Cargando wdbc.data...")

try:
    df = pd.read_csv(datasets_path / "wdbc.data", header=None)
    print(f"✓ Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# 2. INFORMACIÓN BÁSICA
print("\n" + "=" * 70)
print("1. INFORMACIÓN BÁSICA")
print("=" * 70)
print(f"Shape: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.4f} MB")

# 3. TIPOS
print("\n" + "=" * 70)
print("2. TIPOS DE DATOS")
print("=" * 70)
print(df.dtypes.value_counts())

# 4. PRIMERAS FILAS
print("\n" + "=" * 70)
print("3. PRIMERAS 5 FILAS")
print("=" * 70)
print(df.head().to_string())

# 5. ESTADÍSTICAS
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS DESCRIPTIVAS")
print("=" * 70)
print(df.describe().T.to_string())

# 6. COLUMNAS
print("\n" + "=" * 70)
print("5. DESCRIPCIÓN DE COLUMNAS")
print("=" * 70)
print("""
Columna 0: ID número
Columna 1: Diagnóstico (M=Maligno, B=Benigno) - TARGET
Columnas 2-11: Media de 10 características
Columnas 12-21: Error estándar de 10 características
Columnas 22-31: Peor (máximo) de 10 características

Características:
  - Radius (radio)
  - Texture (textura)
  - Perimeter (perímetro)
  - Area (área)
  - Smoothness (suavidad)
  - Compactness (compacidad)
  - Concavity (concavidad)
  - Concave points (puntos cóncavos)
  - Symmetry (simetría)
  - Fractal dimension (dimensión fractal)
""")

# 7. TARGET
print("\n" + "=" * 70)
print("6. ANÁLISIS DEL TARGET (Columna 1)")
print("=" * 70)
target = df.iloc[:, 1]
print(f"Valores: {target.unique()}")
print(f"Distribución:")
print(target.value_counts())
print(f"\nProporción:")
print((target.value_counts() / len(target) * 100).round(2))

# 8. VALORES FALTANTES
print("\n" + "=" * 70)
print("7. VALORES FALTANTES")
print("=" * 70)
missing = df.isnull().sum().sum()
print(f"Total: {missing}")

# 9. CORRELACIONES CON TARGET
print("\n" + "=" * 70)
print("8. ANÁLISIS DE FEATURES (Media de características)")
print("=" * 70)
# Columnas 2-11 son las medias
features_mean = df.iloc[:, 2:12]
print(f"Rango de valores por feature (media):")
print(features_mean.describe().T.to_string())

print("\n" + "=" * 70)
print("RESUMEN BREAST CANCER WISCONSIN (WDBC)")
print("=" * 70)
print(f"✓ {len(df)} muestras de biopsia")
print(f"✓ Clasificación binaria: Maligno vs Benigno")
print(f"✓ 30 características (media, error, peor)")
print(f"✓ Sin valores faltantes")
print(f"✓ Dataset desbalanceado: {(target == 'M').sum()} vs {(target == 'B').sum()}")
print("=" * 70 + "\n")
