import click
from modules import fileutils


def part_1(data):
    """Part 1"""


def part_2(data):
    """Part 2"""


@click.command()
@click.argument('part', type=int)
def d{VALUE}(part):
    """Day {VALUE} commands"""
    data = fileutils.load_raw({VALUE})

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
