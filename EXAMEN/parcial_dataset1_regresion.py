from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# ============================================================
# PARCIAL - DATASET 1 (AMES HOUSING)
# MODELO: REGRESION LINEAL MULTIVARIABLE
# REGLA PEDIDA: Split 75% train / 25% test
# ============================================================
def split_75_25(X, y, seed=42):
    np.random.seed(seed)
    m = X.shape[0]
    idx = np.random.permutation(m)
    train_size = int(0.75 * m)
    train_idx = idx[:train_size]
    test_idx = idx[train_size:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def feature_normalize_train_test(X_train, X_test):
    mu = np.mean(X_train, axis=0)
    sigma = np.std(X_train, axis=0)
    sigma[sigma == 0] = 1.0
    X_train_norm = (X_train - mu) / sigma
    X_test_norm = (X_test - mu) / sigma
    return X_train_norm, X_test_norm, mu, sigma


def add_intercept(X):
    return np.concatenate([np.ones((X.shape[0], 1)), X], axis=1)


def compute_cost(X, y, theta):
    m = y.shape[0]
    return (1 / (2 * m)) * np.sum((X @ theta - y) ** 2)


def gradient_descent(X, y, theta, alpha, num_iters):
    m = y.shape[0]
    J_history = []
    for _ in range(num_iters):
        theta = theta - (alpha / m) * (X.T @ (X @ theta - y))
        J_history.append(compute_cost(X, y, theta))
    return theta, J_history


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)


def main():
    base = Path(__file__).resolve().parent / "datasets" / "ames_housing"
    df = pd.read_excel(base / "AmesHousing.xls")

    print("=== DATASET 1: AMES HOUSING ===")
    print("Shape:", df.shape)
    print("Target: SalePrice")

    # Se usan solo variables numericas para mantener tecnica vista en clase.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols.remove("SalePrice")

    # Se toman 10 features numericas con menos nulos para reducir ruido y sobreajuste.
    null_count = df[numeric_cols].isnull().sum().sort_values()
    selected_features = list(null_count.index[:10])

    work = df[selected_features + ["SalePrice"]].dropna().copy()
    X = work[selected_features].values
    y = work["SalePrice"].values

    print("Filas usadas despues de limpieza:", X.shape[0])
    print("Features seleccionadas:", selected_features)

    # Split 75/25 (requisito del parcial)
    X_train, X_test, y_train, y_test = split_75_25(X, y, seed=42)

    # Normalizacion con estadisticos de train
    X_train_norm, X_test_norm, mu, sigma = feature_normalize_train_test(X_train, X_test)

    # Agregar intercepto
    X_train_i = add_intercept(X_train_norm)
    X_test_i = add_intercept(X_test_norm)

    # Entrenamiento por descenso del gradiente
    theta = np.zeros(X_train_i.shape[1])
    alpha = 0.01
    num_iters = 2500
    theta, J_history = gradient_descent(X_train_i, y_train, theta, alpha, num_iters)

    # Predicciones
    y_pred_train = X_train_i @ theta
    y_pred_test = X_test_i @ theta

    # Metricas
    train_rmse = rmse(y_train, y_pred_train)
    test_rmse = rmse(y_test, y_pred_test)
    train_mae = mae(y_train, y_pred_train)
    test_mae = mae(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)

    print("\n=== RESULTADOS REGRESION ===")
    print(f"RMSE train: {train_rmse:.2f}")
    print(f"RMSE test : {test_rmse:.2f}")
    print(f"MAE train : {train_mae:.2f}")
    print(f"MAE test  : {test_mae:.2f}")
    print(f"R2 train  : {train_r2:.4f}")
    print(f"R2 test   : {test_r2:.4f}")

    print("\nControl de sobreajuste:")
    if test_rmse <= train_rmse * 1.25:
        print("- Diferencia train/test aceptable. Sobreajuste bajo.")
    else:
        print("- Posible sobreajuste. Conviene simplificar features o regularizar.")

    # =========================
    # GRAFICOS
    # =========================
    plt.figure(figsize=(8, 5))
    plt.hist(y, bins=40)
    plt.title("Ames Housing - Distribucion de SalePrice")
    plt.xlabel("SalePrice")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(np.arange(len(J_history)), J_history, lw=2)
    plt.title("Ames Housing - Convergencia del costo")
    plt.xlabel("Iteraciones")
    plt.ylabel("Costo J(theta)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred_test, alpha=0.5)
    min_v = min(np.min(y_test), np.min(y_pred_test))
    max_v = max(np.max(y_test), np.max(y_pred_test))
    plt.plot([min_v, max_v], [min_v, max_v], 'r--')
    plt.title("Ames Housing - Real vs Predicho (test)")
    plt.xlabel("Real")
    plt.ylabel("Predicho")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
