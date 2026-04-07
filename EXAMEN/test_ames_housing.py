"""
TEST AMES HOUSING DATASET
Exploración y visualización de datos
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("AMES HOUSING - EXPLORACION DE DATOS")
print("=" * 70)

# Cargar dataset
dataset_path = Path(__file__).resolve().parent / "datasets" / "ames_housing" / "AmesHousing.xls"
print(f"\n[1] Cargando dataset desde: {dataset_path}")

try:
    df = pd.read_excel(dataset_path)
    print("✓ Dataset cargado exitosamente")
except Exception as e:
    print(f"✗ Error al cargar: {e}")
    exit(1)

# 1. INFORMACIÓN BÁSICA
print("\n" + "=" * 70)
print("1. INFORMACIÓN BÁSICA")
print("=" * 70)
print(f"\nShape: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"Memoria usada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 2. PRIMERAS FILAS
print("\n" + "=" * 70)
print("2. PRIMERAS 5 FILAS")
print("=" * 70)
print(df.head().to_string())

# 3. INFORMACIÓN DE COLUMNAS
print("\n" + "=" * 70)
print("3. TIPOS DE DATOS")
print("=" * 70)
print(df.dtypes.value_counts())

# 4. VALORES FALTANTES
print("\n" + "=" * 70)
print("4. ANÁLISIS DE VALORES FALTANTES")
print("=" * 70)
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Columna': missing[missing > 0].index,
    'Nulos': missing[missing > 0].values,
    'Porcentaje': missing_pct[missing > 0].values
})
print(missing_df.to_string(index=False))
print(f"\nTotal columnas con nulos: {(missing > 0).sum()}/{len(df.columns)}")

# 5. ESTADÍSTICAS DESCRIPTIVAS
print("\n" + "=" * 70)
print("5. ESTADÍSTICAS DESCRIPTIVAS (variables numéricas)")
print("=" * 70)
print(df.describe().T.to_string())

# 6. VARIABLE TARGET
print("\n" + "=" * 70)
print("6. ANÁLISIS DEL TARGET (SalePrice)")
print("=" * 70)
if 'SalePrice' in df.columns:
    target = df['SalePrice']
    print(f"Min: ${target.min():,.0f}")
    print(f"Max: ${target.max():,.0f}")
    print(f"Mean: ${target.mean():,.0f}")
    print(f"Median: ${target.median():,.0f}")
    print(f"Std Dev: ${target.std():,.0f}")
    print(f"Nulos: {target.isnull().sum()}")
else:
    print("SalePrice no encontrado")

# 7. CORRELACIONES CON TARGET
print("\n" + "=" * 70)
print("7. TOP 10 CORRELACIONES CON SalePrice")
print("=" * 70)
if 'SalePrice' in df.columns:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()['SalePrice'].sort_values(ascending=False)
    print(correlations.head(11)[1:].to_string())  # Excluye SalePrice consigo mismo

# 8. VARIABLES CATEGÓRICAS
print("\n" + "=" * 70)
print("8. VARIABLES CATEGÓRICAS")
print("=" * 70)
categorical_cols = df.select_dtypes(include='object').columns
print(f"Total: {len(categorical_cols)} columnas categóricas")
print("\nPrimeras 5:")
for col in categorical_cols[:5]:
    print(f"  {col}: {df[col].nunique()} valores únicos")

# 9. OUTLIERS EN SALEPRICE
print("\n" + "=" * 70)
print("9. ANÁLISIS DE OUTLIERS (SalePrice)")
print("=" * 70)
if 'SalePrice' in df.columns:
    Q1 = df['SalePrice'].quantile(0.25)
    Q3 = df['SalePrice'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df['SalePrice'] < lower_bound) | (df['SalePrice'] > upper_bound)]
    print(f"Outliers detectados: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")
    print(f"Rango válido: ${lower_bound:,.0f} - ${upper_bound:,.0f}")

# 10. RESUMEN FINAL
print("\n" + "=" * 70)
print("10. RESUMEN FINAL")
print("=" * 70)
print(f"✓ Dataset completamente explorado")
print(f"✓ Listo para modelado")
print(f"✓ Recomendación: Manejo de valores faltantes + Escalado numérico")
print("=" * 70 + "\n")
