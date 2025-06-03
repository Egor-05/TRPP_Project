import math
from typing import List, Tuple, Dict


def initialization() -> Tuple[List[List[float]], List[float], List[float]]:
    """Инициализация матрицы затрат, поставщиков и потребителей"""
    mtx = [
        [2.0, 6.0, 3.0, 4.0, 9.0],
        [1.0, 5.0, 6.0, 9.0, 7.0],
        [3.0, 4.0, 1.0, 6.0, 10.0]
    ]
    suppliers = [20.0, 34.0, 16.0, 10.0, 25.0]
    buyers = [40.0, 30.0, 35.0]
    return mtx, suppliers, buyers


def north_west_corner(mtx: List[List[float]],
                      suppliers: List[float],
                      buyers: List[float]) -> Tuple[List[List[float]], float]:
    """Метод северо-западного угла"""
    matrix = [[0.0 for _ in range(len(mtx[0]))] for _ in range(len(mtx))]
    result = 0.0
    j = 0

    for i in range(len(mtx)):
        while buyers[i] > 0:
            if j >= len(suppliers):
                break
            if suppliers[j] == 0:
                j += 1
                continue

            diff = min(suppliers[j], buyers[i])
            matrix[i][j] += diff
            result += diff * mtx[i][j]
            suppliers[j] -= diff
            buyers[i] -= diff

            if suppliers[j] == 0:
                j += 1

    return matrix, result


def min_cost(mtx: List[List[float]],
             suppliers: List[float],
             buyers: List[float]) -> Tuple[List[List[float]], float]:
    """Метод минимальной стоимости"""
    matrix = [[0.0 for _ in range(len(mtx[0]))] for _ in range(len(mtx))]
    result = 0.0
    costs: Dict[float, List[Tuple[int, int]]] = {}

    # Создаем словарь стоимостей
    for i in range(len(mtx)):
        for j in range(len(mtx[i])):
            if mtx[i][j] not in costs:
                costs[mtx[i][j]] = []
            costs[mtx[i][j]].append((j, i))

    # Сортируем по возрастанию стоимости
    sorted_costs = sorted(costs.keys())

    for cost in sorted_costs:
        for j, i in costs[cost]:
            if suppliers[j] > 0 and buyers[i] > 0:
                diff = min(suppliers[j], buyers[i])
                matrix[i][j] += diff
                result += diff * mtx[i][j]
                suppliers[j] -= diff
                buyers[i] -= diff

    return matrix, result


def contains(x: int, y: int, arr: List[Tuple[int, int]]) -> bool: \
   return any(v[0] == x and v[1] == y for v in arr)


def dfs(x: int, y: int, path: List[Tuple[int, int]],
        mtx: List[List[float]], horizontal: bool, cycle: List[Tuple[int, int]]) -> bool:
    """Поиск в глубину для нахождения цикла"""
    if not horizontal:
        for i in range(len(mtx)):
            if mtx[i][x] == 0 or contains(x, i, path):
                continue

            if len(path) > 2 and i == path[0][1] and len(path) % 2 != 0:
                cycle[:] = path + [(x, i)]
                return True

            if dfs(x, i, path + [(x, i)], mtx, not horizontal, cycle):
                return True
    else:
        for i in range(len(mtx[0])):
            if mtx[y][i] == 0 or contains(i, y, path):
                continue

            if len(path) > 2 and i == path[0][0] and len(path) % 2 != 0:
                cycle[:] = path + [(i, y)]
                return True

            if dfs(i, y, path + [(i, y)], mtx, not horizontal, cycle):
                return True
    return False


def find_cycle(points: List[Tuple[int, int]], mtx: List[List[float]]) -> List[Tuple[int, int]]:
    """Находит цикл в матрице"""
    cycle = []
    for v in points:
        if dfs(v[0], v[1], [v], mtx, False, cycle):
            return cycle
        if dfs(v[0], v[1], [v], mtx, True, cycle):
            return cycle
    return []


def calc_potentials(costs: List[List[float]],
                    plan: List[List[float]],
                    len_u: int, len_v: int) -> Tuple[List[float], List[float]]:
    """Вычисляет потенциалы"""
    u = [-math.inf] * len_u
    v = [-math.inf] * len_v
    u[0] = 0
    changed = True

    while changed:
        changed = False
        for i in range(len(u)):
            for j in range(len(v)):
                if plan[i][j] > 0:
                    if u[i] != -math.inf and v[j] == -math.inf:
                        v[j] = costs[i][j] - u[i]
                        changed = True
                    elif v[j] != -math.inf and u[i] == -math.inf:
                        u[i] = costs[i][j] - v[j]
                        changed = True
    return u, v


def calc_deltas(mtx: List[List[float]],
                plan: List[List[float]],
                u: List[float], v: List[float]) -> List[Tuple[int, int]]:
    """Вычисляет дельты для небазисных клеток"""
    min_delta = float('inf')
    deltas = []

    for i in range(len(mtx)):
        for j in range(len(mtx[i])):
            if plan[i][j] == 0:
                delta = mtx[i][j] - (u[i] + v[j])
                if delta < min_delta:
                    min_delta = delta
                    deltas = [(j, i)]
                elif delta == min_delta:
                    deltas.append((j, i))

    return deltas if min_delta < 0 else []


def potentials_method(mtx: List[List[float]],
                      plan: List[List[float]]) -> List[List[float]]:
    """Метод потенциалов"""
    while True:
        u, v = calc_potentials(mtx, plan, len(mtx), len(mtx[0]))
        deltas = calc_deltas(mtx, plan, u, v)

        if not deltas:
            return plan

        cycle = find_cycle(deltas, plan)

        if not cycle:
            return plan

        # Находим минимальное значение в нечетных позициях цикла
        min_val = min(plan[y][x] for x, y in cycle[1::2])

        # Корректируем план
        for i, (x, y) in enumerate(cycle):
            if i % 2 == 0:
                plan[y][x] += min_val
            else:
                plan[y][x] -= min_val


# Пример использования
if __name__ == "__main__":
    mtx, suppliers, buyers = initialization()

    # Копируем исходные данные для каждого метода
    suppliers_nw = suppliers.copy()
    buyers_nw = buyers.copy()
    nw_plan, nw_cost = north_west_corner(mtx, suppliers_nw, buyers_nw)

    suppliers_mc = suppliers.copy()
    buyers_mc = buyers.copy()
    mc_plan, mc_cost = min_cost(mtx, suppliers_mc, buyers_mc)

    optimized_plan = potentials_method(mtx, [row.copy() for row in mc_plan])

    print("Северо-западный угол:")
    for row in nw_plan:
        print(row)
    print(f"Общая стоимость: {nw_cost}")

    print("\nМинимальная стоимость:")
    for row in mc_plan:
        print(row)
    print(f"Общая стоимость: {mc_cost}")

    print("\nОптимизированный план (метод потенциалов):")
    for row in optimized_plan:
        print(row)
    res = 0
    for i in range(len(optimized_plan)):
        for j in range(len(optimized_plan[i])):
            if optimized_plan[i][j]:
                res += optimized_plan[i][j] * mtx[i][j]
    print(res)