#!/usr/bin/env python3.7
import fileinput
from itertools import cycle, accumulate


def twice(changes_):
    seen = {}

    for a in accumulate(cycle(changes_)):
        if seen.get(a):
            return a

        seen.setdefault(a, 1)


if __name__ == '__main__':
    changes = [int(line.strip()) for line in fileinput.input()]
    print(f" I) {sum(changes)}")
    print(f"II) {twice(changes)}")
