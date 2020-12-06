import click

@click.group()
def cli(): pass

from app.d1 import d1
cli.add_command(d1)

from app.d2 import d2
cli.add_command(d2)

from app.d3 import d3
cli.add_command(d3)

from app.d4 import d4
cli.add_command(d4)

from app.d5 import d5
cli.add_command(d5)

from app.d6 import d6
cli.add_command(d6)

if __name__ == '__main__':
    cli()
