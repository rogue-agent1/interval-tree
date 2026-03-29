#!/usr/bin/env python3
"""interval_tree - Interval tree for overlap queries."""
import sys

class Interval:
    __slots__ = ['lo', 'hi', 'data']
    def __init__(self, lo, hi, data=None):
        self.lo = lo
        self.hi = hi
        self.data = data
    def overlaps(self, other):
        return self.lo <= other.hi and other.lo <= self.hi
    def contains(self, point):
        return self.lo <= point <= self.hi
    def __repr__(self):
        return f"[{self.lo}, {self.hi}]"

class ITNode:
    __slots__ = ['interval', 'max_hi', 'left', 'right']
    def __init__(self, interval):
        self.interval = interval
        self.max_hi = interval.hi
        self.left = None
        self.right = None

class IntervalTree:
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, lo, hi, data=None):
        iv = Interval(lo, hi, data)
        self.root = self._insert(self.root, iv)
        self.size += 1
    
    def _insert(self, node, iv):
        if not node:
            return ITNode(iv)
        if iv.lo < node.interval.lo:
            node.left = self._insert(node.left, iv)
        else:
            node.right = self._insert(node.right, iv)
        node.max_hi = max(node.max_hi, iv.hi)
        return node
    
    def query_point(self, point):
        results = []
        self._query_point(self.root, point, results)
        return results
    
    def _query_point(self, node, point, results):
        if not node:
            return
        if node.interval.contains(point):
            results.append(node.interval)
        if node.left and node.left.max_hi >= point:
            self._query_point(node.left, point, results)
        if node.right and node.interval.lo <= point:
            self._query_point(node.right, point, results)
    
    def query_overlap(self, lo, hi):
        query = Interval(lo, hi)
        results = []
        self._query_overlap(self.root, query, results)
        return results
    
    def _query_overlap(self, node, query, results):
        if not node:
            return
        if node.interval.overlaps(query):
            results.append(node.interval)
        if node.left and node.left.max_hi >= query.lo:
            self._query_overlap(node.left, query, results)
        if node.right and node.interval.lo <= query.hi:
            self._query_overlap(node.right, query, results)
    
    def all_intervals(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if not node:
            return
        self._inorder(node.left, result)
        result.append(node.interval)
        self._inorder(node.right, result)

def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_ivs = sorted(intervals, key=lambda iv: iv.lo)
    merged = [Interval(sorted_ivs[0].lo, sorted_ivs[0].hi)]
    for iv in sorted_ivs[1:]:
        if iv.lo <= merged[-1].hi:
            merged[-1].hi = max(merged[-1].hi, iv.hi)
        else:
            merged.append(Interval(iv.lo, iv.hi))
    return merged

def test():
    tree = IntervalTree()
    tree.insert(15, 20)
    tree.insert(10, 30)
    tree.insert(17, 19)
    tree.insert(5, 20)
    tree.insert(12, 15)
    tree.insert(30, 40)
    
    assert tree.size == 6
    
    # Point query
    r = tree.query_point(18)
    assert len(r) >= 2  # [15,20], [10,30], [17,19], [5,20]
    
    # Overlap query
    r = tree.query_overlap(25, 35)
    overlapping = [(iv.lo, iv.hi) for iv in r]
    assert (10, 30) in overlapping or (30, 40) in overlapping
    
    # No overlap
    r = tree.query_overlap(41, 50)
    assert len(r) == 0
    
    # Merge
    intervals = [Interval(1,3), Interval(2,6), Interval(8,10), Interval(15,18)]
    merged = merge_intervals(intervals)
    assert len(merged) == 3
    assert merged[0].lo == 1 and merged[0].hi == 6
    
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: interval_tree.py test")
