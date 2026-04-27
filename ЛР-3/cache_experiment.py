"""
Приложение к Лабораторной работе № 3
Пилотный эксперимент: оценка эффективности LRU-кэша

"""
import time, random, functools, tracemalloc

def expensive_hash(data: str) -> int:
    """Имитация тяжёлой операции: 500 итераций хэширования."""
    result = hash(data)
    for _ in range(500):
        result = hash(str(result) + data)
    return result

@functools.lru_cache(maxsize=256)
def cached_hash(data: str) -> int:
    return expensive_hash(data)

SIZES, UNIQUE_KEYS, REPEATS, SEED = [100,500,1000,2000,5000], 50, 3, 42
random.seed(SEED)

print(f"{'n':>6}  {'Без кэша (мс)':>14}  {'LRU-кэш (мс)':>13}  {'Ускорение':>10}")
print("-" * 50)
for n in SIZES:
    reqs = [f"block_{random.randint(0, UNIQUE_KEYS-1)}" for _ in range(n)]
    t_nc = sum((lambda: [time.perf_counter(),
        [expensive_hash(r) for r in reqs],
        time.perf_counter()])()[2] -
        (lambda: [time.perf_counter(),
        [expensive_hash(r) for r in reqs],
        time.perf_counter()])()[0]
        for _ in range(1)) * 1000

    # Простой замер
    t0 = time.perf_counter()
    for _ in range(REPEATS):
        [expensive_hash(r) for r in reqs]
    t_nc = (time.perf_counter()-t0)/REPEATS*1000

    cached_hash.cache_clear()
    t0 = time.perf_counter()
    for _ in range(REPEATS):
        cached_hash.cache_clear()
        [cached_hash(r) for r in reqs]
    t_lru = (time.perf_counter()-t0)/REPEATS*1000

    print(f"{n:>6}  {t_nc:>14.3f}  {t_lru:>13.3f}  {t_nc/t_lru:>9.1f}x")

cached_hash.cache_clear()
[cached_hash(f"block_{random.randint(0,UNIQUE_KEYS-1)}") for _ in range(1000)]
info = cached_hash.cache_info()
print(f"\nHit rate: {info.hits/(info.hits+info.misses)*100:.1f}%  |  {info}")
