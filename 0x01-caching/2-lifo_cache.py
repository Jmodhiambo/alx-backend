#!/usr/bin/env python3
"""
This is class LIFOCache that inherits from BaseCaching
"""

from typing import Any, Optional
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Inherits from BaseCaching."""
    def __init__(self) -> None:
        """Class init."""
        super().__init__()
        self.last_key: Optional[str] = None

    def put(self, key: Optional[str], item: Optional[Any]) -> None:
        """Adds items to the cache dictionary if key and item are not None."""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if self.last_key is not None:
                    del self.cache_data[self.last_key]
                    print(f"DISCARD: {self.last_key}")
            self.cache_data[key] = item
            self.last_key = key  # Tracks the last inserted key

    def get(self, key: Optional[str]) -> Optional[Any]:
        """Gets the item from the dictionary using the key."""
        if key in self.cache_data:
            return self.cache_data[key]
        return None
