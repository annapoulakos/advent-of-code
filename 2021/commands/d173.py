import click
from modules import fileutils
import functools, math


def part_1(data):
    """Part 1"""
    data = "12"

    data = int(data)

    sq = math.ceil(math.sqrt(data))
    if sq%2==0: sq += 1

    print(f'sq: {sq}')

    arm = sq - 1
    ring = sq // 2
    sv = (sq ** 2)
    print(f'arm: {arm}')
    print(f'ring: {ring}')
    print(f'sv: {sv}')

    while data < sv:
        sv -= arm

    sv += arm

    print(f'sv: {sv}')

    md = data - sv + (arm // 2)
    print(f'md: {md}')


def part_2(data):
    """Part 2"""


@click.command()
@click.argument('part', type=int)
def d173(part):
    """Day 173 commands"""
    data = fileutils.load_raw(173)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
