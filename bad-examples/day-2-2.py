import click
import utils
from heapq import nsmallest

@click.command()
def cli():
    data = utils.load('day-2.txt')
    sizes = []
    for line in data:
        l,w,h = [int(x) for x in line.strip('\n').split('x')]
        s1, s2 = nsmallest(2, [l,w,h])
        sizes.append((2*s1+2*s2) + (l*w*h))

    print(f'Total: {sum(sizes)}')


if __name__ == '__main__':
    cli()
