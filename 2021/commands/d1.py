import click
from modules import fileutils, utils

def counter(lst):
    return sum([(1 if v>lst[i] else 0) for i,v in enumerate(lst[1:])])


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
