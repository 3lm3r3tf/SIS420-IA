"""
TEST NHANES DATASET
Examen Nacional de Salud y Nutrición
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("NHANES - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "nhanes"

# Cargar archivo XPT (SAS export format)
print("\n[1] Cargando AUQ_L.xpt (audiología)...")

try:
    df = pd.read_sas(datasets_path / "AUQ_L.xpt", format="xport")
    print(f"✓ Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# 2. INFORMACIÓN BÁSICA
print("\n" + "=" * 70)
print("1. INFORMACIÓN BÁSICA")
print("=" * 70)
print(f"Shape: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 3. COLUMNAS
print("\n" + "=" * 70)
print("2. COLUMNAS Y TIPOS")
print("=" * 70)
print(f"\nColumnas ({len(df.columns)}):")
for i, col in enumerate(df.columns):
    print(f"  {i+1}. {col}: {df[col].dtype}")

# 4. PRIMERAS FILAS
print("\n" + "=" * 70)
print("3. PRIMERAS 3 FILAS")
print("=" * 70)
print(df.head(3).to_string())

# 5. ESTADÍSTICAS
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS DESCRIPTIVAS")
print("=" * 70)
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 0:
    print(df[numeric_cols].describe().to_string())

# 6. VALORES FALTANTES
print("\n" + "=" * 70)
print("5. VALORES FALTANTES")
print("=" * 70)
missing = df.isnull().sum()
if missing.sum() > 0:
    missing_df = pd.DataFrame({
        'Columna': missing[missing > 0].index,
        'Nulos': missing[missing > 0].values,
        'Porcentaje': (missing[missing > 0] / len(df) * 100).round(2).values
    })
    print(missing_df.to_string(index=False))
else:
    print("Sin valores faltantes")

# 7. VARIABLES DE IDENTIFICACIÓN
print("\n" + "=" * 70)
print("6. VARIABLES CLAVE")
print("=" * 70)
print(f"SEQN (ID único): {df['SEQN'].nunique()} registros únicos")
if 'AUQ054' in df.columns:
    print(f"AUQ054 (Hearing difficulty): {df['AUQ054'].value_counts().to_dict()}")

print("\n" + "=" * 70)
print("RESUMEN NHANES")
print("=" * 70)
print("✓ Datos de salud pública")
print("✓ Diseño complejo de encuesta")
print("✓ Auditoría y pruebas de audición")
print("=" * 70 + "\n")
