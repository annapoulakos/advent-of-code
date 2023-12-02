import click
from modules import fileutils


def part_1(data):
    """Part 1"""
    rows = []
    for line in data:
        line_data = [int(x) for x in line.split('\t')]
        rows.append(max(line_data) - min(line_data))

    print(sum(rows))



def part_2(data):
    """Part 2"""
    rows = []
    for line in data:
        line_data = [int(x) for x in line.split('\t')]
        for l in line_data:
            factors = [(False if x==l else l%x==0) for x in line_data]
            if any(factors):
                idx = factors.index(True)
                rows.append(l//line_data[idx])
                break



    print(sum(rows))

@click.command()
@click.argument('part', type=int)
def d172(part):
    """Day 172 commands"""
    data = fileutils.load_lines(172)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
