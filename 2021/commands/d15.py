import time, math, itertools, functools

import click
from modules import fileutils
from collections import defaultdict


def log(**kw):
    if not kw: print('='*60)
    for k,v in kw.items(): print(f'{k} => {v}')

def build_map(lines):
    risk_map = {}
    for x in range(len(lines[0])):
        for y in range(len(lines)):
            risk_map[(x,y)] = int(lines[x][y])

    return risk_map, (x,y)




def calculate_cost_matrix(risk_map, max_size):
    cost_matrix = defaultdict(lambda: math.inf)

    cost_matrix[(0,0)] = 0

    for coord in itertools.product(range(max_size[0]+1), range(max_size[1]+1)):
        if coord == (0,0): continue

        x,y = coord
        best = min(
            cost_matrix[(x,y-1)],
            cost_matrix[(x-1,y)],
            cost_matrix[(x,y+1)],
            cost_matrix[(x+1,y)],
        )
        cost_matrix[coord] = risk_map[coord] + best

    return cost_matrix

def display(target_map, max_size):
    rows = []
    for x in range(max_size[0]+1):
        row = ''
        for y in range(max_size[1]+1):
            row = f'{row}\t{target_map[(x,y)]}'
        rows.append(row)

    for row in rows:
        print(row)

def part_1(risk_map, target_coords):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE
    cost_matrix = calculate_cost_matrix(risk_map, target_coords)
    # display(risk_map, target_coords)
    # log()
    # display(cost_matrix, target_coords)

    end = time.perf_counter()

    # OUTPUT HERE
    log(
        target_cost=cost_matrix[target_coords],
    )
    print(f'elapsed = {end-start:.4f}')


def part_2(risk_map, target_coords):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE

    end = time.perf_counter()

    # OUTPUT HERE

    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d15(test, part):
    """Day 15 commands"""
    print(f'AoC :: Day 15 :: Part {part} {":: (test)" if test else ""}')
    data = fileutils.load_lines(15, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    risk_map, target_coords = build_map(data)

    fn(risk_map, target_coords)
