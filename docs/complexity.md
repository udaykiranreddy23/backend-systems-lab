# Complexity Notes

| Component | Operation | Expected |
|---|---|---|
| LRU | get/put | O(1) average |
| LFU | get/put | O(1) average in this implementation |
| Bloom Filter | add/contains | O(k) |
| Consistent Hash Ring | lookup | O(log N) |
| Circuit Breaker | allow | O(1) |
| Priority Queue | submit | O(log N) |

Measure benchmark results locally; do not claim unmeasured numbers.
