import itertools
import pathlib
import queue
from collections import deque
import re

with open(pathlib.Path().cwd() / 'day-11.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

MONKEYS = []
EXTRA_WORRY = False

def reset():
    global MONKEYS, EXTRA_WORRY
    MONKEYS = []
    EXTRA_WORRY = False

class Monkey:
    def __init__(self, items, operation, test, truthy, falsey):
        self.parse_items(items.strip())
        self.lhs, self.op, self.rhs = self.parse_operation(operation.strip())
        self.divisor = self.parse_test(test.strip())
        self.truthy, self.falsey = self.parse_conditionals(truthy, falsey)
        self.inspections = 0

    def parse_items(self, items):
        _,_,item_string = items.partition(':')
        values = [int(item.strip()) for item in item_string.split(',')]
        self.items = deque()
        for v in values: self.items.append(v)

    def parse_operation(self, operation):
        pattern = re.compile(r'Operation: new = (?P<lhs>old|\d+) (?P<op>\+|\*|\-|\/) (?P<rhs>old|\d+)')
        results = pattern.match(operation).groupdict()

        if not results: raise Exception('error handling pattern match in operation parser')

        lhs = 'old' if results['lhs'] == 'old' else int(results['lhs'])
        rhs = 'old' if results['rhs'] == 'old' else int(results['rhs'])
        op = results['op']

        return lhs, op, rhs

    def parse_test(self, test):
        _, _, divisor = test.rpartition(' ')
        return int(divisor)

    def parse_conditionals(self, truthy, falsey):
        _, _, t = truthy.rpartition(' ')
        _, _, f = falsey.rpartition(' ')
        return int(t), int(f)

    def worry_update(self, item):
        lhs = item if self.lhs == 'old' else self.lhs
        rhs = item if self.rhs == 'old' else self.rhs

        return {
            '*': lhs * rhs,
            '+': lhs + rhs,
        }.get(self.op)

    def is_divisible(self, val):
        return (val % self.divisor) == 0

    def throws_to(self, val):
        self.inspections += 1
        worry_level = self.worry_update(val)
        if EXTRA_WORRY == False:
            worry_level = worry_level // 3
        if self.is_divisible(worry_level):
            return worry_level, self.truthy
        else:
            return worry_level, self.falsey

    def catch(self, val):
        self.items.append(val)

    def tolist(self):
        return list(self.items)

def do_round():
    global MONKEYS

    for monkey in MONKEYS:
        while len(monkey.items):
            item = monkey.items.popleft()
            it, target = monkey.throws_to(item)
            MONKEYS[target].catch(it)

def parse_input(data):
    global MONKEYS
    groups = [list(sub) for ele,sub in itertools.groupby(data, key=bool) if ele]

    for group in groups:
        monkey = Monkey(*group[1:])
        MONKEYS.append(monkey)

    return MONKEYS

def get_sizes():
    global MONKEYS
    return [len(m.items) for m in MONKEYS]

if __name__ == '__main__':
    reset()
    parse_input(lines)
    EXTRA_WORRY = True

    for x in range(10000):
        if (x%100) == 0:
            print(f'round: {x=}')
            print(get_sizes())
        do_round()

    inspections = [monkey.inspections for monkey in MONKEYS]
    first,second = sorted(inspections)[::-1][:2]
    print(f'{first*second=}')
