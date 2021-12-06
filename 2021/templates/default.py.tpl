import click
from modules import fileutils


def part_1(data):
    """Part 1"""


def part_2(data):
    """Part 2"""


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d{VALUE}(test, part):
    """Day {VALUE} commands"""
    data = fileutils.load_raw({VALUE}, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
