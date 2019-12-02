import click
import utils

@click.command()
@click.option('--test', '-t', default=None)
def cli(test):
    if test is not None:
        data = test
    else:
        data = utils.load('day-5.txt')

if __name__ == '__main__':
    cli()
