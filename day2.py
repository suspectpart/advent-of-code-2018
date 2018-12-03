#!/usr/bin/env python3.7
import difflib
import fileinput
import itertools
from collections import Counter


def check_sum(box_ids):
    """Advent of Code 2018, Day 2, Part I"""

    counts = [Counter(id_).values() for id_ in box_ids]
    twos = sum(2 in c for c in counts)
    threes = sum(3 in c for c in counts)

    return twos * threes


def prototype_fabric(box_ids):
    """Advent of Code 2018, Day 2, Part II"""

    for a, b in itertools.combinations(box_ids, 2):
        distance = len([_ for _ in difflib.ndiff(a, b) if _[0] != ' '])
        if distance != 2:
            continue

        blocks = difflib.SequenceMatcher(None, a, b).get_matching_blocks()
        return "".join([a[block.a:block.a + block.size] for block in blocks])


if __name__ == '__main__':
    data = [line.strip() for line in fileinput.input()]

    print(f" I) Boxes Checksum: {check_sum(data)}")  # 8118
    print(f"II) Prototype fabric in: {prototype_fabric(data)}")  # jbbenqtlaxhivmwyscjukztdp
