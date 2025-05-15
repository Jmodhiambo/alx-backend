#!/usr/bin/env python3
""" LFUCache module """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class that inherits from BaseCaching"""

    def __init__(self):
        """Initialize LFUCache"""
        super().__init__()
        self.freq = {}
        self.usage_order = []

    def put(self, key, item):
        """Add item in cache with LFU policy"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.usage_order.remove(key)
            self.usage_order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the lowest frequency
                min_freq = min(self.freq.values())
                # Find keys with that frequency
                ks = [k for k in self.usage_order if self.freq[k] == min_freq]
                # Discard the least recently used among them
                lru_key = ks[0]
                del self.cache_data[lru_key]
                del self.freq[lru_key]
                self.usage_order.remove(lru_key)
                print(f"DISCARD: {lru_key}")

            self.cache_data[key] = item
            self.freq[key] = 1
            self.usage_order.append(key)

    def get(self, key):
        """Retrieve item from cache"""
        if key is None or key not in self.cache_data:
            return None

        self.freq[key] += 1
        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]
