#!/usr/bin/env python3
"""LIFOCache module"""
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache class implements a FIFO caching algorithm"""
    def __init__(self):
        """Initialise"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if key in self.cache_data:
                del self.cache_data[key]
                self.cache_data[key] = item
            else:
                self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # delete last item before the new key was set
                del_key = list(self.cache_data)[-2]
                self.cache_data.pop(del_key, None)
                print(f"DISCARD: {del_key}")

    def get(self, key):
        """ Get an item by key"""
        return self.cache_data.get(key)
