from time import perf_counter
from systems.cache import LRUCache

cache = LRUCache(10000)
start = perf_counter()
for i in range(100000):
    cache.put(i, i)
    cache.get(i)
elapsed = perf_counter() - start
print(f"Operations: 200000")
print(f"Elapsed: {elapsed:.6f}s")
print(f"Operations/sec: {200000 / elapsed:.2f}")
