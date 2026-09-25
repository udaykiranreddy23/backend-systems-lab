from systems.probabilistic import BloomFilter
from systems.distributed import ConsistentHashRing, Node
from systems.resilience import CircuitBreaker, CircuitState

def test_bloom():
    b = BloomFilter(100)
    b.add("hello")
    assert "hello" in b

def test_ring():
    r = ConsistentHashRing([Node("a"), Node("b")], replicas=10)
    assert r.get_node("user-1").name in {"a","b"}

def test_circuit():
    c = CircuitBreaker(failure_threshold=2, recovery_timeout=100)
    c.failure(); c.failure()
    assert c.state == CircuitState.OPEN
    assert not c.allow()
