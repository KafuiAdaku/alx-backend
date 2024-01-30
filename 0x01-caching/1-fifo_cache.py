#!/usr/bin/env python3
"""FIFOCache module"""
BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache class implements a FIFO caching algorithm"""
    def __init__(self):
        """Initialse"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.MAX_ITEMS += 1

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                del_key = list(self.cache_data.keys())[0]
                del_item = self.cache_data.pop(del_key, None)
                print(f"DISCARD: {del_key}")

    def get(self, key):
        """ Get an item by key"""
        return self.cache_data.get(key)
