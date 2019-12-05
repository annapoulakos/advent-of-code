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

#region 2019 - Day 5

class IntCode:
    def __init__(self, program, input_value):
        self.program = program
        self.input_value = input_value

    def parse_opcode(self, opcode):
        opcode = f'{opcode:0>5}'
        print(f'opcode: {opcode}')
        command = opcode[-2:]
        mode_3, mode_2, mode_1 = opcode[:3]

        return command, [mode_1, mode_2, mode_3]

    def value_from_mode(self, index, mode):
        return self.program[index] if mode == '0' else index

    def execute_command(self, index):
        print(f'Executing command at index {index}')
        command, modes = self.parse_opcode(self.program[index])

        if command == '01':
            """Adder"""
            print(f'Adder Params: {self.program[index:index+4]}')
            l, r, target = self.program[index+1:index+4]

            left = self.value_from_mode(l, modes[0])
            right = self.value_from_mode(r, modes[1])

            print(f'Storing {left} + {right} = {left+right} at index {target}')

            self.program[target] = left + right
            return index + 4
        elif command == '02':
            """Multi"""
            print(f'Multi Params: {self.program[index:index+4]}')
            l, r, target = self.program[index+1:index+4]

            left = self.value_from_mode(l, modes[0])
            right = self.value_from_mode(r, modes[1])

            print(f'Storing {left} * {right} = {left * right} at index {target}')

            self.program[target] = left * right
            return index + 4
        elif command == '03':
            """Input"""
            print(f'Input Params: {self.program[index:index+2]}')
            target = self.program[index + 1]
            print(f'Setting input value {self.input_value} at index {target}')
            self.program[target] = self.input_value
            return index + 2
        elif command == "04":
            """Output"""
            print(f'Output Params: {self.program[index:index+2]}')
            target = self.program[index+1]
            output = self.value_from_mode(target, modes[0])
            print(f'OUTPUT: {output}')
            return index + 2
        elif command == "05":
            """Jump if true"""
            print(f'Input Params: {self.program[index:index+3]}')
            f, s = self.program[index+1:index+3]
            first = self.value_from_mode(f, modes[0])
            second = self.value_from_mode(s, modes[1])

            print(f'Jump if True: {first} == 0 ? {second}')

            return second if first != 0 else index + 3
        elif command == "06":
            """Jump if false"""
            print(f'Input Params: {self.program[index:index+3]}')
            f, s = self.program[index+1:index+3]
            first = self.value_from_mode(f, modes[0])
            second = self.value_from_mode(s, modes[1])

            print(f'Jump if False: {first} != 0 ? {second}')
            return second if first == 0 else index + 3
        elif command == "07":
            """Less Than"""
            print(f'Input Params: {self.program[index:index+4]}')
            f, s, target = self.program[index+1:index+4]

            first = self.value_from_mode(f, modes[0])
            second = self.value_from_mode(s, modes[1])

            value = 1 if first < second else 0
            print(f'Less Than: {first} < {second}? 1: 0')
            print(f'Storing {value} at index {target}')
            self.program[target] = value

            return index + 4
        elif command == "08":
            """equals"""
            print(f'Input Params: {self.program[index:index+4]}')
            f, s, target = self.program[index+1:index+4]

            first = self.value_from_mode(f, modes[0])
            second = self.value_from_mode(s, modes[1])

            value = 1 if first == second else 0
            print(f'Equal: {first} == {second}? 1: 0')
            print(f'Storing {value} at index {target}')
            self.program[target] = value

            return index + 4
        elif command == "99":
            """END"""
            return -1

        raise Exception(f'Unable to action command {command}')


@functions.start
def aoc_2019_5_1(data, **kwargs):
    """add TEST to INTCODE Computer"""
    data = [int(x) for x in data.strip().split(',')]
    program = IntCode(data, 1)
    program_index = 0

    print(f'Total Program Elements: {len(data)}')

    while program_index != -1:
        program_index = program.execute_command(program_index)
        print('------------------------------------------------------')

@functions.start
def aoc_2019_5_2(data, **kwargs):
    """add TEST to INTCODE Computer"""
    data = [int(x) for x in data.strip().split(',')]
    program = IntCode(data, 5)
    program_index = 0

    print(f'Total Program Elements: {len(data)}')

    while program_index != -1:
        program_index = program.execute_command(program_index)
        print('------------------------------------------------------')


#endregion
