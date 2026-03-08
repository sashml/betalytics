import collections

from itertools import chain, combinations


def powerset(iterable, comb_total=None):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    if comb_total:
        return chain.from_iterable(combinations(s, r) for r in range(comb_total, len(s) + 1))
    else:
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def count_frequency(arr):
    return collections.Counter(arr)
