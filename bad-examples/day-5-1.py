import click
import utils
import itertools

def is_nice(message):
    for banned in ['ab', 'cd', 'pq', 'xy']:
        if banned in message:
            return False

    vowels = sum([1 for e in message if e in 'aeiou'])
    if vowels < 3:
        return False

    return any(sum(1 for _ in x) > 1 for _, x in itertools.groupby(message))

@click.command()
@click.option('--test', '-t', default=None)
def cli(test):
    if test is not None:
        data = [test]
    else:
        data = utils.load('day-5.txt')

    nice_strings = 0
    for line in data:
        if is_nice(line):
            nice_strings += 1

    print(f'nice strings: {nice_strings}')

if __name__ == '__main__':
    cli()
