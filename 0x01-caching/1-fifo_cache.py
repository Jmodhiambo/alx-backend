#!/usr/bin/env python3
"""
This is class FIFOCache that inherits from BaseCaching
"""

from typing import Any, Optional
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Inherits from BaseCaching."""
    def __init__(self) -> None:
        """Class init."""
        super().__init__()

    def put(self, key: Optional[str], item: Optional[Any]) -> None:
        """Adds items to the cache dictionary if key and item are not None."""
        if key is not None and item is not None:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                first_key = next(iter(self.cache_data))  # Gets the first key
                del self.cache_data[first_key]  # Removes the first item
                print(f"DISCARD: {first_key}")
            self.cache_data[key] = item

    def get(self, key: Optional[str]) -> Optional[Any]:
        """Gets the item from the dictionary using the key."""
        if key in self.cache_data:
            return self.cache_data[key]
        return None
