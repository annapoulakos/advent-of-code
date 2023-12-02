import click, time, functools
from modules import fileutils
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def translate_x(point:Point, value):
    if point.x < value: return point
    return Point(value-(point.x-value), point.y)

def translate_y(point:Point, value):
    if point.y < value: return point
    return Point(point.x, value-(point.y-value))

def translate(point:Point, axis, value):
    fn = translate_y if axis == 'x' else translate_x
    return fn(point, value)

def log(**kw):
    if not kw: print('='*60)
    else:
        [print(f'{k} => {v}') for k,v in kw.items()]

def run_command(points:set, command:str) -> set:
    axis,value = command
    return {translate(point, axis, int(value)) for point in points}

def display(points):
    max_x = max([p.x for p in points])+1
    max_y = max([p.y for p in points])+1

    rows = [[' ' for _ in range(max_y)] for _ in range(max_x)]

    for point in points:
        rows[point.x][point.y] = '#'

    for row in rows:
        print(''.join(row))

def part_1(points, commands):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE
    points = run_command(points, commands[0])

    end = time.perf_counter()

    # OUTPUT HERE
    log(count=len(points))
    print(f'elapsed = {end-start:.4f}')


def part_2(points, commands):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE
    for command in commands:
        points = run_command(points, command)

    end = time.perf_counter()

    # OUTPUT HERE
    display(points)
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d13(test, part):
    """Day 13 commands"""
    print(f'AoC :: Day 13 :: Part {part} {":: (test)" if test else ""}')
    data = fileutils.load_lines(13, test)

    points, commands = [], []

    for line in data:
        if not line: continue
        if line.startswith('fold'):
            command = line.replace('fold along', '').strip().split('=')
            commands.append(command)
        else:
            x,y = line.split(',')
            points.append(Point(int(y), int(x)))

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(points, commands)
