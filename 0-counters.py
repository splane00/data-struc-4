"""
Data Structures Lab 4 (Sorting) — Counters

Purpose:
    Lightweight counters shared by all algorithms to track:
    - comparisons: key-to-key comparisons
    - exchanges:   element swaps (arrays) or pointer relinks/moves (linked lists)

Notes:
    Keeping counters in a dedicated module improves cohesion and clarity.
"""

class Counters:
    """Mutable counters for comparisons and exchanges."""
    def __init__(self):
        self.comparisons = 0
        self.exchanges = 0

    def add(self, other: "Counters") -> None:
        """Accumulate another Counters object into this one."""
        self.comparisons += other.comparisons
        self.exchanges   += other.exchanges
