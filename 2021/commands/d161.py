import click, math
from modules import fileutils



class PointA():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction=0

    def turn(self, direction):
        mod = 1 if direction=='R' else -1
        self.direction = (self.direction + mod) % 4

    def move(self, instruction):
        direction,magnitude = instruction[0], int(instruction[1:])
        self.turn(direction)

        if self.direction == 0:
            self.y = self.y - magnitude
        elif self.direction == 1:
            self.x = self.x + magnitude
        elif self.direction == 2:
            self.y = self.y + magnitude
        else:
            self.x = self.x - magnitude

    @property
    def loc(self):
        return (self.x, self.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

def part_1(data):
    """Part 1"""
    instructions = [i.strip() for i in data.split(',')]

    p = PointA()
    [p.move(i) for i in instructions]

    print(abs(p.x) + abs(p.y))


def part_2(data):
    """Part 2"""
    instructions = [i.strip() for i in data.split(',')]

    p = PointA()
    visited = set()
    for i in instructions:
        p.move(i)
        if p.loc in visited:
            break
        visited.add(p.loc)

    print(abs(p.x) + abs(p.y))

@click.command()
@click.argument('part', type=int)
def d161(part):
    """Day 161 commands"""
    data = fileutils.load_raw(161)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
