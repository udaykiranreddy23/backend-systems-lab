import hashlib
import math

class BloomFilter:
    def __init__(self, capacity: int, false_positive_rate: float = 0.01):
        if capacity <= 0 or not 0 < false_positive_rate < 1:
            raise ValueError("invalid Bloom filter parameters")
        self.size = math.ceil(-(capacity * math.log(false_positive_rate)) / (math.log(2) ** 2))
        self.hash_count = max(1, math.ceil((self.size / capacity) * math.log(2)))
        self.bits = bytearray((self.size + 7) // 8)

    def _indexes(self, value):
        digest = hashlib.sha256(str(value).encode()).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big")
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.size

    def add(self, value):
        for i in self._indexes(value):
            self.bits[i // 8] |= 1 << (i % 8)

    def __contains__(self, value):
        return all(self.bits[i // 8] & (1 << (i % 8)) for i in self._indexes(value))
