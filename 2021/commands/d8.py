import click, time
from modules import fileutils
from collections import namedtuple

Parsed = namedtuple('Parsed', 'digits outputs')

def parse_digits(pattern):
    d, _, o = pattern.partition('|')

    digits = [x.strip() for x in d.split(' ') if x]
    outputs = [x.strip() for x in o.split(' ') if x]

    return Parsed(digits, outputs)

def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    parsed = [parse_digits(d) for d in data]

    mapping = {
        1: 2,
        4: 4,
        7: 3,
        8: 7,
    }

    total = 0
    for p in parsed:
        total += sum([1 for x in p.outputs if len(x) in mapping.values()])

    end = time.perf_counter()

    # OUTPUT HERE

    print(f'{total=}')
    print(f'elapsed = {end-start:.4f}')

def ssort(str):
    return ''.join(sorted(str))

def find(d, v):
    idx = list(d.values()).index(v)
    return list(d.keys())[idx]

def solve_5(d, sln):
    """solve for 2,3,5"""
    s, k = sorted(d), sorted(find(sln, 1))
    if all(e in s for e in k): return 3

    k2 = sorted(find(sln, 4))
    k2 = [x for x in k2 if x not in k]
    if all(e in s for e in k2): return 5

    return 2

def solve_6(d, sln):
    """solve for 0,6,9"""
    s, k = sorted(d), sorted(find(sln, 4))
    if all(e in s for e in k): return 9

    k2 = sorted(find(sln, 1))
    if all(e in s for e in k2): return 0

    return 6

def solve(digits):
    solution = {}

    for d in digits:
        rule = {
            2: lambda *x: 1,
            3: lambda *x: 7,
            4: lambda *x: 4,
            5: solve_5,
            6: solve_6,
            7: lambda *x: 8
        }.get(len(d))

        solution[ssort(d)] = rule(d, solution)

    return solution

def calc(nums):
    return sum([x*(10**i) for i,x in enumerate(reversed(nums))])


def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    parsed = [parse_digits(d) for d in data]

    numbers = []
    for line in parsed:
        solution = solve(sorted(line.digits, key=lambda k: len(k)))
        solved = [solution[ssort(x)] for x in line.outputs]
        numbers.append(calc(solved))

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'{sum(numbers)=}')
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d8(test, part):
    """Day 8 commands"""
    data = fileutils.load_lines(8, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
