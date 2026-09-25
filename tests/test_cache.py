from systems.cache import LRUCache, LFUCache

def test_lru_eviction():
    c = LRUCache(2)
    c.put("a",1); c.put("b",2)
    assert c.get("a") == 1
    c.put("c",3)
    assert c.get("b") is None

def test_lfu_eviction():
    c = LFUCache(2)
    c.put("a",1); c.put("b",2)
    assert c.get("a") == 1
    c.put("c",3)
    assert c.get("b") is None
