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


class Action:
    stack = []

    def __init__(self, string):
        date, action = re.match('\[(.+)\]\s(.+)', string).groups()
        self._minute = datetime.strptime(date, "%Y-%m-%d %H:%M").minute
        self._action = action

    def execute(self, guards):
        if "#" in self._action:
            id_ = int(re.search("#(\d+)", self._action).group(1))
            Action.stack = [guards.pick(id_)]
        elif "asleep" in self._action:
            Action.stack.append(self._minute)
        else:
            guard, start = Action.stack[0], Action.stack.pop()
            guard.sleep(start, self._minute)


class Guards(dict):
    def pick(self, number):
        return self.setdefault(number, Guard(number))

    def sleepiest(self):
        return sorted(self.values())[-1]


if __name__ == '__main__':
    actions = [Action(record.strip()) for record in sorted(fileinput.input("inputs/day4.txt"))]
    guards_ = Guards()

    for action_ in actions:
        action_.execute(guards_)

    print(guards_.sleepiest().attack_vector())
