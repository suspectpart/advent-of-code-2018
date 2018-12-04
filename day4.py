#!/usr/bin/env python3.7
import fileinput
import re
from collections import defaultdict
from datetime import datetime


class Guard(object):
    def __init__(self, number):
        self._number = number
        self._minutes = defaultdict(int)
        self._total = 0

    def number(self):
        return self._number

    def sleep(self, start, end):
        for minute in range(start, end):
            self._minutes[minute] += 1

        self._total += end - start

    def slept(self):
        return self._total

    def favorite_minute(self):
        return None if not self._minutes else max(self._minutes, key=self._minutes.get)

    def attack_vector(self):
        return self.favorite_minute() * self.number()

    def __lt__(self, other):
        return self.slept() < other.slept()


class Record:
    pattern = re.compile('\[(.+)\]\s(.+)')

    def __init__(self, string):
        date, action = Record.pattern.match(string).groups()

        self._date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        self._action = action

    def action(self):
        return self._action

    def minute(self):
        return self._date.minute

    def begin_shift(self):
        guard_num = re.search("#(\d+)", self.action())
        return int(guard_num.group(1)) if guard_num else None


class Guards(dict):
    def pick(self, number):
        return self.setdefault(number, Guard(number))

    def sleepiest(self):
        return sorted(self.values())[-1]


if __name__ == '__main__':
    records = [Record(record.strip()) for record in sorted(fileinput.input("inputs/day4.txt"))]
    guards = Guards()
    current = None
    start_ = 0

    for record in records:
        if "#" in record.action():
            current = guards.pick(record.begin_shift())
        elif "asleep" in record.action():
            start_ = record.minute()
        else:
            current.sleep(start_, record.minute())

    print(guards.sleepiest().attack_vector())
