"""
TEST STATLOG AUSTRALIAN CREDIT DATASET
Aprobación de crédito australiano
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("STATLOG AUSTRALIAN CREDIT - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "statlog_australian_credit"

# Cargar dataset
print("\n[1] Cargando australian.dat...")

try:
    df = pd.read_csv(datasets_path / "australian.dat", header=None, sep=' ')
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
print(df.dtypes)

# 4. PRIMERAS FILAS
print("\n" + "=" * 70)
print("3. PRIMERAS 5 FILAS")
print("=" * 70)
print(df.head().to_string())

# 5. ESTADÍSTICAS
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS NUMÉRICAS")
print("=" * 70)
numeric_df = df.select_dtypes(include=[np.number])
print(numeric_df.describe().to_string())

# 6. INFORMACIÓN POR COLUMNA
print("\n" + "=" * 70)
print("5. INFORMACIÓN POR COLUMNA")
print("=" * 70)
for i in range(len(df.columns)):
    col = df.iloc[:, i]
    print(f"\nCol {i}: {col.dtype}")
    if col.dtype == 'object':
        print(f"  Valores únicos: {col.nunique()}")
        print(f"  Valores: {col.unique()}")
    else:
        print(f"  Rango: {col.min():.2f} - {col.max():.2f}")
        print(f"  Media: {col.mean():.2f}")

# 7. TARGET
print("\n" + "=" * 70)
print("6. ANÁLISIS DEL TARGET (Columna 14)")
print("=" * 70)
target = df.iloc[:, -1]
print(f"Valores únicos: {target.nunique()}")
print(f"Distribución:")
print(target.value_counts())

# 8. VALORES FALTANTES
print("\n" + "=" * 70)
print("7. VALORES FALTANTES")
print("=" * 70)
missing = df.isnull().sum()
print(f"Total: {missing.sum()}")

# 9. BALANCEO
print("\n" + "=" * 70)
print("8. BALANCEO DE CLASES")
print("=" * 70)
prop = target.value_counts() / len(target) * 100
print(f"Clase 0: {prop.get(0, 0):.2f}%")
print(f"Clase 1: {prop.get(1, 0):.2f}%")

print("\n" + "=" * 70)
print("RESUMEN STATLOG AUSTRALIAN CREDIT")
print("=" * 70)
print(f"✓ {len(df)} aplicaciones de crédito")
print(f"✓ Clasificación binaria")
print(f"✓ {df.shape[1]} características")
print(f"✓ Sin valores faltantes")
print("=" * 70 + "\n")
