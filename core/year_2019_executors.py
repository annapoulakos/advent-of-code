import core.functions as functions
import math
import itertools

#region 2019 - Day 1
@functions.start
def aoc_2019_1_1(data, **kwargs):
    data = data.strip().split('\n')

    convert = lambda x: math.floor(int(x) / 3) - 2
    fuel_required = [convert(datum) for datum in data]

    print(sum(fuel_required))

@functions.start
def aoc_2019_1_2(data, **kwargs):
    data = data.strip().split('\n')

    convert = lambda x: math.floor(int(x) // 3) - 2

    fuel_required = []
    for datum in data:
        module_fuel = convert(datum)
        addl_module_fuel = convert(module_fuel)
        module_fuel += addl_module_fuel

        while True:
            addl_module_fuel = convert(addl_module_fuel)
            if addl_module_fuel < 0:
                break

            module_fuel += addl_module_fuel

        fuel_required.append(module_fuel)

    print(fuel_required)
    print(sum(fuel_required))
#endregion

#region 2019 - Day 2
f_add = lambda a,b: a+b
f_mul = lambda a,b: a*b
def execute_program(program):
    #print(f'executing program: {program[:4]}')
    pointer = 0
    while True:
        opcode = program[pointer]
        if opcode == 99:
            break

        left, right, target = program[pointer+1:pointer+4]
        fn = f_add if opcode == 1 else f_mul
        value = fn(program[left], program[right])
        program[target] = value
        pointer += 4

    #print(f'Results: {program[:4]}')
    return program


@functions.start
def aoc_2019_2_1(data, **kwargs):
    """Create and INTCODE computer... Damn elves"""
    data = [int(d) for d in data.strip().split(',')]

    data[1] = 12
    data[2] = 2

    result = execute_program(data)
    print(result[:4])


@functions.start
def aoc_2019_2_2(data, **kwargs):
    """Find the correct target vector... damn elves"""
    data = [int(d) for d in data.strip().split(',')]

    for n,v in itertools.product(range(100), range(100)):
        intcode = data.copy()
        intcode[1] = n
        intcode[2] = v

        result = execute_program(intcode)

        if result[0] == 19690720:
            print(f'Found: {result[0]}')
            print(f'Noun: {result[1]}')
            print(f'Verb: {result[2]}')
            print(f'Output: {(100*result[1]) + result[2]}')
            break
#endregion

#region 2019 - Day 3
def part_to_vector(part):
    return part[0], int(part[1:])

def move(x,y,direction):
    if direction == 'R':
        x += 1
    elif direction == 'L':
        x -= 1
    elif direction == 'U':
        y += 1
    elif direction == 'D':
        y -= 1

    return x,y

def get_distance_to(target_x, target_y, path):
    x,y,steps = 0,0,0
    for part in path:
        direction, distance = part_to_vector(part)
        for _ in range(distance):
            x,y = move(x,y,direction)
            steps += 1
            if target_x == x and target_y == y:
                return steps

    return steps


@functions.start
def aoc_2019_3_1(data, **kwargs):
    """Find distance to closest port"""
    data = data.strip().split('\n')
    first_path, second_path = [d.split(',') for d in data]

    sparse_matrix = functions.sparse_matrix()
    sparse_matrix[(0,0)] = -1

    x, y = 0, 0
    for part in first_path:
        direction, distance = part_to_vector(part)
        for _ in range(distance):
            x,y = move(x,y,direction)
            sparse_matrix[(x,y)] = 1

    x, y = 0, 0
    for part in second_path:
        direction, distance = part_to_vector(part)
        for _ in range(distance):
            x,y = move(x,y,direction)
            sparse_matrix[(x,y)] += 2

    crossings = [k for k,v in sparse_matrix.items() if v == 3]
    distances = {}
    for crossing in crossings:
        x,y = crossing
        distances[crossing] = abs(x) + abs(y)

    print(min(distances.values()))


@functions.start
def aoc_2019_3_2(data, **kwargs):
    """Find first crossing  (by steps)"""
    data = data.strip().split('\n')
    first_path, second_path = [d.split(',') for d in data]

    sparse_matrix = functions.sparse_matrix()
    sparse_matrix[(0,0)] = -1

    x,y = 0,0
    for part in first_path:
        direction, distance = part_to_vector(part)
        for _ in range(distance):
            x,y = move(x,y,direction)
            sparse_matrix[(x,y)] = 1

    x, y = 0, 0
    for part in second_path:
        direction, distance = part_to_vector(part)
        for _ in range(distance):
            x,y = move(x,y,direction)
            sparse_matrix[(x,y)] += 2

    crossings = [k for k,v in sparse_matrix.items() if v > 2]

    intersections = {}
    for crossing in crossings:
        first_dist = get_distance_to(*crossing, first_path)
        second_dist = get_distance_to(*crossing, second_path)
        intersections[crossing] = (first_dist, second_dist, first_dist+second_dist)

    smallest = float('inf')
    for _,_,intersect in intersections.values():
        if intersect < smallest:
            smallest = intersect

    print(smallest)
#endregion

#region 2019 - Day 4
import re

def ascending(nums):
    return nums[5] >= nums[4] >= nums[3] >= nums[2] >= nums[1] >= nums[0]

@functions.start
def aoc_2019_4_1(data, **kwargs):
    """Password crackin' part 1"""
    lower, upper = data.strip().split('-')
    lower = int(lower)
    upper = int(upper)

    match_criteria = []
    PATTERN = r'(\d)\1+'
    for x in range(lower, upper+1):
        matches = re.search(PATTERN, str(x))
        if matches:
            nums = str(x)
            if ascending(nums):
                match_criteria.append(x)

    print(match_criteria)
    print(f'found {len(match_criteria)} matches')

@functions.start
def aoc_2019_4_2(data, **kwargs):
    """better password crackin'"""

    lower, upper = data.strip().split('-')
    lower = int(lower)
    upper = int(upper)

    match_criteria = []

    matches = [x for x in range(lower, upper) if ascending(str(x))]
    print(f'Matches only ascending numbers: {len(matches)}')

    def has_pair(val):
        s = str(val)
        matches = re.findall(r'(\d)\1+', s)

        if not matches:
            return False

        counts = []
        for m in matches:
            counts.append(len([l for l in s if l == m]))

        return any([True for c in counts if c == 2])

    matches = [x for x in matches if has_pair(x)]
    print(f'Found values with at least 1 matching pair (but no larger groups: {len(matches)}')


#endregion
