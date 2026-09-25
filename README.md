# Backend Systems Lab

Algorithms and backend primitives implemented with tests, complexity notes and benchmarks.

## Modules
- LRU Cache
- LFU Cache
- Bloom Filter
- Consistent Hash Ring
- Circuit Breaker
- Retry Policy
- Priority Task Queue

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python benchmarks/run_benchmarks.py
```

Every module is accompanied by tests and engineering notes. Benchmark numbers must be measured locally rather than copied into documentation.
