"""
TEST ADULT DATASET
Predicción de ingresos > 50K
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("ADULT - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "adult"

# Cargar dataset
print("\n[1] Cargando adult.data...")

# Nombres de columnas según documentación UCI
column_names = [
    'age', 'workclass', 'fnlwgt', 'education', 'education-num',
    'marital-status', 'occupation', 'relationship', 'race', 'sex',
    'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
]

try:
    df = pd.read_csv(datasets_path / "adult.data", header=None, names=column_names, sep=', ')
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

# 5. ESTADÍSTICAS NUMÉRICAS
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS (variables numéricas)")
print("=" * 70)
print(df.describe().to_string())

# 6. TARGET
print("\n" + "=" * 70)
print("5. ANÁLISIS DEL TARGET (income)")
print("=" * 70)
print(df['income'].value_counts())
print(f"\nProporción >50K: {(df['income'] == ' >50K').sum() / len(df) * 100:.2f}%")

# 7. VARIABLES CATEGÓRICAS
print("\n" + "=" * 70)
print("6. VARIABLES CATEGÓRICAS")
print("=" * 70)
categorical = df.select_dtypes(include=['object']).columns
for col in categorical:
    if col != 'income':
        print(f"\n{col}: {df[col].nunique()} valores")
        print(df[col].value_counts().head(5).to_string())

# 8. VALORES FALTANTES
print("\n" + "=" * 70)
print("7. VALORES FALTANTES")
print("=" * 70)
missing = df.isnull().sum()
print(f"Total: {missing.sum()}")
if missing.sum() > 0:
    print(missing[missing > 0])

# 9. EDAD Y EDUCACIÓN
print("\n" + "=" * 70)
print("8. DISTRIBUCIONES CLAVE")
print("=" * 70)
print(f"\nEdad - Min: {df['age'].min()}, Max: {df['age'].max()}, Media: {df['age'].mean():.1f}")
print(f"Horas semana - Min: {df['hours-per-week'].min()}, Max: {df['hours-per-week'].max()}, Media: {df['hours-per-week'].mean():.1f}")
print(f"\nEducación:")
print(df['education'].value_counts())
print(f"\nSexo:")
print(df['sex'].value_counts())

print("\n" + "=" * 70)
print("RESUMEN ADULT (Income Prediction)")
print("=" * 70)
print(f"✓ {len(df)} registros de censos")
print(f"✓ Problema de clasificación binaria (income > 50K)")
print(f"✓ Mix de variables categóricas y numéricas")
print(f"✓ Dataset desbalanceado ({(df['income'] == ' <=50K').sum()} vs {(df['income'] == ' >50K').sum()})")
print("=" * 70 + "\n")
