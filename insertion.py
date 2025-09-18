"""
Insertion Sort for subranges (no imports)
Author: <Your Name>

Purpose:
    Provide insertion_sort(arr, left, right, counters) used as a finishing step
    by Quicksort variants for small partitions (<=50 / <=100), to reduce overhead.

Counting:
    - comparisons: number of (arr[j] > key) comparisons
    - exchanges:   counts element moves (shifts + final placement)
"""

from counters import Counters

def insertion_sort(arr, left: int, right: int, c: Counters) -> None:
    """Stable in-place insertion sort on arr[left..right] inclusive."""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        # Shift larger elements to the right
        while j >= left:
            c.comparisons += 1  # compare arr[j] > key
            if arr[j] > key:
                arr[j + 1] = arr[j]
                c.exchanges += 1  # count shift as a move
                j -= 1
            else:
                break
        # Place key
        arr[j + 1] = key
        c.exchanges += 1
