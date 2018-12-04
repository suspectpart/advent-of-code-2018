#!/usr/bin/env python3.7
import fileinput
import re
from collections import defaultdict
from datetime import datetime


class Guard:
    def __init__(self, number):
        self._number = number
        self.felt_asleep = None
        self._minutes = defaultdict(int)
        self._total = 0

    def number(self):
        return self._number

    def sleep(self, time_):
        self.felt_asleep = time_

    def wake_up(self, time_):
        for minute in range(self.felt_asleep, time_):
            self._minutes[minute] += 1

        self._total += time_ - self.felt_asleep

    def slept(self):
        return self._total

    def favorite_minute(self):
        if not self._minutes:
            return None

        return max(self._minutes, key=self._minutes.get)

    def attack_vector(self):
        return self.favorite_minute() * self.number()

    def __lt__(self, other):
        return self.slept() < other.slept()

    def __repr__(self):
        return f"Guard<num: {self._number}, slept: {self.slept()}, fav: {self.favorite_minute()}>"


class Record:
    pattern = re.compile('\[(?P<date>.+)\]\s(?P<action>.+)')

    def __init__(self, string):
        date, action = Record.pattern.match(string).groups()

        self._date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        self._action = action

    def action(self):
        return self._action

    def date(self):
        return self._date

    def minute(self):
        return self._date.minute

    def guard(self):
        guard_num = re.match("^Guard #(?P<number>\d+)\sbegins shift", self.action())
        return int(guard_num.group(1)) if guard_num else None

    def __lt__(self, other):
        return self.date() < other.date()

    def __repr__(self):
        return f"Record<date: {self.date()}, action: {self.action()}>"


if __name__ == '__main__':
    records = sorted(Record(record.strip()) for record in fileinput.input("inputs/day4.txt"))

    guards = {}
    current = None

    for record in records:
        if record.guard():
            current = guards.setdefault(record.guard(), Guard(record.guard()))
        elif "asleep" in record.action():
            current.sleep(record.minute())
        else:
            current.wake_up(record.minute())

    sleeper = list(sorted(guards.values(), reverse=True))[0]
    print(sleeper.attack_vector())
