from collections import OrderedDict
from threading import RLock

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data = OrderedDict()
        self._lock = RLock()

    def get(self, key, default=None):
        with self._lock:
            if key not in self._data:
                return default
            value = self._data.pop(key)
            self._data[key] = value
            return value

    def put(self, key, value):
        with self._lock:
            self._data.pop(key, None)
            self._data[key] = value
            if len(self._data) > self.capacity:
                self._data.popitem(last=False)

class LFUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.values = {}
        self.freq = {}
        self.buckets = {}
        self.min_freq = 0
        self._lock = RLock()

    def get(self, key, default=None):
        with self._lock:
            if key not in self.values:
                return default
            self._touch(key)
            return self.values[key]

    def put(self, key, value):
        with self._lock:
            if key in self.values:
                self.values[key] = value
                self._touch(key)
                return
            if len(self.values) >= self.capacity:
                victim = next(iter(self.buckets[self.min_freq]))
                self.buckets[self.min_freq].remove(victim)
                del self.values[victim]
                del self.freq[victim]
            self.values[key] = value
            self.freq[key] = 1
            self.buckets.setdefault(1, set()).add(key)
            self.min_freq = 1

    def _touch(self, key):
        old = self.freq[key]
        self.buckets[old].remove(key)
        if not self.buckets[old] and old == self.min_freq:
            self.min_freq += 1
        new = old + 1
        self.freq[key] = new
        self.buckets.setdefault(new, set()).add(key)
