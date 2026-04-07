from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PARCIAL - DATASET 5 (STATLOG AUSTRALIAN CREDIT)
# MODELO: REGRESION LOGISTICA BINARIA
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


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def compute_cost(theta, X, y):
    m = y.shape[0]
    h = sigmoid(X @ theta)
    eps = 1e-9
    h = np.clip(h, eps, 1 - eps)
    return (1 / m) * np.sum(-y * np.log(h) - (1 - y) * np.log(1 - h))


def gradient_descent(theta, X, y, alpha, num_iters):
    m = y.shape[0]
    J_history = []
    for _ in range(num_iters):
        h = sigmoid(X @ theta)
        theta = theta - (alpha / m) * (X.T @ (h - y))
        J_history.append(compute_cost(theta, X, y))
    return theta, J_history


def confusion_matrix_manual(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return np.array([[tn, fp], [fn, tp]])


def metrics_manual(y_true, y_pred):
    cm = confusion_matrix_manual(y_true, y_pred)
    tn, fp = cm[0, 0], cm[0, 1]
    fn, tp = cm[1, 0], cm[1, 1]

    acc = (tp + tn) / np.sum(cm)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return acc, precision, recall, f1, cm


def main():
    base = Path(__file__).resolve().parent / "datasets" / "statlog_australian_credit"
    df = pd.read_csv(base / "australian.dat", header=None, sep=" ")

    print("=== DATASET 5: STATLOG AUSTRALIAN CREDIT ===")
    print("Shape:", df.shape)
    print("Target: ultima columna (0/1)")

    X = df.iloc[:, :-1].values.astype(float)
    y = df.iloc[:, -1].values.astype(int)

    # Split 75/25 (requisito del parcial)
    X_train, X_test, y_train, y_test = split_75_25(X, y, seed=42)

    # Normalizacion con estadisticos de train
    X_train_norm, X_test_norm, mu, sigma = feature_normalize_train_test(X_train, X_test)

    # Intercepto
    X_train_i = add_intercept(X_train_norm)
    X_test_i = add_intercept(X_test_norm)

    # Entrenamiento logistica
    theta = np.zeros(X_train_i.shape[1])
    alpha = 0.05
    num_iters = 3000
    theta, J_history = gradient_descent(theta, X_train_i, y_train, alpha, num_iters)

    # Probabilidades y clases
    p_train = sigmoid(X_train_i @ theta)
    p_test = sigmoid(X_test_i @ theta)
    y_pred_train = (p_train >= 0.5).astype(int)
    y_pred_test = (p_test >= 0.5).astype(int)

    # Metricas
    acc_tr, pre_tr, rec_tr, f1_tr, cm_tr = metrics_manual(y_train, y_pred_train)
    acc_te, pre_te, rec_te, f1_te, cm_te = metrics_manual(y_test, y_pred_test)

    print("\n=== RESULTADOS CLASIFICACION ===")
    print(f"Train -> Acc: {acc_tr:.4f}, Prec: {pre_tr:.4f}, Rec: {rec_tr:.4f}, F1: {f1_tr:.4f}")
    print(f"Test  -> Acc: {acc_te:.4f}, Prec: {pre_te:.4f}, Rec: {rec_te:.4f}, F1: {f1_te:.4f}")

    print("\nMatriz de confusion (test) [ [TN, FP], [FN, TP] ]")
    print(cm_te)

    print("\nControl de sobreajuste:")
    if acc_te >= (acc_tr - 0.08):
        print("- Diferencia train/test aceptable. Sobreajuste bajo.")
    else:
        print("- Posible sobreajuste. Revisar features/iteraciones/alpha.")

    # =========================
    # GRAFICOS
    # =========================
    plt.figure(figsize=(7, 4))
    pd.Series(y).value_counts().sort_index().plot(kind="bar")
    plt.title("Statlog - Distribucion de clases (0/1)")
    plt.xlabel("Clase")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(np.arange(len(J_history)), J_history, lw=2)
    plt.title("Statlog - Convergencia del costo logistico")
    plt.xlabel("Iteraciones")
    plt.ylabel("Costo J(theta)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 5))
    plt.imshow(cm_te, cmap="Blues")
    plt.title("Matriz de confusion (test)")
    plt.colorbar()
    plt.xticks([0, 1], ["Pred 0", "Pred 1"])
    plt.yticks([0, 1], ["Real 0", "Real 1"])
    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm_te[i, j], ha="center", va="center", color="black")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
