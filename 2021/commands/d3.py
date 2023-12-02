import click
from modules import fileutils, itertools


def part_1(data):
    """Part 1"""
    gamma, epsilon = '', ''

    for x in range(len(data[0])):
        bits = sum([int(d[x]) for d in data])
        gamma += '1' if bits>(len(data)/2) else '0'
        epsilon += '0' if bits>(len(data)/2) else '1'

    print(gamma, epsilon)

    print(int(gamma, 2) * int(epsilon, 2))

def get_value(lst, parity):
    parts = [x for x in lst]

    for x in range(len(lst[0])):
        print(parts)
        bits = sum(int(d[x]) for d in parts)
        print(f'bits: {bits}')

        if bits == (pl:=len(parts) / 2) or bits > pl:
            bit = parity
        else:
            bit = 1 if parity == 0 else 0

        print(f'bit: {bit}')


        parts = list(filter(lambda p: int(p[x]) == bit, parts))
        if len(parts) == 1:
            break

    return int(parts[0], 2)

def part_2(data):
    """Part 2"""

    partials = [x for x in data]
    o2 = get_value(partials, 1)
    co2 = get_value(partials, 0)


    print(o2, co2)
    print(o2 * co2)








@click.command()
@click.argument('part', type=int)
def d3(part):
    """Day 3 commands"""
    data = fileutils.load_lines(3)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
