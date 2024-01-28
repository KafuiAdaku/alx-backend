#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Args:
            index (int): The current index of the return page.
            That is, the index of the first item of in the current page

            page_size (int): Number of items/row displayed per page

        Returns:
            dict: A dictionary with the following key-value pairs:
                index, next_index, page_size, data (actual page of dataset)
        """
        index = 0 if index is None else index

        assert isinstance(index, int)
        assert index <= len(self.indexed_dataset())
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.indexed_dataset()
        data = []
        next_index = index + page_size

        for idx in range(index, next_index):
            if dataset.get(idx) is not None:
                data.append(dataset[idx])
            else:
                idx += 1
                next_index += 1

        return {
                "index": index,
                "next_index": next_index,
                "page_size": page_size,
                "data": data,
                }
