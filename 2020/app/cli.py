import click
import pathlib
from importlib import import_module

@click.group()
def cli(): pass

path = pathlib.Path(__file__).parent
files = path.glob('d*.py')

for filepath in files:
    module = import_module(f'app.{filepath.stem}')
    klass = getattr(module, filepath.stem)
    cli.add_command(klass)


if __name__ == '__main__':
    cli()
