import numpy as np


def build_comparison_matrix(values, c):
    mn = min(values)
    mx = max(values)
    scale_ratio = mx / mn / 9

    matrix = np.ones((len(values), len(values)))

    for i in range(len(values)):
        for j in range(len(values)):
            if i != j:
                if values[j] != 0:
                    ratio = values[i] / values[j]
                    if ratio >= 1:
                        scaled_value = max(round(ratio / scale_ratio), 1)
                    else:
                        scaled_value = 1 / max(round((1 / ratio) / scale_ratio), 1)
                    if not c:
                        scaled_value = 1 / scaled_value
                    matrix[i, j] = scaled_value
                else:
                    matrix[i, j] = 9
    return matrix


def calculate_consistency_ratio(matrix: np.ndarray) -> float:
    n = matrix.shape[0]
    eigenvalues = np.linalg.eigvals(matrix)
    lambda_max = np.max(eigenvalues).real
    CI = (lambda_max - n) / (n - 1)

    RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    RI = RI_dict.get(n, 1.49)

    return CI / RI if RI != 0 else 0


def adjust_matrix(matrix: np.ndarray, s=0) -> np.ndarray:
    mtx = []
    consistency = calculate_consistency_ratio(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            mtx1 = matrix.copy()
            mtx2 = matrix.copy()
            if matrix[i, j] % 1 == 0:
                mtx1[i, j] = max(int(mtx1[i, j]) - 1, 1)
                mtx1[j, i] = 1 / mtx1[i, j]
                mtx2[i, j] = min(int(mtx2[i, j]) + 1, 9)
                mtx2[j, i] = 1 / mtx2[i, j]
            else:
                mtx1[j, i] = min(int(mtx1[j, i]) - 1, 1)
                mtx1[i, j] = 1 / mtx1[j, i]
                mtx1[j, i] = max(int(mtx1[j, i]) + 1, 9)
                mtx1[i, j] = 1 / mtx1[j, i]
            if consistency > calculate_consistency_ratio(mtx1):
                mtx = mtx1.copy()
                consistency = calculate_consistency_ratio(mtx1)
            if consistency > calculate_consistency_ratio(mtx2):
                mtx = mtx2.copy()
                consistency = calculate_consistency_ratio(mtx2)
    if consistency <= 0.1 or s > 10:
        return mtx
    return adjust_matrix(mtx, s + 1)


def calculate_vector(mtx):
    v, w = [], []
    for i in mtx:
        s = 1
        for j in i:
            s *= j
        s **= 0.2
        v.append(s)

    for i in v:
        w.append(i / sum(v))

    return w


def synthesize(criteria_matrix, values, alternatives, comparison):
    w = calculate_vector(criteria_matrix)

    alts = {}
    for i in alternatives:
        alts[i] = 0

    for i in range(len(values)):
        matrix = build_comparison_matrix(values[i], comparison[i] == "+")
        if calculate_consistency_ratio(matrix) > 0.1:
            matrix = adjust_matrix(matrix)
        wi = calculate_vector(matrix)
        for j in range(len(wi)):
            alts[alternatives[j]] += float(w[i] * wi[j])

    return {"alternatives": alts}


a = synthesize(
    [
        [1, 1.0 / 2.0, 2, 2],
        [2, 1, 2, 4],
        [1.0 / 2.0, 1.0 / 2.0, 1, 2],
        [1.0 / 2.0, 1.0 / 4.0, 1.0 / 2.0, 1],
    ],
    [
        [95, 98, 131, 125, 70, 125, 130, 500, 280, 150],
        [13.5, 10, 11, 16.5, 9, 16, 11, 24, 25, 12],
        [2750, 2000, 2750, 2900, 1750, 2750, 2000, 4500, 3000, 3500],
        [23000, 24000, 25000, 22500, 22500, 23000, 25000, 25000, 25000, 22500],
    ],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ["+", "-", "-", "+"],
)
