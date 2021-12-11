import click, time, itertools, json
from modules import fileutils



def parse_data(lines):
    return [[int(x) for x in l] for l in lines]

class OctoMap:
    def __init__(self, lines):
        self._internal = {}
        for p in itertools.product(range(len(lines)), range(len(lines[0]))):
            self._internal[p] = lines[p[0]][p[1]]

        self._count = len(lines) * len(lines[0])

    def neighbors(self,p:tuple):
        x,y = p[0],p[1]

        neighbors = []
        for p in itertools.product([-1,0,1], [-1,0,1]):
            if p == (0,0): continue
            tgt = (p[0]+x, p[1]+y)
            if tgt in self._internal and self._internal[tgt] <= 9:
                neighbors.append(tgt)

        return neighbors

    def _age(self):
        for k in self._internal:
            self._internal[k] += 1

    def run_generation(self, days=100, early_exit=False):
        flashes = 0
        first = None

        for day in range(days):
            self._age()
            pending = [k for k,v in self._internal.items() if v > 9]
            if len(pending) == 0: continue

            while len(pending):
                p = pending.pop()

                for n in self.neighbors(p):
                    self._internal[n] += 1
                    if self._internal[n] > 9:
                        pending.append(n)
            else:
                count = 0
                for k in self._internal:
                    if self._internal[k] > 9:
                        self._internal[k] = 0
                        flashes += 1
                        count += 1

                if first is None and count == self._count: first = day+1

            if early_exit and first is not None: break

        return flashes, first

    def __str__(self):
        return self._internal

    def __repr__(self): return f'{self._internal}'


def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE
    om = OctoMap(data)
    flashes,_ = om.run_generation(100)

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'{flashes=}')
    print(f'elapsed = {end-start:.4f}')


def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE
    om = OctoMap(data)
    _,day = om.run_generation(1000, early_exit=True)

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'{day=}')
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d11(test, part):
    """Day 11 commands"""
    print(f'AoC :: Day 11 :: Part {part} {":: (test)" if test else ""}')
    data = fileutils.load_lines(11, test)
    data = parse_data(data)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
