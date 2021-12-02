import click, parse
from modules import fileutils

class Location:
    def __init__(self):
        self.h = 0
        self.d = 0
        self.a = 0

    def _mv_f(self, distance):
        self.h += distance

    def _mv_u(self, distance):
        self.d -= distance

    def _mv_d(self, distance):
        self.d += distance


    def _mva_f(self, distance):
        self.h += distance
        self.d += self.a * distance

    def _mva_u(self, distance):
        self.a -= distance

    def _mva_d(self, distance):
        self.a += distance

    def move(self, command=None, distance=0):
        if command is None: return
        fn = {
            'forward': self._mv_f,
            'up': self._mv_u,
            'down': self._mv_d,
        }.get(command)
        fn(distance)

    def move_aim(self, command=None, distance=0):
        if command is None: return
        fn = {
            'forward': self._mva_f,
            'up': self._mva_u,
            'down': self._mva_d,
        }.get(command)
        fn(distance)


    def __str__(self):
        return f'({self.h}, {self.d}): {self.h*self.d}'

def part_1(data):
    """Part 1"""
    pattern = parse.compile('{} {:d}')
    loc = Location()

    for line in data:
        print(line)
        command, value = pattern.parse(line)
        loc.move(command, value)

    print(loc)



def part_2(data):
    """Part 2"""
    pattern = parse.compile('{} {:d}')
    loc = Location()

    for line in data:
        print(line)
        command, value = pattern.parse(line)
        loc.move_aim(command, value)

    print(loc)


@click.command()
@click.argument('part', type=int)
def d2(part):
    """Day 2 commands"""
    data = fileutils.load_lines(2)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
