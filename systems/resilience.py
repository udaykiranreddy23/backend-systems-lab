import random
import time
from enum import Enum

class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.opened_at = None
        self.state = CircuitState.CLOSED

    def allow(self):
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN and time.monotonic() - self.opened_at >= self.recovery_timeout:
            self.state = CircuitState.HALF_OPEN
            return True
        return self.state == CircuitState.HALF_OPEN

    def success(self):
        self.failures = 0
        self.opened_at = None
        self.state = CircuitState.CLOSED

    def failure(self):
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = time.monotonic()

def retry(operation, attempts=3, base_delay=0.1, max_delay=2.0):
    for attempt in range(attempts):
        try:
            return operation()
        except Exception:
            if attempt == attempts - 1:
                raise
            delay = min(max_delay, base_delay * (2 ** attempt))
            time.sleep(delay * random.uniform(0.8, 1.2))
