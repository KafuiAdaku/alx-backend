#!/usr/bin/env python3
"""MRUCache module"""
BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """MRUCache class implements Most Recently Used caching algorithm"""
    def __init__(self):
        super().__init__()
        self.put_count = 0
        self.counts = {}

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) < BaseCaching.MAX_ITEMS or \
                    key in self.cache_data:
                self.cache_data[key] = item
            else:
                del_key = max(self.counts, key=lambda k: self.counts[k])
                self.cache_data.pop(del_key, None)
                self.counts.pop(del_key, None)
                self.cache_data[key] = item
                print(f"DISCARD: {del_key}")

            self.put_count += 1
            self.counts[key] = self.put_count

    def get(self, key):
        """Get an item by key"""
        if key in self.cache_data:
            self.put_count += 1
            self.counts[key] = self.put_count
            return self.cache_data[key]
        return None
