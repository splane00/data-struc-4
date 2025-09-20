"""
Deterministic RNG + Fisher–Yates shuffle (no external imports)

Purpose:
    Provide a tiny deterministic RNG (LCG) and in-place shuffle so we can
    generate randomized inputs without importing 'random'. This keeps runs reproducible.

Interface:
    LCG(seed).randint(lo, hi) -> inclusive integer
    fisher_yates_shuffle(arr, rng) -> shuffles arr in-place
"""

class LCG:
    """Simple 31-bit LCG for repeatable pseudo-random integers."""
    def __init__(self, seed: int):
        self.state = seed & 0x7FFFFFFF

    def next(self) -> int:
        # Parameters chosen to give reasonable distribution; deterministic by seed.
        self.state = (1103515245 * self.state + 12345) & 0x7FFFFFFF
        return self.state

    def randint(self, lo: int, hi: int) -> int:
        """Return integer in [lo, hi] inclusive."""
        r = self.next()
        span = hi - lo + 1
        return lo + (r % span)

def fisher_yates_shuffle(arr, rng: LCG) -> None:
    """In-place Fisher–Yates shuffle using provided LCG."""
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
