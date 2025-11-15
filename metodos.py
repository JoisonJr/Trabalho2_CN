import numpy as np

# ==========================
# Funções auxiliares de Cálculo
# ==========================

def resolver_sistema_direto(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    # função que retorna a solução do sistema linear ax=b
    return np.linalg.solve(A, b)


def metodo_gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=10000):
    # cópia das matrizes presentes nas entradas da função
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    # tamanho de linhas da matriz
    n = len(b)
    # inicializa uma matriz linha para as operaçoes em linha
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)

    for k in range(max_iter):
        x_ant = x.copy()
        for i in range(n):
            soma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x_ant[i + 1:])
            x[i] = (b[i] - soma) / A[i, i]
        if np.linalg.norm(x - x_ant, ord=np.inf) < tol:
            return x, k + 1
    raise RuntimeError("Método de Gauss-Seidel não convergiu.")


def regra_trapezio(x, y):
    x, y = np.array(x), np.array(y)
    h = (x[-1] - x[0]) / (len(x) - 1)
    return (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


def regra_simpson(x, y):
    x, y = np.array(x), np.array(y)
    n = len(x) - 1
    if n % 2 == 1:
        raise ValueError("A Regra de Simpson composta requer número par de subintervalos.")
    h = (x[-1] - x[0]) / n
    return (h / 3) * (y[0] + 2 * np.sum(y[2:-1:2]) + 4 * np.sum(y[1::2]) + y[-1])
