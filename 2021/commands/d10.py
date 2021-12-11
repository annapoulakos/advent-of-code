import click, time, logging, statistics
from modules import fileutils

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

OPENINGS = ['(', '[', '{', '<']
CLOSINGS = [')', ']', '}', '>']
POINTS = [3, 57, 1197, 25137]

class Status:
    LEGAL = 'STATUS.LEGAL'
    INCOMPLETE = 'STATUS.INCOMPLETE'
    CORRUPTED = 'STATUS.CORRUPTED'
    UNKNOWN = 'STATUS.UNKNOWN'

def check_line(line):
    stack = []

    for c in line:
        if c in OPENINGS:
            stack.append(c)
        elif c in CLOSINGS:
            x,y = OPENINGS.index(stack[-1]), CLOSINGS.index(c)
            if x == y:
                stack.pop()
            else:
                return Status.CORRUPTED, c
        else:
            return Status.UNKNOWN, None

    if len(stack) > 0:
        return Status.INCOMPLETE, None

    return Status.LEGAL, None

def get_closing(line):
    stack = []
    chars = []

    for c in line:
        if c in OPENINGS:
            stack.append(c)
        elif c in CLOSINGS:
            x,y = OPENINGS.index(stack[-1]), CLOSINGS.index(c)
            if x != y:
                chars.append(CLOSINGS[x])
            stack.pop()
        else:
            raise Exception(f'Unknown character in line {line=}')

    while len(stack) > 0:
        x = CLOSINGS[OPENINGS.index(stack.pop())]
        chars.append(x)

    return chars

def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE
    legality = [check_line(line) for line in data]
    points = [POINTS[CLOSINGS.index(c)] for _,c in legality if c is not None]

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'total={sum(points)}')
    print(f'elapsed = {end-start:.4f}')

def calculate_score(line):
    sum = 0

    for c in line:
        sum *= 5
        sum += CLOSINGS.index(c) + 1

    return sum

def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE
    legality = [check_line(line) for line in data]
    incompletes = [data[i] for i,l in enumerate(legality) if l[0] == Status.INCOMPLETE]
    missing = [get_closing(line) for line in incompletes]
    scores = [calculate_score(s) for s in missing]

    end = time.perf_counter()

    # OUTPUT HERE
    print(f'median={statistics.median(scores)}')
    print(f'elapsed = {end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d10(test, part):
    """Day 10 commands"""
    data = fileutils.load_lines(10, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
