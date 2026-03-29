#!/usr/bin/env python3
"""Interval tree for range overlap queries."""
import sys

class Interval:
    def __init__(self, lo, hi, data=None):
        self.lo, self.hi, self.data = lo, hi, data
    def overlaps(self, other): return self.lo <= other.hi and other.lo <= self.hi
    def contains(self, point): return self.lo <= point <= self.hi
    def __repr__(self): return f"[{self.lo},{self.hi}]"

class ITNode:
    def __init__(self, interval):
        self.interval = interval; self.max_hi = interval.hi
        self.left = self.right = None

class IntervalTree:
    def __init__(self): self.root = None
    def insert(self, interval):
        self.root = self._insert(self.root, interval)
    def _insert(self, node, interval):
        if not node: return ITNode(interval)
        if interval.lo < node.interval.lo: node.left = self._insert(node.left, interval)
        else: node.right = self._insert(node.right, interval)
        node.max_hi = max(node.max_hi, interval.hi)
        return node
    def query_point(self, point):
        results = []; self._query_point(self.root, point, results); return results
    def _query_point(self, node, point, results):
        if not node: return
        if node.interval.contains(point): results.append(node.interval)
        if node.left and node.left.max_hi >= point:
            self._query_point(node.left, point, results)
        self._query_point(node.right, point, results)
    def query_overlap(self, interval):
        results = []; self._query_overlap(self.root, interval, results); return results
    def _query_overlap(self, node, interval, results):
        if not node: return
        if node.interval.overlaps(interval): results.append(node.interval)
        if node.left and node.left.max_hi >= interval.lo:
            self._query_overlap(node.left, interval, results)
        self._query_overlap(node.right, interval, results)
    def all_intervals(self):
        result = []; self._inorder(self.root, result); return result
    def _inorder(self, node, result):
        if not node: return
        self._inorder(node.left, result); result.append(node.interval); self._inorder(node.right, result)

def main():
    if len(sys.argv) < 2: print("Usage: interval_tree.py <demo|test>"); return
    if sys.argv[1] == "test":
        tree = IntervalTree()
        tree.insert(Interval(15, 20, "a")); tree.insert(Interval(10, 30, "b"))
        tree.insert(Interval(5, 12, "c")); tree.insert(Interval(25, 35, "d"))
        r = tree.query_point(11); assert len(r) == 2  # [10,30] and [5,12]
        r2 = tree.query_point(40); assert len(r2) == 0
        r3 = tree.query_overlap(Interval(14, 16))
        assert any(i.data == "a" for i in r3)  # [15,20] overlaps
        assert any(i.data == "b" for i in r3)  # [10,30] overlaps
        assert tree.all_intervals()
        # Edge: point at boundary
        r4 = tree.query_point(20)
        assert any(i.data == "a" for i in r4)
        print("All tests passed!")
    else:
        tree = IntervalTree()
        for lo, hi in [(1,5),(3,8),(6,10)]: tree.insert(Interval(lo, hi))
        print(f"Point 4: {tree.query_point(4)}")

if __name__ == "__main__": main()
