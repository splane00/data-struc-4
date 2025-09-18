"""
Iterative Quicksort Variants (no recursion)

Implements four variants required by the lab:
  1) first_stop12     : first element as pivot; partitions of size <= 2 handled directly
  2) first_ins100     : first element as pivot; insertion sort when size <= 100
  3) first_ins50      : first element as pivot; insertion sort when size <= 50
  4) median3_stop12   : median-of-three pivot; partitions of size <= 2 handled directly

Partitioning:
  - Uses Hoare's partitioning scheme for fewer swaps.

Counting policy:
  - comparisons: all element-to-element comparisons
  - exchanges  : swaps of array elements
"""

from counters import Counters
from insertion import insertion_sort

def _tiny_sort_size_le_2(arr, l: int, r: int, c: Counters) -> None:
    """Sort partitions of size 2 directly, counting one comparison and possibly one swap."""
    if r - l <= 0:
        return
    c.comparisons += 1
    if arr[l] > arr[r]:
        arr[l], arr[r] = arr[r], arr[l]
        c.exchanges += 1

def _median_of_three(arr, l: int, r: int, c: Counters):
    """Place the median of (l, m, r) at arr[l] and return it as pivot."""
    m = (l + r) // 2
    # order l, m
    c.comparisons += 1
    if arr[m] < arr[l]:
        arr[m], arr[l] = arr[l], arr[m]; c.exchanges += 1
    # order m, r
    c.comparisons += 1
    if arr[r] < arr[m]:
        arr[r], arr[m] = arr[m], arr[r]; c.exchanges += 1
    # ensure l, m
    c.comparisons += 1
    if arr[m] < arr[l]:
        arr[m], arr[l] = arr[l], arr[m]; c.exchanges += 1
    # move median to l
    arr[l], arr[m] = arr[m], arr[l]; c.exchanges += 1
    return arr[l]

def _hoare_partition(arr, l: int, r: int, pivot, c: Counters) -> int:
    """Hoare partition around given pivot value; returns split index j with ranges [l..j], [j+1..r]."""
    i = l - 1
    j = r + 1
    while True:
        # move i right
        while True:
            i += 1
            c.comparisons += 1
            if not (arr[i] < pivot):
                break
        # move j left
        while True:
            j -= 1
            c.comparisons += 1
            if not (arr[j] > pivot):
                break
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
        c.exchanges += 1

def quicksort_variant(arr, variant: str, c: Counters) -> None:
    """
    Sort arr in-place using one of the four variants.
    variant ∈ {'first_stop12','first_ins100','first_ins50','median3_stop12'}
    """
    n = len(arr)
    if n <= 1:
        return
    stack = [(0, n - 1)]
    while stack:
        l, r = stack.pop()
        if l >= r:
            continue
        size = r - l + 1

        # Stop/switch rules
        if variant == 'first_stop12' or variant == 'median3_stop12':
            if size <= 2:
                _tiny_sort_size_le_2(arr, l, r, c)
                continue
        if variant == 'first_ins100' and size <= 100:
            insertion_sort(arr, l, r, c); continue
        if variant == 'first_ins50'  and size <= 50:
            insertion_sort(arr, l, r, c); continue

        # Choose pivot
        if variant.startswith('median3'):
            pivot = _median_of_three(arr, l, r, c)
        else:
            pivot = arr[l]

        p = _hoare_partition(arr, l, r, pivot, c)
        # Process subranges; order of push is arbitrary—push right then left
        stack.append((p + 1, r))
        stack.append((l, p))
