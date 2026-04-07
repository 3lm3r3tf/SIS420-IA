"""
TEST MENINGITIS MISSING DATASET
Diagnóstico de meningitis con datos faltantes
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("MENINGITIS MISSING - EXPLORACION DE DATOS")
print("=" * 70)

datasets_path = Path(__file__).resolve().parent / "datasets" / "meningitis_missing"

# Cargar dataset
print("\n[1] Cargando mening missing 12.csv...")

try:
    df = pd.read_csv(datasets_path / "mening missing 12.csv")
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

# 6. VALORES FALTANTES - MUY IMPORTANTE
print("\n" + "=" * 70)
print("5. ANÁLISIS DE VALORES FALTANTES (CRÍTICO)")
print("=" * 70)
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Columna': missing[missing > 0].index,
    'Nulos': missing[missing > 0].values,
    'Porcentaje': missing_pct[missing > 0].values
})
print(missing_df.sort_values('Porcentaje', ascending=False).to_string(index=False))
print(f"\nTotal faltantes: {missing.sum()} valores")
print(f"Cobertura promedio: {100 - missing_pct.mean():.2f}%")

# 7. INFORMACIÓN CLÍNICA
print("\n" + "=" * 70)
print("6. DISTRIBUCIONES DE VARIABLES CLAVE")
print("=" * 70)
if 'Gender' in df.columns:
    print(f"\nGénero:")
    print(df['Gender'].value_counts(dropna=False))

if 'Age' in df.columns:
    print(f"\nEdad (sin nulos):")
    print(f"  Min: {df['Age'].min()}")
    print(f"  Max: {df['Age'].max()}")
    print(f"  Media: {df['Age'].mean():.2f}")

if 'Diagnosis' in df.columns:
    print(f"\nDiagnóstico:")
    print(df['Diagnosis'].value_counts(dropna=False))

if 'Outcome' in df.columns:
    print(f"\nResultado:")
    print(df['Outcome'].value_counts(dropna=False))

# 8. CARACTERÍSTICAS CLÍNICAS
print("\n" + "=" * 70)
print("7. CARACTERÍSTICAS CLÍNICAS")
print("=" * 70)
print("""
Variables clínicas:
  - Age: Edad del paciente
  - Gender: Género
  - WBC_Count: Recuento de glóbulos blancos
  - Protein_Level: Nivel de proteína en LCR
  - Glucose_Level: Nivel de glucosa en LCR
  - Pathogen_Present: Presencia de patógeno
  - Hemoglobin: Nivel de hemoglobina
  - WBC_Blood_Count: Recuento de WBC en sangre
  - Platelets: Conteo de plaquetas
  - CRP_Level: Proteína C reactiva
  - Diagnosis: Diagnóstico (TARGET)
  - Outcome: Resultado del tratamiento
""")

# 9. CORRELACIONES (solo numéricas sin nulos)
print("\n" + "=" * 70)
print("8. ANÁLISIS DE COMPLETITUD POR VARIABLE")
print("=" * 70)
complete_pct = (1 - df.isnull().sum() / len(df)) * 100
for col in df.columns:
    print(f"{col:20s}: {complete_pct[col]:6.2f}% completo ({df[col].isnull().sum():4d} nulos)")

print("\n" + "=" * 70)
print("RESUMEN MENINGITIS MISSING")
print("=" * 70)
print(f"✓ {len(df)} pacientes con meningitis")
print(f"✓ {df.shape[1]} variables clínicas")
print(f"✓ ⚠ Datos ALTAMENTE faltantes (causa del nombre)")
print(f"✓ Problema de imputación / análisis con valores faltantes")
print(f"✓ Ideal para técnicas MCAR/MAR/MNAR")
print("=" * 70 + "\n")
