"""
Natural Merge Sort (Linked List, iterative)

Purpose:
    Linked implementation of Natural Merge Sort to avoid the 2x array space
    overhead of classic Merge Sort. Detects natural ascending runs and iteratively
    merges adjacent runs until one remains.

Counting policy:
    - comparisons: key comparisons during merge and run detection
    - exchanges  : counts pointer relinks (each node appended/moved)

Why linked list?
    The lab emphasizes external sorting friendliness and space efficiency;
    using a singly-linked list enables merge by relinking nodes instead of copying arrays.
"""
from __future__ import annotations
from typing import Optional, List
from counters import Counters

class Node:
    __slots__ = ("val", "next")
    def __init__(self, v: int):
        self.val: int = v
        self.next: Optional[Node] = None  # Allow None or Node

def list_from_array(arr: List[int]) -> Optional[Node]:
    """Build singly-linked list from array; return head or None if empty."""
    head: Optional[Node] = None
    tail: Optional[Node] = None
    for x in arr:
        n = Node(x)
        if head is None:
            head = n
            tail = n
        else:
            assert tail is not None  # for type checker
            tail.next = n
            tail = n
    return head

def list_to_array(head: Optional[Node]) -> List[int]:
    """Convert linked list to Python list."""
    out: List[int] = []
    cur = head
    while cur is not None:
        out.append(cur.val)
        cur = cur.next
    return out

def _split_runs(head: Optional[Node], c: Counters) -> List[Node]:
    """Split into natural ascending runs, returning list of run heads."""
    runs: List[Node] = []
    cur = head
    while cur is not None:
        run_head = cur
        while cur.next is not None:
            c.comparisons += 1
            if cur.val <= cur.next.val:
                cur = cur.next
            else:
                break
        nxt = cur.next
        cur.next = None
        runs.append(run_head)
        cur = nxt
    return runs

def _merge_two(a: Optional[Node], b: Optional[Node], c: Counters) -> Optional[Node]:
    """Merge two sorted lists into one."""
    if a is None: return b
    if b is None: return a
    dummy = Node(0)
    tail: Node = dummy
    while a is not None and b is not None:
        c.comparisons += 1
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
        c.exchanges += 1
    while a is not None:
        tail.next = a
        a = a.next
        tail = tail.next
        c.exchanges += 1
    while b is not None:
        tail.next = b
        b = b.next
        tail = tail.next
        c.exchanges += 1
    return dummy.next

def natural_merge_sort_linked(head: Optional[Node], c: Counters) -> Optional[Node]:
    """Iteratively merge runs until one sorted list remains."""
    if head is None or head.next is None:
        return head
    while True:
        runs = _split_runs(head, c)
        if len(runs) <= 1:
            return runs[0] if runs else None
        merged_head: Optional[Node] = None
        merged_tail: Optional[Node] = None
        i = 0
        while i < len(runs):
            a = runs[i]
            b = runs[i+1] if i+1 < len(runs) else None
            merged = _merge_two(a, b, c) if b is not None else a
            if merged_head is None:
                merged_head = merged
                merged_tail = merged
                while merged_tail is not None and merged_tail.next is not None:
                    merged_tail = merged_tail.next
            else:
                assert merged_tail is not None
                merged_tail.next = merged
                while merged_tail.next is not None:
                    merged_tail = merged_tail.next
            i += 2
        head = merged_head
