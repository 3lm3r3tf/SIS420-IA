"""
TEST MIMIC III DEMO DATASET
Exploración de datos clínicos
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("MIMIC III DEMO - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "mimic_iii_demo"

# 1. PATIENTS.csv
print("\n" + "=" * 70)
print("1. PATIENTS.csv")
print("=" * 70)

try:
    df_patients = pd.read_csv(datasets_path / "PATIENTS.csv")
    print(f"✓ Cargado: {df_patients.shape[0]} filas x {df_patients.shape[1]} columnas")
    print(f"\nColumnas: {list(df_patients.columns)}")
    print(f"\nPrimero 3 filas:\n{df_patients.head(3).to_string()}")
    print(f"\nNulos por columna:\n{df_patients.isnull().sum()}")
    print(f"\nEstadísticas:\n{df_patients.describe()}")
except Exception as e:
    print(f"✗ Error: {e}")

# 2. ADMISSIONS.csv
print("\n" + "=" * 70)
print("2. ADMISSIONS.csv")
print("=" * 70)

try:
    df_admissions = pd.read_csv(datasets_path / "ADMISSIONS.csv")
    print(f"✓ Cargado: {df_admissions.shape[0]} filas x {df_admissions.shape[1]} columnas")
    print(f"\nColumnas: {list(df_admissions.columns)}")
    print(f"\nPrimero 3 filas:\n{df_admissions.head(3).to_string()}")
    print(f"\nNulos por columna:\n{df_admissions.isnull().sum()}")
    print(f"\nTipos de datos:\n{df_admissions.dtypes}")
    
    # Análisis de admisiones
    if 'admission_type' in df_admissions.columns:
        print(f"\nTipos de admisión:\n{df_admissions['admission_type'].value_counts()}")
except Exception as e:
    print(f"✗ Error: {e}")

# 3. CHARTEVENTS.csv (si existe)
print("\n" + "=" * 70)
print("3. CHARTEVENTS.csv")
print("=" * 70)

try:
    df_chart = pd.read_csv(datasets_path / "CHARTEVENTS.csv", nrows=100)
    print(f"✓ Primeras 100 filas cargadas: {df_chart.shape[1]} columnas")
    print(f"\nColumnas: {list(df_chart.columns)}")
    print(f"{df_chart.head(2).to_string()}")
except Exception as e:
    print(f"✗ No disponible o error: {e}")

print("\n" + "=" * 70)
print("RESUMEN MIMIC III")
print("=" * 70)
print("✓ Base de datos clínica de UCI")
print("✓ Múltiples tablas para análisis temporal")
print("✓ Listo para análisis de supervivencia")
print("=" * 70 + "\n")
