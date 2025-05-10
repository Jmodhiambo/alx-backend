#!/usr/bin/env python3
"""Simple pagination"""

import csv
import math
from typing import List, Union, Dict, Optional

index_range = __import__('0-simple_helper_function').index_range


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
        """Returns the page content"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start, end = index_range(page, page_size)
        dataset = self.dataset()

        return dataset[start:end]

    def get_hyper(
        self, page: int = 1, page_size: int = 10
    ) -> Dict[str, Union[int, List[List], Optional[int]]]:
        """Hypermedia pagination"""
        dataset_page = self.get_page(page, page_size)
        full_dataset_items = len(self.dataset())

        total_pages = math.ceil(full_dataset_items / page_size)

        return {
             "page_size": len(dataset_page),
             "page": page,
             "data": dataset_page,
             "next_page": page + 1 if page < total_pages else None,
             "prev_page": page - 1 if page > 1 else None,
             "total_pages": total_pages,
        }
