import click
from app import helpers

def load_data():
    data = sorted([int(x) for x in helpers.file_to_lines('inputs', '2020-12-01.txt')])
    return data

@click.group()
def d1(): pass


@d1.command()
def p1():
    """Day 1, Part 1
    find two numbers that sum to 2020 and multiply them
    """
    data = load_data()

    first, last = data.pop(0), data.pop(-1)

    while True:
        if first + last == 2020: break
        if first + last > 2020:
            last = data.pop(-1)
        else:
            first = data.pop(0)

    output = first * last
    print(f'found: {first}, {last}')
    print(f'output: {output}')


@d1.command()
def p2():
    """Day 1, Part 2
    find three numbers that sum to 2020 and multiply them
    """
    import itertools

    data = load_data()
    a,b,c = next((x for x in itertools.combinations(data, 3) if sum(x) == 2020))

    output = a*b*c
    print(f'found: {a}, {b}, {c}')
    print(f'output: {output}')
