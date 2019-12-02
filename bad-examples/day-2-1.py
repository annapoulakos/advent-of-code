import click
import utils

@click.command()
def cli():
    data = utils.load('day-2.txt')

    sizes = []
    for line in data:
        h,l,w = [int(x) for x in line.strip('\n').split('x')]
        hl = h*l
        lw = l*w
        wh = w*h
        extra = min(hl, lw, wh)
        sizes.append(2*(hl+lw+wh) + extra)

    print(f'total: {sum(sizes)}')
    print(sizes[-1])

if __name__ == '__main__':
    cli()
