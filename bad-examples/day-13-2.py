import click
import utils
import itertools
import re
from collections import namedtuple

Rule = namedtuple('Rule', 'actor action value actee')
Node = namedtuple('Node', 'name')
Edge = namedtuple('Edge', 'pair weight')

import pathlib
base_path = pathlib.Path(__file__).parent / 'utils' / 'day-13.txt'

DATA = [
    'Alice would gain 54 happiness units by sitting next to Bob.',
    'Alice would lose 79 happiness units by sitting next to Carol.',
    'Alice would lose 2 happiness units by sitting next to David.',
    'Bob would gain 83 happiness units by sitting next to Alice.',
    'Bob would lose 7 happiness units by sitting next to Carol.',
    'Bob would lose 63 happiness units by sitting next to David.',
    'Carol would lose 62 happiness units by sitting next to Alice.',
    'Carol would gain 60 happiness units by sitting next to Bob.',
    'Carol would gain 55 happiness units by sitting next to David.',
    'David would gain 46 happiness units by sitting next to Alice.',
    'David would lose 7 happiness units by sitting next to Bob.',
    'David would gain 41 happiness units by sitting next to Carol.',
]

with open(base_path) as handle:
    DATA = handle.read().strip().split('\n')

PATTERN = r'(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).'



@click.command()
def cli():
    raw_data = []
    rules = []
    nodes = set()
    edges = {}
    for datum in DATA:
        matches = list(re.findall(PATTERN, datum))
        print(matches[0])
        raw_data.append(matches[0])
        rules.append(Rule(*matches[0]))

        actor, action, weight, actee = matches[0]
        weight = int(weight)

        node = Node(actor)

        nodes.add(node)
        weight = weight if action == 'gain' else -1 * weight

        edges[(actor,actee)] = weight


    names = [n.name for n in nodes]
    me = Node('Anna')
    for name in names:
        edges[(me.name, name)] = 0
        edges[(name, me.name)] = 0
    names.append(me.name)

    names.sort()

    print('--- RAW DATA ---')
    print(raw_data)

    print('--- RULES ---')
    print(len(rules))
    print(rules[0])

    print('--- NODES ---')
    print(nodes)

    print('--- EDGES ---')
    print(edges)

    print('--- NAMES ---')
    print(names)

    permutations = list(itertools.permutations(names))
    print('--- PERMUTATIONS ---')
    print(len(permutations))

    weights = {}
    for permutation in permutations:
        wts = 0
        for index, actor in enumerate(permutation):
            wts += edges[(actor, permutation[index - 1])]
            wts += edges[(permutation[index - 1], actor)]

        weights[permutation] = wts

    order = None
    best = -1 * float('inf')
    for k,v in weights.items():
        if v > best:
            best = v
            order = k

    print(f'best: {best}')
    print(f'order: {order}')

if __name__ == '__main__':
    cli()
