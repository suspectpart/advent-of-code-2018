#!/usr/bin/env python3.7
import fileinput
import re
from collections import defaultdict
from itertools import product


class Fabric:
    def __init__(self):
        self._claimed = defaultdict(list)

    def claim(self, area):
        self._claimed[area].append(claim)

    def unique(self, claim_):
        return all(len(self._claimed[area]) == 1 for area in claim_.areas())

    def conflicts(self):
        return sum(map(lambda c: len(c) > 1, self._claimed.values()))


class Claim:
    pattern = re.compile('^#(?P<number>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)')

    def __init__(self, number, x, y, width, height):
        self.number = number
        self.x_range = range(x, x + width)
        self.y_range = range(y, y + height)

    @classmethod
    def from_string(cls, string):
        return cls(*tuple(map(int, Claim.pattern.match(string).groups())))

    def areas(self):
        return product(self.x_range, self.y_range)

    def id(self):
        return set(self.areas())

    def __call__(self, fabric_):
        for area in self.areas():
            fabric_.claim(area)

    def __repr__(self):
        return f"#{self.number}"


if __name__ == '__main__':
    """Advent of Code, Day 3, Part I"""
    claims = [Claim.from_string(line) for line in fileinput.input()]
    fabric = Fabric()

    for claim in claims:
        claim(fabric)

    print(f"I) {fabric.conflicts()}")
    print(f"II) {next(c for c in claims if fabric.unique(c))}")

