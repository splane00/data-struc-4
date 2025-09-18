"""
I/O utilities: file read/write, input generation, validation, checksums

Guideline compliance:
  - Named files via command line (driver handles argv).
  - Error checking: missing files, non-integer lines, etc.
  - Output files echo input and include clearly labeled stats.

Note:
  We avoid imports except standard I/O via 'sys' in driver. No 'os' used here.
"""

from counters import Counters
from rng import LCG, fisher_yates_shuffle

def read_ints(path: str):
    """
    Read newline-separated integers from 'path'.
    Returns (values, errors) where errors is a list of (lineno, text).
    """
    vals = []
    errors = []
    try:
        f = open(path, "r")
    except:
        return None, [(-1, "ERROR: cannot open file")]
    lineno = 0
    for line in f:
        lineno += 1
        s = line.strip()
        if s == "":
            # treat blank line as error per guideline (no blanks)
            errors.append((lineno, "blank line"))
            continue
        neg = False
        if s[0] == '-':
            neg = True
            s2 = s[1:]
        else:
            s2 = s
        if s2.isdigit():
            vals.append(int(s))
        else:
            errors.append((lineno, "non-integer: " + s))
    f.close()
    return vals, errors

def write_lines(path: str, lines):
    """Write given strings to file; caller passes fully formatted lines."""
    try:
        f = open(path, "w")
        for item in lines:
            f.write(item)
            if not item.endswith("\n"):
                f.write("\n")
        f.close()
        return True
    except:
        return False

def checksum(values):
    """
    Simple checksum to echo large inputs concisely without massive files:
    Returns (count, sum, xor) for sanity verification across environments.
    """
    cnt = 0
    s = 0
    x = 0
    for v in values:
        cnt += 1
        s += v
        x ^= (v & 0xFFFFFFFF)
    return cnt, s, x

def generate_inputs_for_sizes(sizes, out_dir, seed_base=123456789):
    """
    Generate ascending, descending, and randomized inputs for required sizes.
    Files:
        {size}_asc.txt, {size}_desc.txt, {size}_rand.txt
    Numbers are 1..size (duplicates == 0% which is ≤ 1% requirement).
    """
    for n in sizes:
        asc = list(range(1, n+1))
        desc = list(range(n, 0, -1))
        rnd = list(range(1, n+1))
        rng = LCG(seed=seed_base + n)
        fisher_yates_shuffle(rnd, rng)
        _write_int_list(out_dir + f"/{n}_asc.txt", asc)
        _write_int_list(out_dir + f"/{n}_desc.txt", desc)
        _write_int_list(out_dir + f"/{n}_rand.txt", rnd)

def _write_int_list(path, nums):
    lines = [str(x) for x in nums]
    write_lines(path, lines)

def echo_block_for_large_input(values, max_show=20):
    """
    Build a concise echo for large inputs: first/last few + checksum.
    Satisfies 'echo input' guideline without dumping 10k numbers.
    """
    cnt, s, x = checksum(values)
    out = []
    out.append(f"INPUT_ECHO_COUNT={cnt}")
    out.append(f"INPUT_ECHO_SUM={s}")
    out.append(f"INPUT_ECHO_XOR={x}")
    if cnt <= 2 * max_show:
        out.append("INPUT_VALUES=" + " ".join(str(v) for v in values))
    else:
        head = " ".join(str(v) for v in values[:max_show])
        tail = " ".join(str(v) for v in values[-max_show:])
        out.append(f"INPUT_HEAD({max_show})=" + head)
        out.append(f"INPUT_TAIL({max_show})=" + tail)
    return out
