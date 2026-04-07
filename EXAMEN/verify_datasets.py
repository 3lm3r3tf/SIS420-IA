"""
EXAM PREP: Verificación de Datasets Locales
Genera reporte técnico de cada dataset descargado
Corre SIN internet - válido para examen
"""

import pandas as pd
import os
import json
from pathlib import Path
import numpy as np

# Configuración
BASE_DIR = Path(__file__).resolve().parent
DATASETS_PATH = BASE_DIR / "datasets"
REPORT_PATH = BASE_DIR / "DATASETS_REPORT.md"

# Definir cómo cargar cada dataset
DATASET_LOADERS = {
    "ames_housing": {
        "files": ["AmesHousing.xls"],
        "loader": lambda f: pd.read_excel(f),
        "target": "SalePrice"
    },
    "mimic_iii_demo": {
        "files": ["PATIENTS.csv", "ADMISSIONS.csv"],
        "loader": lambda f: pd.read_csv(f),
        "target": "subject_id"  # No target real, es base para otros CSVs
    },
    "nhanes": {
        "files": ["AUQ_L.xpt"],
        "loader": lambda f: pd.read_sas(f, format="xport"),
        "target": None
    },
    "bike_sharing": {
        "files": ["train.csv"],
        "loader": lambda f: pd.read_csv(f),
        "target": "count"
    },
    "adult": {
        "files": ["adult.data"],
        "loader": lambda f: pd.read_csv(f, header=None),
        "target": None  # Última columna
    },
    "credit_approval": {
        "files": ["crx.data"],
        "loader": lambda f: pd.read_csv(f, header=None),
        "target": None  # Última columna
    },
    "statlog_australian_credit": {
        "files": ["australian.dat"],
        "loader": lambda f: pd.read_csv(f, header=None, sep=" "),
        "target": None  # Última columna
    },
    "breast_cancer_wisconsin": {
        "files": ["wdbc.data"],
        "loader": lambda f: pd.read_csv(f, header=None),
        "target": None  # Segunda columna es el target (diagnosis)
    },
    "meningitis_missing": {
        "files": ["mening missing 12.csv"],
        "loader": lambda f: pd.read_csv(f),
        "target": None
    }
}

def load_and_summarize_dataset(dataset_name, config):
    """Carga un dataset y genera resumen técnico"""
    
    report = {}
    errors = []
    
    for file in config["files"]:
        file_path = DATASETS_PATH / dataset_name / file
        
        if not file_path.exists():
            errors.append(f"[ERROR] Archivo no encontrado: {file}")
            continue
        
        try:
            df = config["loader"](str(file_path))
            
            # Generar resumen
            report[file] = {
                "shape": df.shape,
                "columnas": list(df.columns),
                "tipos": df.dtypes.to_dict(),
                "nulos": df.isnull().sum().to_dict(),
                "target": config.get("target")
            }
            
            print(f"[OK] {dataset_name}/{file} cargado exitosamente")
            print(f"   Shape: {df.shape} | Nulos: {df.isnull().sum().sum()}")
            
        except Exception as e:
            errors.append(f"[ERROR] Error cargando {file}: {str(e)}")
            print(f"[ERROR] Error en {dataset_name}/{file}: {e}")
    
    return report, errors

def generate_markdown_report(all_reports):
    """Genera reporte en Markdown"""
    
    md_lines = [
        "# Reporte de Datasets - Examen ML",
        "Verificacion local sin internet",
        f"\n**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n---\n"
    ]
    
    for dataset_name, (report, errors) in all_reports.items():
        md_lines.append(f"## {dataset_name.upper()}")
        
        if errors:
            md_lines.append("### Errores:")
            for err in errors:
                md_lines.append(f"- {err}")
        
        if report:
            for file, info in report.items():
                md_lines.append(f"\n### Archivo: `{file}`")
                md_lines.append(f"- **Shape**: {info['shape'][0]} filas x {info['shape'][1]} columnas")
                md_lines.append(f"- **Target estimado**: {info['target']}")
                md_lines.append(f"- **Columnas**: {len(info['columnas'])}")
                md_lines.append(f"- **Columnas con nulos**: {sum(1 for v in info['nulos'].values() if v > 0)}")
                
                # Listar nulos por columna
                nulos_por_col = {k: v for k, v in info['nulos'].items() if v > 0}
                if nulos_por_col:
                    md_lines.append(f"  - Nulos por columna: {nulos_por_col}")
        
        md_lines.append("\n")
    
    return "\n".join(md_lines)

def main():
    print("=" * 60)
    print("VERIFICACION DE DATASETS - EXAM PREP")
    print("=" * 60 + "\n")
    
    all_reports = {}
    
    for dataset_name, config in DATASET_LOADERS.items():
        print(f"\n[INFO] Procesando: {dataset_name}")
        report, errors = load_and_summarize_dataset(dataset_name, config)
        all_reports[dataset_name] = (report, errors)
    
    # Generar reporte en Markdown
    markdown_report = generate_markdown_report(all_reports)
    
    # Guardar reporte
    with open(REPORT_PATH, "w") as f:
        f.write(markdown_report)
    
    print("\n" + "=" * 60)
    print(f"[OK] Reporte guardado en: {REPORT_PATH}")
    print("=" * 60)
    
    # Mostrar resumen final
    total_datasets = len(DATASET_LOADERS)
    loaded = sum(1 for _, (r, e) in all_reports.items() if r)
    print(f"\nRESUMEN:")
    print(f"- Datasets encontrados: {total_datasets}/9")
    print(f"- Datasets cargados exitosamente: {loaded}/9")
    print("\nListo para examen sin internet [OK]")

if __name__ == "__main__":
    main()
