import click, time
from modules import fileutils
from collections import Counter

def log(**kw):
    if not kw: print('='*60)
    for k,v in kw.items(): print(f'{k} => {v}')

def build_polymer(polymer, instructions, iterations):
    pairs = Counter([polymer[i:i+2] for i in range(len(polymer)-1)])

    for _ in range(iterations):
        temp_pairs = Counter()
        for pair, count in pairs.items():
            temp_pairs[pair[0]+instructions[pair]] += count
            temp_pairs[instructions[pair]+pair[1]] += count
        pairs = temp_pairs

    letter_counts = Counter()
    for pair, count in pairs.items():
        for letter in pair:
            letter_counts[letter] += count

    # love me some off-by-one errors :argh:
    letter_counts[polymer[0]] += 1
    letter_counts[polymer[-1]] += 1

    mn,mx = min(letter_counts.values()), max(letter_counts.values())

    # forgot i am basically doubling each letter in the count
    return (mx - mn) // 2


def part_1(starter, instructions):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE
    diff = build_polymer(starter, instructions, 10)

    end = time.perf_counter()

    # OUTPUT HERE
    log(diff=diff)
    print(f'elapsed = {end-start:.4f}')


def part_2(starter, instructions):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE
    diff = build_polymer(starter, instructions, 40)

    end = time.perf_counter()

    # OUTPUT HERE
    log(diff=diff)
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d14(test, part):
    """Day 14 commands"""
    print(f'AoC :: Day 14 :: Part {part} {":: (test)" if test else ""}')
    data = fileutils.load_lines(14, test)

    starter = data[0]
    instructions = {}
    for line in data[1:]:
        if not line: continue
        c,_,o = line.partition('->')
        instructions[c.strip()] = o.strip()

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(starter, instructions)
