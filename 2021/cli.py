import click, pathlib
from importlib import import_module

@click.group()
def cli(): pass


target = pathlib.Path(__file__).parent / 'commands'
for filename in target.glob('*.py'):
    if filename.stem == '__init__': continue

    module = import_module(f'commands.{filename.stem}')
    cli.add_command(getattr(module, filename.stem))

if __name__ == '__main__':
    cli()
