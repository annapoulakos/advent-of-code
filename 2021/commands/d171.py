import click
from modules import fileutils


def part_1(data):
    """Part 1"""
    ints = [int(x) for x in data]
    matches = []

    for i, v in enumerate(ints):
        t = i+1 if i<len(ints)-1 else 0
        if v == ints[t]: matches.append(v)

    print(sum(matches))

def part_2(data):
    """Part 2"""
    ints = [int(x) for x in data]
    mid = int(len(ints)/2)
    matches = []

    for i,v in enumerate(ints):
        t = (i+mid) % len(ints)
        if v == ints[t]: matches.append(v)

    print(sum(matches))

@click.command()
@click.argument('part', type=int)
def d171(part):
    """Day 171 commands"""
    data = fileutils.load_raw(171)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
