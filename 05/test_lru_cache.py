import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_lru_cache_get(self):
        cache = LRUCache()

        for i in range(10):
            cache.set(f"k{i}", f"val{i}")

        for i in range(10):
            self.assertEqual(f"val{i}", cache.get(f"k{i}"))

        # if key not in cache
        self.assertNotEqual("val10", cache.get("k10"))
        self.assertEqual(None, cache.get("k10"))

    def test_lru_cache_change_limit(self):
        cache = LRUCache(20)

        self.assertNotEqual(42, cache.limit)
        self.assertEqual(20, cache.limit)

    def test_lru_cache_set(self):
        cache = LRUCache(10)

        for i in range(10):
            cache.set(f"k{i}", f"val{i}")
        for i in range(10):
            self.assertEqual(f"val{i}", cache.get(f"k{i}"))

        # add node over the limit
        cache.set("k10", "val10")

        self.assertNotEqual("val0", cache.get("k0"))
        self.assertEqual(None, cache.get("k0"))
        for i in range(1, 11):
            self.assertEqual(f"val{i}", cache.get(f"k{i}"))

        # if key in cache
        cache.set("k10", "newval10")

        self.assertNotEqual("val10", cache.get("k10"))
        self.assertEqual("newval10", cache.get("k10"))

    def test_lru_cache_replace_to_head(self):
        cache = LRUCache(3)

        # if one node is head
        cache.set(0, "val0")
        self.assertEqual("val0", cache.get(0))

        # if tail is None
        cache.set(1, "val1")
        self.assertEqual("val1", cache.get(1))

        # if node is not head and tail
        cache.set(2, "val2")
        self.assertEqual("val1", cache.get(1))

        # if node is tail
        self.assertEqual("val0", cache.get(0))
