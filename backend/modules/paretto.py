import numpy as np


def paretto(alternatives, criteria, comparison):
    for i in range(len(criteria)):
        if comparison[i] == "-":
            for j in range(len(criteria[i])):
                criteria[i][j] = -criteria[i][j]

    criteria = np.array(criteria)
    paretto_set = {}

    for i in range(len(alternatives)):
        dominating = False
        for j in range(len(alternatives)):
            if i == j:
                continue
            dominates_i = all(a >= b for a, b in zip(criteria[:, i], criteria[:, j]))
            dominates_j = all(a <= b for a, b in zip(criteria[:, i], criteria[:, j]))

            if dominates_i:
                dominating = True
            elif dominates_j:
                break
        else:
            if dominating:
                paretto_set[alternatives[i]] = [abs(int(j)) for j in criteria[:, i]]
    return {'paretto_set': list(paretto_set.keys())}
