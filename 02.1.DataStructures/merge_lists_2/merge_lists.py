import heapq
from heapq import *
import typing as tp
import copy


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    h: heapq = []
    res = []
    for seq2 in seq:
        if seq2:
            heappush(h, copy.deepcopy(seq2))
    while len(h) > 0:
        arr = heappop(h)
        res.append(arr[0])
        arr.remove(arr[0])
        if arr:
            heappush(h, arr)
    return res
