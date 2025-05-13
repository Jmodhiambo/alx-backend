#!/usr/bin/env python3
"""
This is a class BasicCache that inherits from BaseCaching
"""

from typing import Any, Optional
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Inherits from BaseCaching."""
    def __init__(self) -> None:
        """Class init."""
        super().__init__()

    def put(self, key: Optional[str], item: Optional[Any]) -> None:
        """Adds items to the cache dictionary if key and item are not None."""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key: Optional[str]) -> Optional[Any]:
        """Gets the item from the dictionary using the key."""
        if key in self.cache_data:
            return self.cache_data[key]
        return None
