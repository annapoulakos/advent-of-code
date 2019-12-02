import click
import utils
from collections import defaultdict
from itertools import product

class S:
    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def loc(self):
        return (self.x, self.y)

def direction(char):
    if char == '^':
        return True, -1
    if char == '>':
        return False, 1
    if char == 'v':
        return False, 1
    if char == '<':
        return True, -1



@click.command()
@click.option('--test', '-t', default=None)
def cli(test):
    data = utils.read('day-3.txt')
    grid = defaultdict(lambda: 0)

    which = 'santa'
    santas = {
        'santa': S(),
        'robosanta': S(),
    }
    grid[santas[which].loc] = grid[santas[which].loc] + 1

    for char in data:
        if char == '^':
            santas[which].y -= 1
        elif char == 'v':
            santas[which].y += 1
        elif char == '<':
            santas[which].x -= 1
        elif char == '>':
            santas[which].x += 1

        grid[santas[which].loc] = grid[santas[which].loc] + 1

        which = 'robosanta' if which == 'santa' else 'santa'

    print(f'Houses? {len(grid.keys())}')


if __name__ == '__main__':
    cli()
