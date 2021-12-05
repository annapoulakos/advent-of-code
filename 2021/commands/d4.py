import click
from modules import fileutils
from modules import itertools as it
from typing import List


class Board:
    def __init__(self, board):
        self._rows = []
        for row in board:
            points = [int(x) for x in row.split(' ') if x]
            self._rows.append(points)

        self._cols = []
        for x in range(5):
            self._cols.append([r[x] for r in self._rows])

    def complete(self, targets):
        for row in self._rows:
            if all(elem in targets for elem in row): return 'ROW', row

        for col in self._cols:
            if all(elem in targets for elem in col): return 'COL', col

        return None, None

    def row(self, idx):
        return self._rows(idx)

    @property
    def rows(self):
        return self._rows

    @property
    def values(self):
        return [i for s in self._rows for i in s]

from collections import OrderedDict

def solve_boards(calls:List[int], boards:List[Board]):
    current = 4
    solved = OrderedDict()

    remaining = [b for b in boards]
    while current < len(calls):
        partial = calls[0:current]

        for board in remaining:
            state,target = board.complete(partial)

            if state is not None:
                solved[calls[current]] = board
                del remaining[remaining.index(board)]

        current += 1

    return solved

def part_1(calls, boards):
    """Part 1"""
    solved = solve_boards(calls, boards)
    first = next(iter(solved))

    print(f'first: {first}')
    print(f'board: {solved[first].values}')

    idx = calls.index(first)
    partial = calls[0:idx]

    print(f'idx: {idx}')
    print(f'calls: {calls}')
    print(f'partial: {partial}')

    unclaimed = [x for x in solved[first].values if x not in calls[0:calls.index(first)]]
    print(f'unclaimed: {unclaimed}')

    print(f'sum: {sum(unclaimed)}')
    print(f'end: {sum(unclaimed)*partial[-1]}')



def part_2(calls, boards):
    """Part 2"""
    solved = solve_boards(calls, boards)
    last = next(iter(reversed(solved)))

    print(f'{last=}')
    print(f'board: {solved[last].values}')

    idx = calls.index(last)
    partial = calls[0:idx]

    print(f'{idx=}')
    print(f'{calls=}')
    print(f'{partial=}')

    unclaimed = [x for x in solved[last].values if x not in calls[0:calls.index(last)]]
    print(f'{unclaimed=}')

    print(f'{sum(unclaimed)=}')
    print(f'{sum(unclaimed)*partial[-1]=}')

@click.command()
@click.argument('part', type=int)
def d4(part):
    """Day 4 commands"""
    data = fileutils.load_lines(4)

    # data = [
    #     '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
    #     '22 13 17 11  0',
    #     ' 8  2 23  4 24',
    #     '21  9 14 16  7',
    #     ' 6 10  3 18  5',
    #     ' 1 12 20 15 19',
    #     ' 3 15  0  2 22',
    #     ' 9 18 13 17  5',
    #     '19  8  7 25 23',
    #     '20 11 10 24  4',
    #     '14 21 16 12  6',
    #     '14 21 17 24  4',
    #     '10 16 15  9 19',
    #     '18  8 23 26 20',
    #     '22 11 13  6  5',
    #     ' 2  0 12  3  7',
    # ]

    calls = [int(x) for x in data[0].split(',')]
    chunks = list(it.chunk(data[1:], 5))
    boards = [Board(b) for b in chunks]

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(calls, boards)
