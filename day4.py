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
        return max(self._minutes, key=self._minutes.get) if self._minutes else 0

    def highest_count(self):
        return max(self._minutes.values()) if self._minutes else 0

    def minutes_slept(self):
        return self._total

    def __lt__(self, other):
        return self.minutes_slept() < other.minutes_slept()

    def __repr__(self):
        return f"{self.favorite_minute() * self._number}"


class Record:
    stack = []

    def __init__(self, string):
        date, action = re.match('\[(.+)\]\s(.+)', string).groups()
        self._minute = datetime.strptime(date, "%Y-%m-%d %H:%M").minute
        self._action = action

    def replay(self, statistics):
        if "#" in self._action:
            id_ = int(re.search("#(\d+)", self._action).group(1))
            Record.stack = [statistics.pick(id_)]
        elif "asleep" in self._action:
            Record.stack.append(self._minute)
        else:
            guard, start = Record.stack[0], Record.stack.pop()
            guard.sleep(start, self._minute)


class Log:
    def __init__(self, records):
        self._records = records

    def replay(self):
        statistics = Statistics()
        for record in self._records:
            record.replay(statistics)

        return statistics

    @staticmethod
    def from_file(path):
        return Log([Record(line.strip()) for line in sorted(fileinput.input(path))])


class Statistics(dict):
    def pick(self, number):
        return self.setdefault(number, Guard(number))

    def sleepiest(self):
        return sorted(self.values())[-1]

    def highest_frequency(self):
        return sorted(self.values(), key=Guard.highest_count)[-1]


if __name__ == '__main__':
    stats = Log.from_file("inputs/day4.txt").replay()

    print(stats.sleepiest())
    print(stats.highest_frequency())
