"""
TEST BIKE SHARING DATASET
Predicción de demanda de bicicletas compartidas
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("BIKE SHARING - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "bike_sharing"

# Cargar dataset
print("\n[1] Cargando train.csv...")

try:
    df = pd.read_csv(datasets_path / "train.csv")
    print(f"✓ Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# 2. INFORMACIÓN BÁSICA
print("\n" + "=" * 70)
print("1. INFORMACIÓN BÁSICA")
print("=" * 70)
print(f"Shape: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"Rango temporal: {df['datetime'].min()} a {df['datetime'].max()}")

# 3. COLUMNAS
print("\n" + "=" * 70)
print("2. COLUMNAS Y TIPOS")
print("=" * 70)
print(df.dtypes)

# 4. PRIMERAS FILAS
print("\n" + "=" * 70)
print("3. PRIMERAS 5 FILAS")
print("=" * 70)
print(df.head().to_string())

# 5. ESTADÍSTICAS
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS DESCRIPTIVAS")
print("=" * 70)
print(df.describe().to_string())

# 6. TARGET: count (demanda)
print("\n" + "=" * 70)
print("5. ANÁLISIS DEL TARGET (count - demanda)")
print("=" * 70)
print(f"Min: {df['count'].min()}")
print(f"Max: {df['count'].max()}")
print(f"Media: {df['count'].mean():.2f}")
print(f"Mediana: {df['count'].median():.2f}")
print(f"Std Dev: {df['count'].std():.2f}")
print(f"Nulos: {df['count'].isnull().sum()}")

# 7. INFORMACIÓN DE FEATURES
print("\n" + "=" * 70)
print("6. INTERPRETACIÓN DE FEATURES")
print("=" * 70)
print("""
datetime    - Fecha y hora (índice temporal)
season      - Estación (1=Invierno, 2=Primavera, 3=Verano, 4=Otoño)
holiday     - Día feriado (1=Sí, 0=No)
workingday  - Día laboral (1=Sí, 0=No)
weather     - Condición climática (1-4)
temp        - Temperatura (Celsius)
atemp       - Temperatura "sentida" (Celsius)
humidity    - Humedad relativa (%)
windspeed   - Velocidad del viento
casual      - Usuarios casuales (sin registro)
registered - Usuarios registrados
count       - Total de bicicletas alquiladas (TARGET)
""")

# 8. CORRELACIONES
print("\n" + "=" * 70)
print("7. CORRELACIONES CON COUNT")
print("=" * 70)
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['count'].sort_values(ascending=False)
print(correlations.to_string())

# 9. VARIABLES CATEGÓRICAS
print("\n" + "=" * 70)
print("8. DISTRIBUCIONES CATEGÓRICAS")
print("=" * 70)
print(f"\nSeasons: {df['season'].value_counts().to_dict()}")
print(f"Holiday: {df['holiday'].value_counts().to_dict()}")
print(f"Working day: {df['workingday'].value_counts().to_dict()}")
print(f"Weather: {df['weather'].value_counts().to_dict()}")

print("\n" + "=" * 70)
print("RESUMEN BIKE SHARING")
print("=" * 70)
print("✓ Datos de series temporales")
print(f"✓ {len(df)} registros horarios")
print("✓ Problema de regresión: predicción de demanda")
print("✓ Sin valores faltantes")
print("=" * 70 + "\n")
