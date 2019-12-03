import click
import pathlib
import requests
from importlib import import_module


base_path = pathlib.Path(__file__).parent

@click.group()
def cli():
    pass

@cli.command()
@click.argument('year', type=click.INT)
@click.argument('day', type=click.INT)
def pull(year, day):
    target = base_path / 'data' / f'{year}.{day}.txt'
    if not target.exists():
        print('File not found; downloading...')
        target.parent.mkdir(parents=True,exist_ok=True)
        cookies = {
            #'session': '53616c7465645f5f2bf2c8626b539a6661d7d2cf9517c8ab2df794177fafff317e01a24043884ae90e4a80dc4985a828',
            'session': '53616c7465645f5fb8454af400b9ae125ad914acebdff842140e2f5a309fcd44d13b9aa85c6d3468484197c494f1257e',
        }
        response = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies=cookies)
        response.raise_for_status()

        with target.open(mode='w+') as handle:
            handle.write(response.text)

    print('Completed')





@cli.command()
@click.argument('year', type=click.INT)
@click.argument('day', type=click.INT)
@click.argument('puzzle', type=click.INT)
def run(**kwargs):
    try:
        module = import_module(f'core.year_{kwargs["year"]}_executors')
    except:
        print(f'Cannot load module core.year_{kwargs["year"]}_executors')
        return

    executor = f'aoc_{kwargs["year"]}_{kwargs["day"]}_{kwargs["puzzle"]}'
    fn = getattr(module, executor, None)
    if not fn:
        print(f'Unable to find executor {executor}')
        return

    fn(**kwargs)


if __name__ == '__main__':
    cli()
