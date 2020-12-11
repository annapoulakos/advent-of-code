import click
from app import helpers
import itertools
from abc import ABC, abstractstaticmethod
from copy import deepcopy
import time

class Rule(ABC):
    @abstractstaticmethod
    def condition(seat): pass
    @abstractstaticmethod
    def action(neighbors, seat): pass

class EmptySeat(Rule):
    @staticmethod
    def condition(seat): return seat == 'L'
    @staticmethod
    def action(n, s): return '#' if n == 0 else s

class OccupiedSeat(Rule):
    @staticmethod
    def condition(seat): return seat == '#'
    @staticmethod
    def action(n, s): return 'L' if n >= 4 else s


def load_data():
    lines = helpers.file_to_lines('inputs', '2020-12-11.txt')

    # lines = [
    #     'L.LL.LL.LL',
    #     'LLLLLLL.LL',
    #     'L.L.L..L..',
    #     'LLLL.LL.LL',
    #     'L.LL.LL.LL',
    #     'L.LLLLL.LL',
    #     '..L.L.....',
    #     'LLLLLLLLLL',
    #     'L.LLLLLL.L',
    #     'L.LLLLL.LL',
    #     ]

    lines = [list(line) for line in lines]

    return lines


def count_seats(status):
    seats = [1 for row in status for col in row if col == '#']
    return sum(seats)

def get_neighbors(x, y, status):
    cells = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))

    neighbors = 0

    for tx,ty in cells:
        # Cull edge pieces (x < 0)
        if tx < 0 or ty < 0: continue
        if tx >= len(status) or ty >= len(status[0]): continue

        # Cull current location
        if tx == x and ty == y: continue

        if status[tx][ty] == '#': neighbors += 1

    return neighbors

@click.group()
def d11(): pass

@d11.command()
def p1():
    """Day 11, Part 1
    Determine how many seats are filled after following ruleset
    """
    seat_status = load_data()
    rows, cols = len(seat_status), len(seat_status[0])
    new_status = deepcopy(seat_status)

    cells = list(itertools.product(range(rows), range(cols)))

    start_time = time.perf_counter()
    while True:
        for x,y in cells:
            if seat_status[x][y] == '.': continue

            neighbors = get_neighbors(x,y, seat_status)
            rule = next((r for r in [EmptySeat, OccupiedSeat] if r.condition(seat_status[x][y])))
            new_status[x][y] = rule.action(neighbors, seat_status[x][y])

        if seat_status == new_status:
            end_time = time.perf_counter()
            print(f'time: {end_time-start_time:0.4f} seconds')
            print(f'output: {count_seats(seat_status)}')
            return

        seat_status = deepcopy(new_status)

def load_data_int():
    lines = load_data()

    cells = itertools.product(range(len(lines)), range(len(lines[0])))

    state = {}
    convert = lambda c: {'L': 0, '.': -1}.get(c, 1)

    for x,y in cells:
        state[(x,y)] = convert(lines[x][y])

    return state


class EmptySeatInt(Rule):
    @staticmethod
    def condition(seat): return seat == 0
    @staticmethod
    def action(neighbors, seat): return 1 if neighbors == 0 else seat

class OccupiedSeatInt(Rule):
    @staticmethod
    def condition(seat): return seat == 1
    @staticmethod
    def action(neighbors, seat): return 0 if neighbors >= 5 else seat

DELTAS = list(itertools.product(range(-1,2), range(-1,2)))
DELTAS.remove((0,0))

def find_neighbors_long(pos, state):
    neighborhood = []
    for dx,dy in DELTAS:
        target = -1
        x,y = pos
        while target < 0:
            x += dx
            y += dy
            target = state.get((x, y), 0)

        neighborhood.append(target)

    return sum(neighborhood)

def count_seats_int(state):
    values = [v for k,v in state.items() if v > 0]
    return sum(values)

def update_state(state):
    new = {}
    for pos, seat in state.items():
        if seat == -1: continue

        neighbors = find_neighbors_long(pos, state)
        rule = next((r for r in [EmptySeatInt, OccupiedSeatInt] if r.condition(seat)), None)
        if rule is not None:
            new[pos] = rule.action(neighbors, seat)

    return new

@d11.command()
def p2():
    """Day 11, Part 2
    Same as part 1, but with updated rules
    """
    state = load_data_int()
    new = deepcopy(state)

    start = time.perf_counter()

    while True:
        delta = update_state(state)
        new.update(delta)

        if new == state: break

        state = deepcopy(new)

    end = time.perf_counter()
    print(f'time: {end-start:0.4f}')
    print(f'final seat count: {count_seats_int(state)}')
