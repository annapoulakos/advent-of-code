import click
from app import helpers

def load_data():
    return helpers.file_to_lines('inputs', '2020-12-02.txt')

def parse(line):
    rule, _, password = line.partition(':')
    quantity, _, letter = rule.partition(' ')
    mn, _, mx = quantity.partition('-')

    mn = int(mn.strip())
    mx = int(mx.strip())
    letter = letter.strip()
    password = password.strip()

    return password, letter, mn, mx

@click.group()
def d2(): pass


@d2.command()
def p1():
    """Day 2, Part 1
    count valid passwords from list

    rule: X-Y A: P (A must appear at least X times and at most Y times in P)
    """
    data = load_data()

    output = {
        'valid': [],
        'invalid': [],
    }

    for line in data:
        password, letter, mn, mx = parse(line)
        count = password.count(letter)

        key = 'valid' if count >= mn and count <= mx else 'invalid'

        output[key].append(line)

    print(f'output: {len(output["valid"])}')

@d2.command()
def p2():
    """Day 2, Part 2
    count valid passwords from list

    rule: X-Y A: P (A must appear exactly once at either X or Y)
    """
    data = load_data()

    output = {
        'valid': [],
        'invalid': [],
    }

    for line in data:
        password, letter, p1, p2 = parse(line)

        # convert to zero-indexed keys
        p1 = p1 - 1
        p2 = p2 - 1

        if password[p1] == letter and password[p2] != letter:
            key = 'valid'
        elif password[p1] != letter and password[p2] == letter:
            key = 'valid'
        else:
            key = 'invalid'

        output[key].append(line)

    print(f'output: {len(output["valid"])}')
