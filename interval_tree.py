#!/usr/bin/env python3
"""interval_tree - Interval tree for overlapping interval queries."""
import sys

class Interval:
    def __init__(self, low, high, data=None):
        self.low = low
        self.high = high
        self.data = data
    def overlaps(self, other):
        return self.low <= other.high and other.low <= self.high
    def __repr__(self):
        return f"[{self.low},{self.high}]"

class ITNode:
    def __init__(self, interval):
        self.interval = interval
        self.max_high = interval.high
        self.left = None
        self.right = None

def insert(root, interval):
    if not root:
        return ITNode(interval)
    if interval.low < root.interval.low:
        root.left = insert(root.left, interval)
    else:
        root.right = insert(root.right, interval)
    if root.max_high < interval.high:
        root.max_high = interval.high
    return root

def query(root, interval, results=None):
    if results is None:
        results = []
    if not root:
        return results
    if root.interval.overlaps(interval):
        results.append(root.interval)
    if root.left and root.left.max_high >= interval.low:
        query(root.left, interval, results)
    if root.right and root.interval.low <= interval.high:
        query(root.right, interval, results)
    return results

def test():
    intervals = [(15, 20), (10, 30), (17, 19), (5, 20), (12, 15), (30, 40)]
    root = None
    for lo, hi in intervals:
        root = insert(root, Interval(lo, hi))
    r = query(root, Interval(14, 16))
    overlapping = [(i.low, i.high) for i in r]
    assert (15, 20) in overlapping
    assert (10, 30) in overlapping
    assert (5, 20) in overlapping
    assert (12, 15) in overlapping
    assert (30, 40) not in overlapping
    r2 = query(root, Interval(50, 60))
    assert len(r2) == 0
    print("OK: interval_tree")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: interval_tree.py test")
