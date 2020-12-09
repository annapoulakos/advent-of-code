import click
from app import helpers
import itertools

def load_data():
    lines = helpers.file_to_lines('inputs', '2020-12-09.txt')
    lines = [int(line) for line in lines]
    return lines

@click.group()
def d9(): pass


@d9.command()
def p1():
    """Day 9, Part 1
    Find number that doesn't match encryption
    """
    xmas_data = load_data()
    index = 25
    found = False

    while index < len(xmas_data):
        found = any([sum(x) == xmas_data[index] for x in itertools.combinations(xmas_data[index-25:index], 2)])
        if not found:
            break

        index += 1

    print(f'output: {xmas_data[index]}')

@d9.command()
def p2():
    """Day 9, Part 2
    Find the encryption weakness
    """
    xmas_data = load_data()
    target = 393911906
    end_index = xmas_data.index(target) - 1


    while end_index >= 0:
        if xmas_data[end_index] > target:
            end_index -= 1
            continue

        for start_index in range(end_index - 1, 0, -1):
            if sum(xmas_data[start_index:end_index]) > target:
                end_index -= 1
                break
            elif sum(chunk:=xmas_data[start_index:end_index]) == target:
                print(f'output: {min(chunk) + max(chunk)}')
                return
