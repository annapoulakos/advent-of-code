import click
from app import helpers
import re
from collections import defaultdict, namedtuple

def load_data():
    lines = helpers.file_to_lines('inputs', '2020-12-07.txt')

    definitions = defaultdict(dict)
    for line in lines:
        matches = re.match('(.*?) bags contain (.*)', line)

        if matches:
            container, contents = matches[1], matches[2]
            if 'no other bags' in contents:
                definitions[container] = {}
                continue

            pattern = '(\d+) (.*?) bag[s]*'
            regex = re.compile(pattern)
            for bag in contents.split(','):
                matches = regex.match(bag.strip())
                if matches:
                    definitions[container][matches[2]] = int(matches[1])

    return definitions



@click.group()
def d7(): pass

@d7.command()
def p1():
    """Day 7, Part 1
    how many bag colors can eventually hold a shiny gold bag?
    """
    definitions = load_data()

    current = ['shiny gold']
    bags = []
    while current:
        current = [bag for bag, contents in definitions.items() for target in current if target in contents]
        bags += current

    print(f'output: {len(set(bags))}')

@d7.command()
def p2():
    """Day 7, Part 2
    find how many bags need to go in your shiny gold bag
    """
    definitions = load_data()

    current = 'shiny gold'
    bags = []

    def get_quantity(bag):
        my_quantity = sum(definitions[bag].values())
        my_child_quantities = [definitions[bag][b] * get_quantity(b) for b in definitions[bag]]

        return my_quantity + sum(my_child_quantities)

    bags = get_quantity(current)

    print(f'output: {bags}')
