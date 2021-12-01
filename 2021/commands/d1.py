import click
from modules import fileutils, utils

def counter(lst):
    cnt = 0
    c = lst[0]

    for v in lst[1:]:
        if v > c: cnt += 1
        c = v

    return cnt

def part_1(data):
    """Part 1"""
    print(counter(data))


def part_2(data):
    """Part 2"""
    windows = [sum(data[i:i+3]) for i in range(len(data) - 2)]
    print(counter(windows))


@click.command()
@click.argument('part', type=int)
def d1(part):
    """Day 1 commands"""
    data = fileutils.load_lines(1)
    data = utils.convert.to_int(data)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
