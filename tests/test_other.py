from systems.probabilistic import BloomFilter
from systems.distributed import ConsistentHashRing, Node
from systems.resilience import CircuitBreaker, CircuitState, retry


def test_bloom():
    b = BloomFilter(100)
    b.add("hello")
    assert "hello" in b


def test_ring():
    r = ConsistentHashRing([Node("a"), Node("b")], replicas=10)
    assert r.get_node("user-1").name in {"a", "b"}


def test_circuit():
    c = CircuitBreaker(failure_threshold=2, recovery_timeout=100)
    c.failure()
    c.failure()
    assert c.state == CircuitState.OPEN
    assert not c.allow()


def test_retry_succeeds_immediately():
    calls = []

    def operation():
        calls.append(1)
        return "success"

    result = retry(operation, attempts=3, base_delay=0)

    assert result == "success"
    assert len(calls) == 1


def test_retry_succeeds_after_failures():
    calls = []

    def operation():
        calls.append(1)

        if len(calls) < 3:
            raise ValueError("temporary failure")

        return "success"

    result = retry(operation, attempts=3, base_delay=0)

    assert result == "success"
    assert len(calls) == 3


def test_retry_raises_after_max_attempts():
    calls = []

    def operation():
        calls.append(1)
        raise ValueError("permanent failure")

    try:
        retry(operation, attempts=3, base_delay=0)
        assert False, "retry should have raised"
    except ValueError as exc:
        assert str(exc) == "permanent failure"

    assert len(calls) == 3