import click
from modules import fileutils
from collections import defaultdict

def age(data, days):
    current = defaultdict(lambda: 0)

    for n in data:
        current[n] += 1

    for x in range(days):
        next_gen = defaultdict(lambda: 0)
        for f in current:
            ng = f - 1
            if ng < 0:
                next_gen[6] += current[f]
                next_gen[8] += current[f]
            else:
                next_gen[ng] += current[f]
        current = next_gen

    return current


def part_1(data):
    """Part 1"""
    current = age(data, 80)
    print(sum(current.values()))


def part_2(data):
    """Part 2"""
    current = age(data, 256)
    print(sum(current.values()))

@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d6(test, part):
    """Day 6 commands"""
    data = fileutils.load_raw(6, test)
    data = [int(x) for x in data.split(',') if x]

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
