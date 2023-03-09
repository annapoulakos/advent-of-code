import itertools
import pathlib
from typing import Tuple, Dict

with open(pathlib.Path().cwd() / 'day-08.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

convert_input = lambda lines: [tuple([int(y) for y in tuple(list(x))]) for x in lines]
matrix_rotate = lambda lines: list(zip(*lines))

def row_visibility(line):
    result = [False]*len(line)

    current = -1
    for i,ele in enumerate(line):
        if ele>current:
            current = ele
            result[i] = True

    current = -1
    for i,ele in reversed(list(enumerate(line))):
        if ele>current:
            current = ele
            result[i] = True

    return result

def grid_visibility(lines):
    rows = convert_input(lines)
    result = [row_visibility(row) for row in rows]
    col_result = [row_visibility(row) for row in matrix_rotate(rows)]
    col_result = matrix_rotate(col_result)

    for x,y in itertools.product(range(len(lines)), range(len(lines[0]))):
        result[x][y] = result[x][y] or col_result[x][y]

    return result

def get_visible_count(lines):
    grid = grid_visibility(lines)
    count = sum([sum([e for e in ele if e]) for ele in grid])
    return count

def get_cell_score(row, index):
    left, right = 0, 0

    for value in row[index+1:]:
        left += 1
        if value >= row[index]: break

    for value in row[:index][::-1]:
        right += 1
        if value >= row[index]: break

    return left * right

def get_scenic_scores(lines):
    rows = convert_input(lines)
    cols = matrix_rotate(rows)
    scores = []

    for x,y in itertools.product(range(len(lines)), range(len(lines[0]))):
        hor,ver = get_cell_score(rows[x],y), get_cell_score(cols[y],x)
        scores.append(hor*ver)

    return scores

if __name__ == '__main__':
    print(f'part one: {get_visible_count(lines)}')
    print(f'part two: {max(get_scenic_scores(lines))}')
