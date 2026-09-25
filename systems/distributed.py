import hashlib
import bisect
from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    name: str

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=100):
        self.replicas = replicas
        self._ring = []
        self._owners = {}
        for node in nodes or []:
            self.add_node(node)

    def _hash(self, value):
        return int(hashlib.sha256(value.encode()).hexdigest(), 16)

    def add_node(self, node):
        for replica in range(self.replicas):
            key = self._hash(f"{node.name}:{replica}")
            self._owners[key] = node
            bisect.insort(self._ring, key)

    def remove_node(self, node):
        for replica in range(self.replicas):
            key = self._hash(f"{node.name}:{replica}")
            self._owners.pop(key, None)
            i = bisect.bisect_left(self._ring, key)
            if i < len(self._ring) and self._ring[i] == key:
                self._ring.pop(i)

    def get_node(self, key):
        if not self._ring:
            raise LookupError("ring is empty")
        point = self._hash(key)
        i = bisect.bisect_left(self._ring, point)
        if i == len(self._ring):
            i = 0
        return self._owners[self._ring[i]]
