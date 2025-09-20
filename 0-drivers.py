"""
drivers.py
Course: 605.202 Data Structures
Assignment: Lab 4 — Sorting Algorithm Comparison

Purpose:
    This is the main driver for Lab 4. It can:
      1) Generate the required input datasets for testing.
      2) Execute all five sorting algorithms on all datasets, capturing
         counts of comparisons and exchanges, and writing the outputs
         to labeled text files.

Usage:
    Generate inputs:
        python drivers.py gen <output_input_dir>

    Run all sorts on all inputs:
        python drivers.py run <input_dir> <output_dir>

Notes:
    - This file is the only program entry point for the lab.
    - All file names are provided via the command line (no GUI/interactive).
    - For n=50 inputs, the output file includes:
         • Labeled header
         • Full echo of input
         • Full sorted output
    - For larger inputs, output file includes:
         • Labeled header
         • Concise echo of input (count, sum, xor, head/tail)
         • No sorted output (per lab instructions)
    - Errors in reading input (blank lines, non-integers) are logged to
      separate files in the output directory.

Dependencies:
    - counters.py
    - quicksort.py
    - insertion.py
    - natural_merge.py
    - io_utils.py
"""

import sys
from typing import Optional

from counters import Counters
from quicksort import quicksort_variant
from natural_merge import list_from_array, list_to_array, natural_merge_sort_linked, Node
from io_utils import read_ints, write_lines, generate_inputs_for_sizes, echo_block_for_large_input

# Lab-required sizes and orders
SIZES = [50, 1000, 2000, 5000, 10000]
ORDERS = ["asc", "desc", "rand"]


def check_sorted(arr: list[int]) -> bool:
    """
    Verify that arr is sorted in non-decreasing order.
    Returns True if sorted, False otherwise.
    """
    for i in range(1, len(arr)):
        if arr[i - 1] > arr[i]:
            return False
    return True


def lines_for_header(algorithm_label: str, input_label: str,
                     comparisons: int, exchanges: int) -> list[str]:
    """
    Create a standardized header for each output file.

    Parameters:
        algorithm_label: Name of the sorting algorithm variant.
        input_label: Name of the input file processed.
        comparisons: Total key comparisons counted.
        exchanges: Total exchanges/moves counted.

    Returns:
        A list of strings representing the header lines.
    """
    return [
        "==== DATA STRUCTURES LAB 4: SORT OUTPUT ====",
        f"ALGORITHM: {algorithm_label}",
        f"INPUT FILE: {input_label}",
        f"comparisons={comparisons}",
        f"exchanges={exchanges}",
        "============================================"
    ]


def run_on_array(arr: list[int], variant_key: str) -> tuple[list[int], Counters]:
    """
    Run a quicksort variant on a copy of arr.

    Parameters:
        arr: The array to be sorted (original will not be modified).
        variant_key: The key identifying which quicksort variant to run.

    Returns:
        (sorted_list, counters) where sorted_list is the sorted copy
        and counters is the Counters object with statistics.
    """
    c = Counters()
    data = arr[:]  # copy to preserve original
    quicksort_variant(data, variant_key, c)
    return data, c


def run_natural_merge(arr: list[int]) -> tuple[list[int], Counters]:
    """
    Run the linked-list Natural Merge Sort on a copy of arr.

    Parameters:
        arr: The array to be sorted (original will not be modified).

    Returns:
        (sorted_list, counters) where sorted_list is the sorted copy
        and counters is the Counters object with statistics.
    """
    c = Counters()
    head: Optional[Node] = list_from_array(arr)
    head = natural_merge_sort_linked(head, c)
    sorted_arr = list_to_array(head)
    return sorted_arr, c


def write_output_for_small(output_dir: str, label: str, header_lines: list[str],
                           raw_input: list[int], sorted_output: list[int]) -> None:
    """
    For small inputs (n=50), write full echo of input and sorted output.
    """
    lines = []
    lines.extend(header_lines)
    lines.append("---- INPUT (full echo) ----")
    lines.extend(str(v) for v in raw_input)
    lines.append("---- SORTED DATA ----")
    lines.extend(str(v) for v in sorted_output)
    ok = write_lines(f"{output_dir}/{label}", lines)
    if not ok:
        print(f"WARNING: could not write {label}")


def write_output_for_large(output_dir: str, label: str, header_lines: list[str],
                           raw_input: list[int]) -> None:
    """
    For large inputs (n > 50), write header and concise echo of input.
    """
    lines = []
    lines.extend(header_lines)
    lines.append("---- INPUT (concise echo) ----")
    lines.extend(echo_block_for_large_input(raw_input, max_show=20))
    ok = write_lines(f"{output_dir}/{label}", lines)
    if not ok:
        print(f"WARNING: could not write {label}")


def run_all(input_dir: str, output_dir: str) -> None:
    """
    Run all five sorts on all inputs and save results to output_dir.

    Parameters:
        input_dir: Directory containing the input text files.
        output_dir: Directory where output files will be saved.
    """
    variants = [
        ("qsort_first_stop12",   "first_stop12"),
        ("qsort_first_ins100",   "first_ins100"),
        ("qsort_first_ins50",    "first_ins50"),
        ("qsort_median3_stop12", "median3_stop12"),
        ("nat_merge_linked",     "natmerge")
    ]

    for n in SIZES:
        for order in ORDERS:
            in_path = f"{input_dir}/{n}_{order}.txt"
            raw, errs = read_ints(in_path)
            label_base = f"{n}_{order}"

            if raw is None:
                print(f"ERROR: cannot open input {in_path}")
                continue

            if errs:
                # Write error log for this file
                err_lines = [f"Errors while reading {in_path}:"]
                for lineno, msg in errs:
                    err_lines.append(f"line {lineno}: {msg}")
                write_lines(f"{output_dir}/READ_ERRORS_{label_base}.txt", err_lines)

            for vname, vkey in variants:
                if vkey == "natmerge":
                    sorted_arr, c = run_natural_merge(raw)
                else:
                    sorted_arr, c = run_on_array(raw, vkey)

                # Verify sortedness
                if not check_sorted(sorted_arr):
                    write_lines(f"{output_dir}/ERROR_sort_{vname}_{label_base}.txt",
                                [f"Sort did not produce non-decreasing output for {in_path}."])

                # Build header
                header = lines_for_header(vname, f"{n}_{order}.txt",
                                          c.comparisons, c.exchanges)

                # Save output per size rule
                out_name = f"{vname}_{label_base}.txt"
                if n == 50:
                    write_output_for_small(output_dir, out_name, header, raw, sorted_arr)
                else:
                    write_output_for_large(output_dir, out_name, header, raw)


def generate_inputs(out_input_dir: str) -> None:
    """Generate required input files into out_input_dir."""
    generate_inputs_for_sizes(SIZES, out_input_dir)


def main(argv: list[str]) -> None:
    """
    Main entry point for the driver.

    CLI:
        driver.py gen <out_input_dir>
        driver.py run <input_dir> <output_dir>
    """
    if len(argv) < 2:
        print("USAGE:")
        print("  python drivers.py gen <out_input_dir>")
        print("  python drivers.py run <input_dir> <output_dir>")
        return

    mode = argv[1]
    if mode == "gen":
        if len(argv) != 3:
            print("USAGE: python drivers.py gen <out_input_dir>")
            return
        generate_inputs(argv[2])
        print(f"Generated input files in {argv[2]}")
    elif mode == "run":
        if len(argv) != 4:
            print("USAGE: python drivers.py run <input_dir> <output_dir>")
            return
        run_all(argv[2], argv[3])
        print(f"Wrote outputs to {argv[3]}")
    else:
        print("Unknown mode:", mode)
        print("USAGE:")
        print("  python drivers.py gen <out_input_dir>")
        print("  python drivers.py run <input_dir> <output_dir>")


if __name__ == "__main__":
    main(sys.argv)
