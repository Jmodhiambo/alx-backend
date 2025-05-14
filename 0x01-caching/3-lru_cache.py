#!/usr/bin/env python3
"""
This is class LRUCache that inherits from BaseCaching
"""

from typing import Any, Optional, List
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """Inherits from BaseCaching and implements LRU cache"""

    def __init__(self) -> None:
        """Initialize LRU cache"""
        super().__init__()
        self.usage_order: List[str] = []

    def put(self, key: Optional[str], item: Optional[Any]) -> None:
        """Add item to cache using LRU eviction policy"""
        if key is None or item is None:
            return

        # If key exists, remove so we can re-add it as most recently used
        if key in self.cache_data:
            self.usage_order.remove(key)

        self.cache_data[key] = item
        self.usage_order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Evict the least recently used item (first in list)
            lru_key = self.usage_order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

    def get(self, key: Optional[str]) -> Optional[Any]:
        """Get item by key and mark it as recently used"""
        if key is None or key not in self.cache_data:
            return None

        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]
