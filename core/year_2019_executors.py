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

@functions.start
def aoc_2019_3_1(data, **kwargs):
    """Find distance to closest port"""
    data = data.strip().split('\n')
    # data = ['R75,D30,R83,U83,L12,D49,R71,U7,L72,U62,R66,U55,R34,D71,R55,D58,R83',
    # 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51,U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']
    first_path, second_path = [d.split(',') for d in data]



    from collections import defaultdict
    sparse_matrix = defaultdict(lambda: 0)

    sparse_matrix[(0,0)] = -1

    x = 0
    y = 0
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
    print(crossings)
    distances = {}
    for crossing in crossings:
        x,y = crossing

        distances[crossing] = abs(x) + abs(y)


    print(min(distances.values()))

def update_matrix(matrix, path, value):
    x,y = 0,0
    for part in path:
        direction, distance = part_to_vector(part)
        for _ in range(distance):
            x,y = move(x,y,distance)
            matrix[(x,y)] += value

    return matrix

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
def aoc_2019_3_2(data, **kwargs):
    """Find first crossing  (by steps)"""
    data = data.strip().split('\n')
    # data = ['R75,D30,R83,U83,L12,D49,R71,U7,L72,U62,R66,U55,R34,D71,R55,D58,R83',
    # 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51,U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']

    # data = [
    #     'R8,U5,L5,D3',
    #     'U7,R6,D4,L4'
    # ]

    first_path, second_path = [d.split(',') for d in data]



    from collections import defaultdict
    sparse_matrix = defaultdict(lambda: 0)

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

    print(intersections)

    smallest = float('inf')
    for _,_,intersect in intersections.values():
        if intersect < smallest:
            smallest = intersect

    print(smallest)



#endregion
