"""
Приложение к Лабораторной работе № 2
Эмпирический эксперимент: сравнение алгоритмов сортировки

"""

import random
import time
import json


# ── Алгоритмы сортировки ──────────────────────────────────────────────────

def bubble_sort(arr):
    """Пузырьковая сортировка. Сложность: O(n²)."""
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def insertion_sort(arr):
    """Сортировка вставками. Сложность: O(n²), O(n) на почти упорядоченных."""
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    """Сортировка слиянием. Сложность: O(n log n)."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    L = merge_sort(arr[:mid])
    R = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            result.append(L[i]); i += 1
        else:
            result.append(R[j]); j += 1
    return result + L[i:] + R[j:]


def quick_sort(arr):
    """Быстрая сортировка. Сложность: O(n log n) в среднем."""
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x <  pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x >  pivot]
    return quick_sort(left) + mid + quick_sort(right)


def python_sort(arr):
    """Встроенная сортировка Python (Timsort). Сложность: O(n log n)."""
    return sorted(arr)


# ── Эксперимент ───────────────────────────────────────────────────────────

ALGORITHMS = {
    "Пузырьковая": bubble_sort,
    "Вставками":   insertion_sort,
    "Слиянием":    merge_sort,
    "Быстрая":     quick_sort,
    "Python sort": python_sort,
}

SIZES   = [100, 500, 1000, 2000, 5000]
REPEATS = 3
SEED    = 42


def run_experiment():
    """Измеряет среднее время каждого алгоритма на каждом размере массива."""
    random.seed(SEED)
    results = {name: {} for name in ALGORITHMS}

    for name, func in ALGORITHMS.items():
        for n in SIZES:
            times = []
            for _ in range(REPEATS):
                arr = [random.randint(0, 100_000) for _ in range(n)]
                t0 = time.perf_counter()
                func(arr)
                times.append((time.perf_counter() - t0) * 1000)
            results[name][n] = round(sum(times) / len(times), 3)

    return results


def print_table(results):
    """Печатает результаты в виде ASCII-таблицы."""
    header = f"{'Алгоритм':<18}" + "".join(f"  n={n:>5}" for n in SIZES)
    print("\n" + "=" * len(header))
    print("РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТА (среднее время в мс)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for name, data in results.items():
        row = f"{name:<18}" + "".join(f"  {data[n]:>7.3f}" for n in SIZES)
        print(row)
    print("=" * len(header) + "\n")


def plot_results(results):
    """Строит и сохраняет графики (требует matplotlib)."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        colors  = ["#e05c6e", "#f5a623", "#3dd68c", "#7c6dfa", "#4ec9e0"]
        markers = ["o", "s", "^", "D", "*"]

        for ax in axes:
            ax.set_facecolor("#18181c")
            ax.tick_params(colors="#b0b0c0")
            ax.grid(True, color="#2e2e38", linestyle="--", linewidth=0.6)
            for spine in ax.spines.values():
                spine.set_edgecolor("#2e2e38")

        # Граф 1: все алгоритмы, логарифмическая шкала
        ax1 = axes[0]
        for (name, data), color, marker in zip(results.items(), colors, markers):
            ax1.plot(SIZES, [data[n] for n in SIZES],
                     color=color, marker=marker, linewidth=2, markersize=7, label=name)
        ax1.set_yscale("log")
        ax1.set_xlabel("Размер массива (n)")
        ax1.set_ylabel("Время (мс, лог. шкала)")
        ax1.set_title("Рис. 1. Все алгоритмы (лог. шкала)")
        ax1.legend(fontsize=9)
        ax1.set_xticks(SIZES)

        # Граф 2: только быстрые, линейная шкала
        ax2 = axes[1]
        fast = ["Слиянием", "Быстрая", "Python sort"]
        for name, color, marker in zip(fast, colors[2:], markers[2:]):
            ax2.plot(SIZES, [results[name][n] for n in SIZES],
                     color=color, marker=marker, linewidth=2, markersize=7, label=name)
        ax2.set_xlabel("Размер массива (n)")
        ax2.set_ylabel("Время (мс)")
        ax2.set_title("Рис. 2. Быстрые алгоритмы (линейная шкала)")
        ax2.legend(fontsize=9)
        ax2.set_xticks(SIZES)

        fig.patch.set_facecolor("#0f0f11")
        fig.tight_layout()
        fig.savefig("sort_chart.png", dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print("График сохранён: sort_chart.png")
    except ImportError:
        print("matplotlib не установлен — график не построен.")


if __name__ == "__main__":
    print("Запуск эксперимента...")
    results = run_experiment()
    print_table(results)
    plot_results(results)
