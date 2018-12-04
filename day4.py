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

    def sleep(self, start, end):
        for minute in range(start, end):
            self._minutes[minute] += 1

        self._total += end - start

    def favorite_minute(self):
        return None if not self._minutes else max(self._minutes, key=self._minutes.get)

    def attack_vector(self):
        return self.favorite_minute() * self._number

    def minutes_slept(self):
        return self._total

    def __lt__(self, other):
        return self.minutes_slept() < other.minutes_slept()


class Record:
    stack = []

    def __init__(self, string):
        date, action = re.match('\[(.+)\]\s(.+)', string).groups()
        self._minute = datetime.strptime(date, "%Y-%m-%d %H:%M").minute
        self._action = action

    def replay(self, guards):
        if "#" in self._action:
            id_ = int(re.search("#(\d+)", self._action).group(1))
            Record.stack = [guards.pick(id_)]
        elif "asleep" in self._action:
            Record.stack.append(self._minute)
        else:
            guard, start = Record.stack[0], Record.stack.pop()
            guard.sleep(start, self._minute)


class Log:
    def __init__(self, records):
        self._records = records

    def replay(self, guards):
        for record in self._records:
            record.replay(guards)

    @staticmethod
    def from_file(path):
        return Log([Record(line.strip()) for line in sorted(fileinput.input(path))])


class Guards(dict):
    def pick(self, number):
        return self.setdefault(number, Guard(number))

    def sleepiest(self):
        return sorted(self.values())[-1]


if __name__ == '__main__':
    guards_ = Guards()
    Log.from_file("inputs/day4.txt").replay(guards_)

    print(guards_.sleepiest().attack_vector())
