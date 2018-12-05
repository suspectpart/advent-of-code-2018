#!/usr/bin/env python3.7
import fileinput
import re
from collections import defaultdict


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
            (minute, action) = re.match('\[.+:(\d{2})\]\s(.+)', record).groups()

            if "#" in action:
                guard_id = int(re.findall("#(\d+)", action)[0])
            elif "asleep" in action:
                start = int(minute)
            else:
                statistics.pick(guard_id).sleep(start, int(minute))

        return statistics

    @staticmethod
    def from_file(path):
        return Log(line.strip() for line in sorted(fileinput.input(path)))


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
