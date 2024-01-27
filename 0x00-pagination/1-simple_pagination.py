#!/usr/bin/env python3
"""Module contaning class to paginate a database"""
import csv
import math
from typing import List


def index_range(page, page_size):
    """
    Args:
        page (int):
        page_size (int):

    Returns:
        tuple: Size 2. start index and end index
    """
    end_index = int(page) * int(page_size)
    start_index = end_index - int(page_size)

    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Args:
            page (int): page to be displayed
            page_size (int): number of rows displayed per page

        Returns;
            list: Rows of items of the specified page
        """
        assert type(page) == int and page > 0
        assert type(page_size) == int and page_size > 0

        page = index_range(page, page_size)

        csv_list = self.dataset()

        upper_bound = len(csv_list)

        if (not (page[0] >= 0 and page[0] <= upper_bound)) or \
                (page[1] > upper_bound):
            return []

        return [csv_list[idx] for idx in range(page[0], page[1] + 1)]
