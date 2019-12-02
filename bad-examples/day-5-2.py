import click
import utils

def is_nice(message):
    for index, letter in enumerate(message[1:]):
        i = index + 1
        pair = message[index]+message[i]
        if pair in message[i+1:]:
            break
    else:
        return False

    for index, letter in enumerate(message[2:]):
        token = message[index:index+3]
        if token[0] == token[2] and token[0] != token[1]:
            break
    else:
        return False

    return True


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
