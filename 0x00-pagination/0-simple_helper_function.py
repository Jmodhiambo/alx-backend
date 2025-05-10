#!/usr/bin/env python3
"""Simple helper function"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns a tuple with start and end indices"""

    start: int = page_size * (page - 1)
    end: int = page_size * page

    return (start, end)
