import click, time
from modules import fileutils
from collections import Counter

def calculate_cost_for_target(crabs, target):
    return sum([abs(x-target) for x in crabs])

def calculate_cost(crabs):
    count = len(crabs) // 10
    c = Counter(crabs)
    mc = c.most_common(count)

    best = None
    for t,_ in mc:
        new = calculate_cost_for_target(crabs, t)
        if best is None or new < best: best = new

    return best

def calculate_extra_cost_for_target(crabs, target):
    fn = lambda n: (n * (n+1)) // 2
    return sum([fn(abs(x-target)) for x in crabs])


def calculate_extra_cost(crabs):
    start = min(crabs)
    end = max(crabs)

    best = None
    for target in range(start, end):
        new = calculate_extra_cost_for_target(crabs, target)
        if best is None or new < best: best = new

    return best


def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    best = calculate_cost(data)

    end = time.perf_counter()

    print(f'{best=}')
    print(f'elapsed = {end-start:.4f}')


def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    best = calculate_extra_cost(data)

    end = time.perf_counter()

    print(f'{best=}')
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d7(test, part):
    """Day 7 commands"""
    data = fileutils.load_raw(7, test)
    data = [int(x) for x in data.split(',') if x]

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
