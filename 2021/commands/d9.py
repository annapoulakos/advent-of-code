import click, time, functools
from modules import fileutils
from collections import defaultdict

class HeightMap:
    def __init__(self):
        self._internal = {}
        self._height = 0
        self._width = 0

    def from_raw(self, lines):
        for y,line in enumerate(lines):
            for x,c in enumerate(line):
                self.add(x,y,int(c))

    def add(self, x, y, h):
        self._internal[(x,y)] = h
        if x>self._width: self._width = x
        if y>self._height: self._height = y

    def is_lower(self, p:tuple):
        return all([self.get(n)>self.get(p) for n in self.get_neighbors(p)])

    def get(self, p:tuple):
        return self._internal[p]

    def __str__(self):
        return f'{str(self._internal)}'
    def __repr__(self):
        return f'{self}'

    @property
    def h(self):
        return self._height

    @property
    def w(self):
        return self._width

    @property
    def points(self):
        return list(self._internal.keys())

    def get_neighbors(self,p):
        x,y=p
        neighbors = [
            (x,y-1) if y>0 else None,
            (x,y+1) if y<self.h else None,
            (x-1,y) if x>0 else None,
            (x+1,y) if x<self.w else None,
        ]
        return [n for n in neighbors if n is not None]

    def get_basins(self):
        # TODO: Find all low points
        lowest = [p for p in self.points if self.is_lower(p)]

        # TODO: Find all basins
        basins = defaultdict(int)
        for lp in lowest:
            to_check = set(self.get_neighbors(lp))
            in_basin = set()
            checked = set()

            while len(to_check) > 0:
                check = next((x for x in to_check if x not in checked), None)
                if check is None:
                    break

                if self.get(check) < 9:
                    in_basin.add(check)
                    to_check.update(self.get_neighbors(check))

                to_check.remove(check)
                checked.add(check)

            basins[lp] = in_basin
        return basins

def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    hm = HeightMap()
    hm.from_raw(data)

    lowers = [hm.get(p) for p in hm.points if hm.is_lower(p)]

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'{sum(x+1 for x in lowers)=}')
    print(f'elapsed = {end-start:.4f}')


def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE
    hm = HeightMap()
    hm.from_raw(data)

    basins = hm.get_basins()
    sizes = [len(b) for b in basins.values()]
    top = sorted(sizes)[-3:]

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'{functools.reduce(lambda x,y:x*y,top)=}')
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d9(test, part):
    """Day 9 commands"""
    data = fileutils.load_lines(9, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
