#!/usr/bin/env python3
"""Contains a helper function for pagination"""


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
