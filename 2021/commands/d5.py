from __future__ import annotations
import click, parse, json
from modules import fileutils
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Point:
    x:int
    y:int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Line:
    def __init__(self, p1:Point, p2:Point):
        self.p1 = p1
        self.p2 = p2

        self._points = []
        self._slope = None
        self._intercept = None

    @property
    def points(self):
        if not self._points:
            print(self)
            if self.is_horizontal:
                small,large = min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)
                self._points = [Point(x, self.p1.y) for x in range(small,large+1)]
            elif self.is_vertical:
                small,large = min(self.p1.y, self.p2.y), max(self.p1.y, self.p2.y)
                self._points = [Point(self.p1.x, y) for y in range(small, large+1)]
            else:
                small,large = min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)
                self._points = [Point(x, self.solve(x)) for x in range(small, large+1)]

        return self._points

    def solve(self,x):
        y = (self.slope) * x + self.y_intercept
        return int(y)

    @property
    def slope(self):
        if self._slope is None:
            if self.is_vertical:
                self._slope = float('NaN')
            else:
                self._slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

        return self._slope

    @property
    def y_intercept(self):
        if self._intercept is None:
            self._intercept = self.p1.y - (self.slope * self.p1.x)

        return self._intercept

    @property
    def is_horizontal(self):
        return self.p1.y == self.p2.y

    @property
    def is_vertical(self):
        return self.p1.x == self.p2.x

    def __str__(self):
        return f'{self.p1} -> {self.p2} :: y = {self.slope}x + {self.y_intercept}'

def parse_lines(lst):
    pattern = parse.compile('{x1:d},{y1:d} -> {x2:d},{y2:d}')
    lines = []
    for elem in lst:
        info = pattern.parse(elem)
        lines.append(Line(Point(x=info['x1'], y=info['y1']), Point(x=info['x2'], y=info['y2'])))

    return lines


def part_1(lines):
    """Part 1"""
    lines = parse_lines(lines)
    grid = defaultdict(lambda: 0)

    for line in lines:
        for point in line.points:
            if line.is_horizontal or line.is_vertical:
                grid[point] += 1

    danger = sum([1 for v in grid.values() if v>1])
    print(f'{danger=}')


def part_2(lines):
    """Part 2"""
    lines = parse_lines(lines)
    grid = defaultdict(lambda: 0)

    for line in lines:
        for point in line.points:
            grid[point] += 1

    danger = sum([1 for v in grid.values() if v>1])
    print(f'{danger=}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d5(test, part):
    """Day 5 commands"""
    lines = fileutils.load_lines(5, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(lines)
