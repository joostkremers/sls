from typing import List
import os


def chunk(lst: List, chunk_size: int):
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def prettify_path(path: str) -> str:
    return path.replace(os.path.sep, " › ")
