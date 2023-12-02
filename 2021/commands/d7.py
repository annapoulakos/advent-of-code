import click, time, statistics
from modules import fileutils
from collections import Counter

def calculate_cost_for_target(crabs, target):
    return sum([abs(x-target) for x in crabs])

def calculate_extra_cost_for_target(crabs, target):
    fx = lambda n: (n * (n+1)) // 2
    return sum([fx(abs(x-target)) for x in crabs])

def get_best_cost(crabs, lst, fx):
    return min(fx(crabs, t) for t in lst)

def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    count = len(data) // 10
    c = Counter(data)
    lst = [t for t,_ in c.most_common(count)]

    best = get_best_cost(data, lst, calculate_cost_for_target)

    end = time.perf_counter()

    print(f'{best=}')
    print(f'elapsed = {end-start:.4f}')

def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    best = get_best_cost(data, range(min(data),max(data)), calculate_extra_cost_for_target)

    end = time.perf_counter()

    print(f'{best=}')
    print(f'elapsed = {end-start:.4f}')

def part_3(data):
    """Part 3"""
    mean = int(statistics.mean(data))
    r = [mean-1, mean, mean+1]

    best1 = get_best_cost(data, r, calculate_extra_cost_for_target)
    best2 = get_best_cost(data, range(min(data), max(data)), calculate_extra_cost_for_target)

    print(f'{best1=}')
    print(f'{best2=}')

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
        3: part_3,
    }.get(part)

    fn(data)
