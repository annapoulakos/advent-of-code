import click, time
from modules import fileutils


def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE

    end = time.perf_counter()

    # OUTPUT HERE

    print(f'elapsed = {end-start:.4f}')


def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE

    end = time.perf_counter()

    # OUTPUT HERE

    print(f'elapsed = {end-start:.4f}')


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
