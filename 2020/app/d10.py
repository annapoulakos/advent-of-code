import click
from app import helpers

def load_data():
    lines = helpers.file_to_lines('inputs', '2020-12-10.txt')

    lines = [0] + sorted([int(l) for l in lines])
    lines.append(lines[-1] + 3)

    return lines

@click.group()
def d10(): pass


@d10.command()
def p1():
    """Day 10, Part 1
    multiple number of 1-jolt diffs by 3-jolt diffs
    """
    adapters = load_data()
    print(adapters[0], adapters[-1])

    diffs = [adapters[i+1]-adapters[i] for i in range(0, len(adapters)-1)]

    ones = sum(1 for d in diffs if d == 1)
    tres = sum(1 for d in diffs if d == 3)

    print(f'ones, threes: {ones}, {tres}')
    print(f'output: {ones * tres}')

@d10.command()
def p2():
    """Day 10, Part 2
    find number of possible sets of adapters to use
    """
    import functools
    adapters = load_data()

    @functools.lru_cache(maxsize=None)
    def get_children(value):
        if value not in adapters: return 0
        if value == adapters[-1]: return 1

        return sum([get_children(value+x) for x in range(1,4)])

    paths = get_children(0)

    print(f'output: {paths}')
