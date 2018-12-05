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

    def id(self):
        return self.favorite_minute() * self._number

    def sleep(self, start, end):
        for minute in range(start, end):
            self._minutes[minute] += 1

        self._total += end - start

    def favorite_minute(self):
        return max(self._minutes, key=self._minutes.get) if self._minutes else 0

    def highest_frequency(self):
        return max(self._minutes.values()) if self._minutes else 0

    def minutes_slept(self):
        return self._total


class Log(list):
    def replay(self):
        statistics = Statistics()
        for record in self:
            record.replay(statistics)

        return statistics

    @staticmethod
    def from_file(path):
        return Log([Record(line.strip()) for line in sorted(fileinput.input(path))])


class Record:
    stack = []

    def __init__(self, string):
        (date, self._action) = re.match('\[(.+)\]\s(.+)', string).groups()
        self._minute = datetime.strptime(date, "%Y-%m-%d %H:%M").minute

    def replay(self, statistics):
        if "#" in self._action:
            guard_id = int(re.findall("#(\d+)", self._action)[0])
            Record.stack = [statistics.pick(guard_id)]
        elif "asleep" in self._action:
            Record.stack.append(self._minute)
        else:
            guard, start = Record.stack[0], Record.stack.pop()
            guard.sleep(start, self._minute)


class Statistics(dict):
    def pick(self, number):
        return self.setdefault(number, Guard(number))

    def sleepiest(self):
        return max(self.values(), key=Guard.minutes_slept)

    def highest_frequency(self):
        return max(self.values(), key=Guard.highest_frequency)


if __name__ == '__main__':
    stats = Log.from_file("inputs/day4.txt").replay()

    print(stats.sleepiest().id())
    print(stats.highest_frequency().id())
