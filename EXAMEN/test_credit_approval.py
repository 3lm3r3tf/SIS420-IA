"""
TEST CREDIT APPROVAL DATASET
Aprobación de crédito - Clasificación binaria
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("CREDIT APPROVAL - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "credit_approval"

# Cargar dataset
print("\n[1] Cargando crx.data...")

try:
    df = pd.read_csv(datasets_path / "crx.data", header=None)
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

# 5. INFORMACIÓN POR COLUMNA
print("\n" + "=" * 70)
print("4. INFORMACIÓN POR COLUMNA")
print("=" * 70)
for i in range(df.shape[1]):
    col = df.iloc[:, i]
    print(f"\nColumna {i}:")
    try:
        # Intentar conversión numérica
        numeric_col = pd.to_numeric(col, errors='coerce')
        if numeric_col.notna().sum() > df.shape[0] * 0.5:  # Si al menos 50% es numérico
            print(f"  Tipo: Numérica")
            print(f"  Rango: {numeric_col.min():.2f} - {numeric_col.max():.2f}")
            print(f"  Media: {numeric_col.mean():.2f}")
        else:
            print(f"  Tipo: Categórica")
            print(f"  Valores únicos: {col.nunique()}")
            print(f"  Valores: {col.unique()[:10]}")
    except:
        print(f"  Tipo: Categórica/Mixto")
        print(f"  Valores únicos: {col.nunique()}")

# 6. VALORES FALTANTES
print("\n" + "=" * 70)
print("5. VALORES FALTANTES")
print("=" * 70)
missing = df.isnull().sum()
print(f"Total: {missing.sum()}")
if missing.sum() > 0:
    print(missing[missing > 0])

# 7. TARGET (última columna)
print("\n" + "=" * 70)
print("6. ANÁLISIS DEL TARGET (Columna 15)")
print("=" * 70)
target = df.iloc[:, -1]
print(f"Valores únicos: {target.nunique()}")
print(f"Distribución:")
print(target.value_counts())

# 8. ESTADÍSTICAS
print("\n" + "=" * 70)
print("7. ESTADÍSTICAS (numéricas)")
print("=" * 70)
numeric_df = df.select_dtypes(include=[np.number])
if len(numeric_df.columns) > 0:
    print(numeric_df.describe().to_string())

print("\n" + "=" * 70)
print("RESUMEN CREDIT APPROVAL")
print("=" * 70)
print(f"✓ {len(df)} solicitudes de crédito")
print(f"✓ Problema de clasificación (aprobado/rechazado)")
print(f"✓ Datos ficticiados por confidencialidad (valores como A1, A2, etc.)")
print(f"✓ Mix de características")
print("=" * 70 + "\n")
