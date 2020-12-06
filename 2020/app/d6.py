import click
from app import helpers


def load_data():
    lines = helpers.file_raw('inputs', '2020-12-06.txt')

    current = []
    groups_raw = []
    for line in lines:
        if line:
            current.append(line)
        else:
            groups_raw.append(current)
            current = []

    if current:
        groups_raw.append(current)

    return groups_raw


@click.group()
def d6(): pass

@d6.command()
def p1():
    """Day 6, Part 1
    sum questions from all groups
    """
    groups = load_data()

    group_sums = []
    for group in groups:
        group_sums.append(len(set([c for c in ''.join(group)])))

    print(f'output: {sum(group_sums)}')

@d6.command()
def p2():
    """Day 6, Part 2
    sum questions where everyone in group answered yes
    """
    groups = load_data()

    group_sums = []

    for group in groups:
        master_list = set([c for c in ''.join(group)])
        group_sum = 0
        for c in master_list:
            group_sum += 1 if all(c in g for g in group) else 0

        group_sums.append(group_sum)

    print(f'output: {sum(group_sums)}')
