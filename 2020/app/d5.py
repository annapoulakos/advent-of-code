import click
from app import helpers


def load_data():
    lines = helpers.file_to_lines('inputs', '2020-12-05.txt')

    boarding_passes = [(l[:7], l[-3:]) for l in lines] # split into distinct sections
    boarding_passes = [(r.replace('F', '0').replace('B', '1'), s.replace('L', '0').replace('R', '1')) for (r,s) in boarding_passes]

    return boarding_passes



@click.group()
def d5(): pass

@d5.command()
def p1():
    """Day 5, Part 1
    Decode seats to find highest seat
    F == lower, B == upper, L == lower, R == upper
    """
    boarding_passes = load_data()

    seat_ids = [int(row, 2)*8 + int(seat, 2) for (row, seat) in boarding_passes]

    highest_seat_id = max(seat_ids)

    print(f'output: {highest_seat_id}')

@d5.command()
def p2():
    """Day 5, Part 2
    find your seat (seat ids +/- 1 will exist and you won't be in first or last row)
    """
    boarding_passes = load_data()
    seat_ids = sorted([int(row, 2) * 8 + int(seat, 2) for (row, seat) in boarding_passes])
    missing_seats = [x for x in range(seat_ids[0], seat_ids[-1]+1) if x not in seat_ids]

    for missing_seat in missing_seats:
        if missing_seat-1 in seat_ids and missing_seat+1 in seat_ids:
            break

    print(f'output: {missing_seat}')
