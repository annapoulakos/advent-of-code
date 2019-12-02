import click
import hashlib

@click.command()
@click.option('--test', '-t', default=None)
def cli(test):
    data = 'iwrupvqb' if test is None else test

    current = 1
    while True:
        d = f'{data}{current}'
        hashed = hashlib.md5(d.encode()).hexdigest()

        if hashed.startswith('00000'):
            break

        current += 1

    print(f'found: {hashed}')
    print(f'after {current} iterations')

if __name__ == '__main__':
    cli()
