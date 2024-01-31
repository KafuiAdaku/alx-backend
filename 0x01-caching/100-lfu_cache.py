#!/usr/bin/env python3
"""LFUCache module"""
BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class implements Least Frequency Used caching algorithm"""
    def __init__(self):
        super().__init__()
        self.put_count = 0
        self.counts = {}  # {key: [freq, self.put_count]

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            self.put_count += 1
            if len(self.cache_data) < BaseCaching.MAX_ITEMS or \
                    key in self.cache_data:
                self.counts[key] = [self.counts.get(key, [0, 0])[0] + 1,
                                    self.put_count]
                self.cache_data[key] = item
            else:
                least_freq_key = \
                        min(self.counts, key=lambda k: self.counts[k][0])
                freq = self.counts[least_freq_key][0]
                least_freq_keys = \
                    [k for k, v in self.counts.items() if v[0] == freq]
                if len(least_freq_keys) > 1:
                    del_key = min(least_freq_keys,
                                  key=lambda k: self.counts[k][1])
                else:
                    del_key = least_freq_key
                del self.cache_data[del_key]
                del self.counts[del_key]
                print(f"DISCARD: {del_key}")

                self.cache_data[key] = item
                self.counts[key] = [1, self.put_count]

    def get(self, key):
        """Get an item by key"""
        if key is not None and key in self.cache_data:
            self.put_count += 1
            self.counts[key] = [self.counts.get(key)[0] + 1, self.put_count]
            return self.cache_data[key]
        return None
