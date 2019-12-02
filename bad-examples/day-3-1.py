import click
import utils
from collections import defaultdict


@click.command()
def cli():
    data = utils.read('day-3.txt')
    grid = defaultdict(lambda: 0)

    x = 0
    y = 0
    grid[(x,y)] = grid[(x,y)] + 1

    for char in data:
        if char == '^':
            y -= 1
        elif char == '>':
            x += 1
        elif char == 'v':
            y += 1
        elif char == '<':
            x -= 1
        grid[(x,y)] = grid[(x,y)] + 1

    print(f'Houses? {len(grid.keys())}')


if __name__ == '__main__':
    cli()
