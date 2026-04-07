from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_dataset(file_path: Path) -> pd.DataFrame:
    extension = file_path.suffix.lower()

    if extension in {".csv", ".txt"}:
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.read_csv(file_path, sep=";")
    if extension in {".xls", ".xlsx"}:
        return pd.read_excel(file_path)
    if extension == ".xpt":
        return pd.read_sas(file_path, format="xport")
    if extension in {".dat", ".data"}:
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.read_csv(file_path, header=None)

    raise ValueError(f"Formato no soportado: {extension}")


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(column) for column in df.columns]
    return df


def print_summary(df: pd.DataFrame) -> None:
    print("=" * 70)
    print("RESUMEN DEL DATASET")
    print("=" * 70)
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")
    print(f"Memoria aproximada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print("\nPrimeras 5 filas:")
    print(df.head().to_string())
    print("\nTipos de datos:")
    print(df.dtypes.to_string())
    print("\nValores nulos por columna:")
    print(df.isnull().sum().to_string())


def plot_numeric_columns(df: pd.DataFrame, max_columns: int = 6, save_dir: Path | None = None) -> None:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    if not numeric_columns:
        print("No se encontraron columnas numericas para graficar.")
        return

    selected_columns = numeric_columns[:max_columns]
    total = len(selected_columns)
    rows = (total + 1) // 2

    fig, axes = plt.subplots(rows, 2, figsize=(14, 4 * rows))
    axes = axes.flatten() if total > 1 else [axes]

    for index, column in enumerate(selected_columns):
        axes[index].hist(df[column].dropna(), bins=30, color="#2E86AB", alpha=0.85, edgecolor="black")
        axes[index].set_title(f"Histograma: {column}")
        axes[index].set_xlabel(column)
        axes[index].set_ylabel("Frecuencia")

    for index in range(total, len(axes)):
        axes[index].axis("off")

    fig.tight_layout()

    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "numerical_histograms.png", dpi=150, bbox_inches="tight")

    plt.show()


def plot_categorical_columns(df: pd.DataFrame, max_columns: int = 4, top_values: int = 10, save_dir: Path | None = None) -> None:
    categorical_columns = df.select_dtypes(include="object").columns.tolist()
    if not categorical_columns:
        print("No se encontraron columnas categoricas para graficar.")
        return

    selected_columns = categorical_columns[:max_columns]
    total = len(selected_columns)
    rows = (total + 1) // 2

    fig, axes = plt.subplots(rows, 2, figsize=(16, 5 * rows))
    axes = axes.flatten() if total > 1 else [axes]

    for index, column in enumerate(selected_columns):
        counts = df[column].astype(str).fillna("NaN").value_counts().head(top_values)
        axes[index].bar(counts.index.astype(str), counts.values, color="#F18F01")
        axes[index].set_title(f"Categorias: {column}")
        axes[index].tick_params(axis="x", rotation=45)
        axes[index].set_ylabel("Frecuencia")

    for index in range(total, len(axes)):
        axes[index].axis("off")

    fig.tight_layout()

    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "categorical_bars.png", dpi=150, bbox_inches="tight")

    plt.show()


def plot_scatter_numeric_pair(df: pd.DataFrame, save_dir: Path | None = None) -> None:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_columns) < 2:
        print("No hay suficientes columnas numericas para scatter.")
        return

    first_column, second_column = numeric_columns[0], numeric_columns[1]

    plt.figure(figsize=(8, 6))
    plt.scatter(df[first_column], df[second_column], alpha=0.5, color="#6A4C93")
    plt.title(f"Scatter: {first_column} vs {second_column}")
    plt.xlabel(first_column)
    plt.ylabel(second_column)
    plt.tight_layout()

    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_dir / "scatter_numeric_pair.png", dpi=150, bbox_inches="tight")

    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ver cualquier dataset con resumen y graficos basicos.")
    parser.add_argument("file", nargs="?", default=None, help="Ruta al archivo del dataset")
    parser.add_argument("--save-dir", default=None, help="Carpeta opcional para guardar graficos")
    parser.add_argument("--max-numeric", type=int, default=6, help="Maximo de columnas numericas a graficar")
    parser.add_argument("--max-categorical", type=int, default=4, help="Maximo de columnas categoricas a graficar")
    args = parser.parse_args()

    if args.file is None:
        print("No se paso archivo por argumento.")
        print("Ejemplos:")
        print(r"  python EXAMEN/ver_dataset.py EXAMEN/datasets/adult/adult.data")
        print(r"  python EXAMEN/ver_dataset.py EXAMEN/datasets/ames_housing/AmesHousing.xls")
        args.file = input("Ingresa la ruta del archivo del dataset: ").strip()

    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")

    df = normalize_column_names(load_dataset(file_path))
    save_dir = Path(args.save_dir).expanduser().resolve() if args.save_dir else None

    print_summary(df)

    print("\n" + "=" * 70)
    print("GRAFICOS")
    print("=" * 70)
    plot_numeric_columns(df, max_columns=args.max_numeric, save_dir=save_dir)
    plot_categorical_columns(df, max_columns=args.max_categorical, save_dir=save_dir)
    plot_scatter_numeric_pair(df, save_dir=save_dir)


if __name__ == "__main__":
    main()