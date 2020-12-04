import click
from app import helpers

def load_data():
    lines = helpers.file_raw('inputs', '2020-12-04.txt')

    passport_raw = []
    current = []
    for line in lines:
        if line:
            current.append(line)
        else:
            passport_raw.append(' '.join(current))
            current = []

    passports = []
    for passport in passport_raw:
        pp = {}
        kvps = passport.split(' ')

        for kvp in kvps:
            key, value = kvp.split(':')
            pp[key] = value

        passports.append(pp)

    return passports

@click.group()
def d4(): pass


@d4.command()
def p1():
    """Day 4, Part 1
    count number of valid passwords in file
    requires: byr, iyr, eyr, hgt, hcl, ecl, pid
    optional: cid
    """
    passports = load_data()

    valid = 0
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for passport in passports:
        valid += 1 if all(elem in passport.keys() for elem in required_fields) else 0

    print(f'output: {valid}')


@d4.command()
def p2():
    """Day 4, Part 2
    add validation rules
    """
    import re
    passports = load_data()
    valid = 0
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    clamp = lambda a,b,c: (a-1) < int(b) and int(b) <= c

    rules = {
        'byr': lambda a: clamp(1920, a, 2002),
        'iyr': lambda a: clamp(2010, a, 2020),
        'eyr': lambda a: clamp(2020, a, 2030),
        'hgt': lambda a: (a.endswith('cm') and clamp(150, a[:-2], 193)) or (a.endswith('in') and clamp(59, a[:-2], 76)),
        'hcl': lambda a: bool(re.match('^#[0-9a-fA-F]{6}$', a)),
        'ecl': lambda a: a in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda a: len(a) == 9 and a.isdigit()
    }

    for passport in passports:
        if all(elem in passport.keys() for elem in required_fields):
            valid += 1 if all(fn(passport[key]) for (key,fn) in rules.items()) else 0


    print(f'output: {valid}')
