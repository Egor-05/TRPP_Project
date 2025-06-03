import pandas as pd
import numpy as np

# Создание DataFrame с новыми данными
alternatives = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
criteria = {
    'Частота': [900, 1000, 1700, 2000, 1000, 1300, 1500, 1000, 1500, 1400],
    'Скорость': [400, 650, 400, 450, 400, 650, 400, 450, 520, 400],
    'Цена': [14000, 13500, 9000, 9500, 7500, 8900, 8000, 7200, 6800, 6200],
    'Вес': [63, 63, 74, 133, 121, 101, 67, 59, 56, 49]
}

df = pd.DataFrame(criteria, index=alternatives)
df1 = df.copy()
print(df)

# Обратные значения для минимизируемых критериев
df['Вес'] = 1 / df['Вес']
df['Цена'] = 1 / df['Цена']

# Попарное сравнение альтернатив
comparison_matrix = np.full((len(alternatives), len(alternatives)), '', dtype=object)

for i in range(len(df)):
    for j in range(i + 1, len(df)):

        dominates_i = all(df.iloc[i] >= df.iloc[j])
        dominates_j = all(df.iloc[j] >= df.iloc[i])

        if dominates_i:
            comparison_matrix[j, i] = alternatives[i]
        elif dominates_j:
            comparison_matrix[j, i] = alternatives[j]
        else:
            comparison_matrix[j, i] = 'н'

comparison_df = pd.DataFrame(comparison_matrix, index=alternatives, columns=alternatives)

df = df1

print("\nПопарное сравнение альтернатив:")
print(comparison_df)

# Фильтрация по границам
print("\nУстановка верхних и нижних границ: (Частота опроса >= 1500, Цена <= 9000)")
filtered_df = df[(df['Цена'] <= 9000) & (df['Частота'] >= 1500)]
print(filtered_df)

# Фильтрация по дополнительным критериям
print("\nСубоптимизация: главный критерий: цена, Вес <= 80, Скорость отслеживания >= 500), Частота >=1000")

filtered_criteria = df[(df['Вес'] <= 80) & (df['Скорость'] >= 500) & (df['Частота'] >= 1000)].sort_values(['Цена']).head(1)
print(filtered_criteria)

# Лексикографическая оптимизация
print("\nЛексикографическая оптимизация. Приоритетность: частота опроса, скорость отслеживания, цена, вес")
lexicographic_optimal = df.sort_values(['Частота', 'Скорость', 'Цена', 'Вес']).tail(1)
print(lexicographic_optimal)


def paretto(alternatives, criteria, comparison):
    for i in range(len(criteria)):
        if comparison[i] == '-':
            for j in range(len(criteria[i])):
                criteria[i][j] = -criteria[i][j]
    comparison_matrix = np.full((len(alternatives), len(alternatives)), '', dtype=object)

    criteria = np.array(criteria)
    paretto_set = []

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
                paretto_set.append(alternatives[i])
    return paretto_set


c = [
    [900, 1000, 1700, 2000, 1000, 1300, 1500, 1000, 1500, 1400],
    [400, 650, 400, 450, 400, 650, 400, 450, 520, 400],
    [14000, 13500, 9000, 9500, 7500, 8900, 8000, 7200, 6800, 6200],
    [63, 63, 74, 133, 121, 101, 67, 59, 56, 49]
]

print(paretto(alternatives, c, ['+', '+', '-', '-']))