from copy import deepcopy
from random import shuffle as r_shuffle
from typing import TypeVar


_T = TypeVar("_T")


def flatten(list_of_lists: list[list[_T]]) -> list[_T]:
    items = []
    for sub_list in list_of_lists:
        for item in sub_list:
            items.append(item)
    return items


def unique(items: list[_T]) -> list[_T]:
    return list(set(items))


def shuffle(items: list[_T]) -> list[_T]:
    shuffled = deepcopy(items)
    r_shuffle(shuffled)
    return shuffled
