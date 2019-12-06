import pathlib
import core.functions as functions
import json
import numbers
import re
from dataclasses import dataclass, field
import itertools


base_path = pathlib.Path(__file__).parent

def greet(year, day, puzzle, **kwargs):
    print(f'{year}.{day}.{puzzle} -> begin')

def load_data(filename):
    with (base_path/'data'/filename).open('r') as handle:
        return handle.read()

def turn_on(value):
    return value | 1

def turn_off(value):
    return value & 0

def toggle(value):
    return value ^ 1



def aoc_2015_1_1(year, day, **kwargs):
    greet(year, day, **kwargs)
    data = load_data('2015.1.txt')
    result = sum([1 if d == '(' else -1 for d in data])
    print(f'result: {result}')

def aoc_2015_6_1(year, day, **kwargs):
    greet(year, day, **kwargs)
    data = load_data('2015.6.txt').strip('\n').split('\n')

    print('-> creating grid')
    import numpy as np
    import itertools
    grid = np.zeros([1000,1000], dtype=int)

    from collections import defaultdict
    alt_grid = defaultdict(lambda:0)

    for datum in data:
        # print(f'-> Original: {datum}')
        datum = datum.replace('turn ', '').replace('through ', '')
        # print(f'-> Updated: {datum}')

        command, first, second = datum.split(' ')
        start = [int(x) for x in first.split(',')]
        end = [int(x) for x in second.split(',')]

        fn = {
            'on': turn_on,
            'off': turn_off,
            'toggle': toggle,
        }.get(command)

        print(f'-> Command: {command} {start[0]},{end[0]}:{start[1]},{end[1]}')
        # print(f'-> Starting coords: {start}')
        # print(f'-> Ending coords: {end}')

        iterations = 0
        for x,y in itertools.product(range(start[0], end[0]+1), range(start[1], end[1]+1)):
            grid[x,y] = fn(grid[x,y])
            alt_grid[(x,y)] = fn(alt_grid[(x,y)])
            iterations += 1

        print(f'-> Iterations: {iterations}')
        print(f'-> Current Count: {np.sum(grid)}')

    print(f'-> Total: {np.sum(grid)}')
    count = sum([v for k,v in alt_grid.items()])
    print(count)

def aoc_2015_6_2(year, day, **kwargs):
    import numpy as np
    import itertools

    greet(year, day, **kwargs)
    data = load_data('2015.6.txt').strip('\n').split('\n')

    def on(value):
        return value + 1
    def off(value):
        return 0 if value == 0 else value - 1
    def toggle(value):
        return value + 2

    grid = np.zeros([1000,1000], dtype=int)

    for datum in data:
        datum = datum.replace('turn ', '').replace('through ', '')

        command, first, second = datum.split(' ')
        start = [int(x) for x in first.split(',')]
        end = [int(x) for x in second.split(',')]
        fn = {
            'on': on,
            'off': off,
            'toggle': toggle,
        }.get(command)

        range_x = range(start[0], end[0] + 1)
        range_y = range(start[1], end[1] + 1)

        iterations = 0
        for x,y in itertools.product(range_x, range_y):
            grid[x,y] = fn(grid[x,y])
            iterations += 1

        print(f'-> Command: {command} for rectangle: {first} to {second}')
        print(f'-> Iterations: {iterations}')
        print(f'-> Current Brightness: {np.sum(grid)}')

    print(f'-> Total Brightness: {np.sum(grid)}')

def aoc_2015_7_1(year, day, **kwargs):
    greet(year, day, **kwargs)

    #region Imports
    import re
    from collections import namedtuple
    #endregion

    #region Builtins
    Action = namedtuple('Action', 'instruction target')
    #endregion

    #region Setup
    data = load_data('2015.7.txt').strip('\n').split('\n')

    command_list = []
    for datum in data:
        instruction, _, target = datum.partition(' -> ')
        command_list.append(Action(instruction, target))

    registers = {}
    #endregion

    #region Execute
    setters = [action for action in command_list if re.match('^\d+$', action.instruction)]
    for setter in setters:
        registers[setter.target] = int(setter.instruction)

    not_executed = [action for action in command_list if action not in setters]

    iterations = 0
    while(not_executed):
        iterations += 1
        print(f'-> Iteration: {iterations}, unexecuted actions: {len(not_executed)}')
        executed = []

        for action in not_executed:
            if re.match('^[a-z]{1,2}$', action.instruction) and action.instruction in registers:
                registers[action.target] = registers[action.instruction]
                executed.append(action)
                continue

            if action.instruction.startswith('NOT'):
                register = action.instruction.replace('NOT', '').strip()
                if register in registers:
                    registers[action.target] = ~registers[register]
                    executed.append(action)
                    continue

            if 'AND' in action.instruction or 'OR' in action.instruction:
                left, command, right = action.instruction.split(' ')
                if command == 'AND':
                    fn = lambda a,b: a & b
                else:
                    fn = lambda a,b: a | b
                execute = False

                if left.isnumeric() and right.isnumeric():
                    left = int(left)
                    right = int(right)
                    execute = True
                elif left.isnumeric() and right in registers:
                    left = int(left)
                    right = registers[right]
                    execute = True
                elif right.isnumeric() and left in registers:
                    left = registers[left]
                    right = int(right)
                    execute = True
                elif left in registers and right in registers:
                    left = registers[left]
                    right = registers[right]
                    execute = True

                if execute:
                    registers[action.target] = fn(left, right)
                    executed.append(action)
                    continue

            if 'SHIFT' in action.instruction:
                left, command, right = action.instruction.split(' ')
                if command == 'LSHIFT':
                    fn = lambda a,b: a << b
                else:
                    fn = lambda a,b: a >> b

                if left in registers:
                    right = int(right)
                    registers[action.target] = fn(registers[left], right)
                    executed.append(action)
                    continue

        print(f'-> Executed {len(executed)} actions')
        not_executed = list(filter(lambda a: a not in executed, not_executed))

    for k,v in registers.items():
        registers[k] = v & 0xFFFF

    #endregion

    #region Output
    print(registers)
    #endregion

def aoc_2015_7_2(year, day, **kwargs):
    greet(year, day, **kwargs)

    #region Imports
    import re
    from collections import namedtuple
    #endregion

    #region Builtins
    Action = namedtuple('Action', 'instruction target')
    #endregion

    #region Setup
    data = load_data('2015.7.txt').strip('\n').split('\n')

    command_list = []
    for datum in data:
        instruction, _, target = datum.partition(' -> ')
        command_list.append(Action(instruction, target))

    registers = {
        'b': 16076
    }
    #endregion

    #region Execute
    setters = [action for action in command_list if re.match('^\d+$', action.instruction)]
    for setter in setters:
        if setter.target == 'b':
            continue
        registers[setter.target] = int(setter.instruction)

    not_executed = [action for action in command_list if action not in setters]

    iterations = 0
    while(not_executed):
        iterations += 1
        print(f'-> Iteration: {iterations}, unexecuted actions: {len(not_executed)}')
        executed = []


        for action in not_executed:
            if action.target == 'b':
                executed.append(action)
                continue
            if re.match('^[a-z]{1,2}$', action.instruction) and action.instruction in registers:
                registers[action.target] = registers[action.instruction]
                executed.append(action)
                continue

            if action.instruction.startswith('NOT'):
                register = action.instruction.replace('NOT', '').strip()
                if register in registers:
                    registers[action.target] = ~registers[register]
                    executed.append(action)
                    continue

            if 'AND' in action.instruction or 'OR' in action.instruction:
                left, command, right = action.instruction.split(' ')
                if command == 'AND':
                    fn = lambda a,b: a & b
                else:
                    fn = lambda a,b: a | b
                execute = False

                if left.isnumeric() and right.isnumeric():
                    left = int(left)
                    right = int(right)
                    execute = True
                elif left.isnumeric() and right in registers:
                    left = int(left)
                    right = registers[right]
                    execute = True
                elif right.isnumeric() and left in registers:
                    left = registers[left]
                    right = int(right)
                    execute = True
                elif left in registers and right in registers:
                    left = registers[left]
                    right = registers[right]
                    execute = True

                if execute:
                    registers[action.target] = fn(left, right)
                    executed.append(action)
                    continue

            if 'SHIFT' in action.instruction:
                left, command, right = action.instruction.split(' ')
                if command == 'LSHIFT':
                    fn = lambda a,b: a << b
                else:
                    fn = lambda a,b: a >> b

                if left in registers:
                    right = int(right)
                    registers[action.target] = fn(registers[left], right)
                    executed.append(action)
                    continue

        print(f'-> Executed {len(executed)} actions')
        not_executed = list(filter(lambda a: a not in executed, not_executed))

    for k,v in registers.items():
        registers[k] = v & 0xFFFF

    #endregion

    #region Output
    print(registers)
    #endregion

def get_in_memory_char_count(datum):
    decoded = datum.encode('utf-8').decode('unicode-escape')
    return len(decoded) - 2

def get_encoded_size(datum):
    datum = datum.replace('\\', '\\\\')
    datum = datum.replace('"', '\\"')
    datum = f'"{datum}"'
    return len(datum)

def aoc_2015_8_1(year, day, **kwargs):
    greet(year, day, **kwargs)

    data = load_data('2015.8.txt').strip('\n').split('\n')

    sizes = [(len(datum), get_in_memory_char_count(datum)) for datum in data]
    code_size = sum([s[0] for s in sizes])
    mem_size = sum([s[1] for s in sizes])

    print(f'Code: {code_size}')
    print(f'Memory: {mem_size}')
    print(f'Diff: {code_size - mem_size}')

def aoc_2015_8_2(year, day, **kwargs):
    greet(year, day, **kwargs)

    data = load_data('2015.8.txt').strip('\n').split('\n')

    def enc(datum):
        datum = datum.replace('\\', '\\\\')
        datum = datum.replace('"', '\\"')
        return f'"{datum}"'

    sizes = [(len(datum), get_encoded_size(datum)) for datum in data]
    code_size = sum([s[0] for s in sizes])
    enc_size = sum([s[1] for s in sizes])

    print(f'Code: {code_size}')
    print(f'Encoded: {enc_size}')
    print(f'Diff: {enc_size - code_size}')


#region Day 9
import itertools

def generate_route_distances(routes, distance_data):
    distances = []
    for route in routes:
        route_distance = 0
        valid = False
        for index, city in enumerate(route[1:]):
            key = (route[index], route[index+1])
            valid = key in distance_data
            if valid:
                route_distance += distance_data[key]
            else:
                break

        if valid:
            distances.append((route, route_distance))
    return distances

def generate_city_data(raw_data):
    distance_data = {}
    cities = set()
    for datum in raw_data:
        route, _, distance = datum.rpartition('=')
        start, _, end = route.partition('to')
        start = start.strip()
        end = end.strip()
        distance = int(distance.strip())

        distance_data[(start,end)] = distance
        distance_data[(end,start)] = distance
        cities.add(start)
        cities.add(end)
    return distance_data, cities

@functions.start
def aoc_2015_9_1(data, **kwargs):
    raw_data = data.strip().split('\n')

    data, cities = generate_city_data(raw_data)
    routes = [list(route) for route in itertools.permutations(cities)]
    distances = generate_route_distances(routes, data)

    min_distance = float('inf')
    min_route = None
    for route, distance in distances:
        if distance < min_distance:
            min_distance = distance
            min_route = route

    print(min_distance, min_route)

@functions.start
def aoc_2015_9_2(data, **kwargs):
    raw_data = data.strip().split('\n')

    data, cities = generate_city_data(raw_data)
    routes = [list(route) for route in itertools.permutations(cities)]
    distances = generate_route_distances(routes, data)

    max_distance = -1
    max_route = None
    for route, distance in distances:
        if distance > max_distance:
            max_distance = distance
            max_route = route

    print(max_distance, max_route)
#endregion

#region 2015 - Day 10

@functions.start
def aoc_2015_10_1(data, **kwargs):
    """Get result length of look-and-say starting value over 40 iterations"""
    data = data.strip()
    size = len(data)

    def transform(value):
        char = value[0]
        count = 1
        value = value[1:] + ' '
        output = ''

        for actual in value:
            if actual != char:
                output += f'{count}{char}'
                count = 1
                char = actual
            else:
                count += 1

        return output

    for _ in range(40):
        data = transform(data)

    print(len(data))
    import math
    conways = size * math.pow(1.303577269, 40)
    print(f'Conways: {conways}')


@functions.start
def aoc_2015_10_2(data, **kwargs):
    """Get result length of look-and-say starting value over 50 iterations"""
    data = data.strip()

    import math
    size = len(data) * math.pow(1.303577269, 50)
    print(size)

    def transform(value):
        char = value[0]
        count = 1
        value = value[1:] + ' '
        output = ''

        for actual in value:
            if actual != char:
                output += f'{count}{char}'
                count = 1
                char = actual
            else:
                count += 1

        return output

    for _ in range(50):
        data = transform(data)

    print(len(data))


#endregion

#region 2015 - Day 11

BANNED = [ord('i'), ord('o'), ord('l')]

def passes_rules(password_array):
    # Must have a straight of three chars
    for index, _ in enumerate(password_array[3:]):
        first, second, third = password_array[index:index+3]
        if first == second + 1 and second == third + 1:
            break
    else:
        return False, 'No consecutive values'

    # Must not contained banned letters
    if any([l in BANNED for l in password_array]):
        return False, 'Contains banned characters'

    # Must contain two different pairs
    pairs = set()
    for index, _ in enumerate(password_array[2:]):
        first, second = password_array[index:index+2]
        if first == second:
            pairs.add(first)

    if len(pairs) < 2:
        return False, 'Less than two pairs'

    return True, ''

@functions.start
def aoc_2015_11_1(data, **kwargs):
    """Creating a new password for the santa boss"""
    #data = 'ghijklmn'
    data = data.strip()
    ALPHA, ZED = ord('a'), ord('z')

    data = [ord(l) for l in reversed(data)]

    def stringify(arr):
        return ''.join([chr(l) for l in reversed(arr)])

    def increment(arr):
        if not arr:
            raise Exception('Welp, ran out of numbers to increment')

        arr[0] += 1
        if arr[0] > ZED:
            arr = [ALPHA] + increment(arr[1:])

        return arr

    print(f'Starting Password: {data} ({stringify(data)})')
    while True:
        passes, _ = passes_rules(data)
        if passes:
            break
        data = increment(data)

    print(f'Ending Password: {data} ({stringify(data)})')

@functions.start
def aoc_2015_11_2(data, **kwargs):
    """Make a second password after the first"""
    data = 'vzbxxyzz'
    ALPHA, ZED = ord('a'), ord('z')

    data = [ord(l) for l in reversed(data)]

    def stringify(arr):
        return ''.join([chr(l) for l in reversed(arr)])

    def increment(arr):
        if not arr:
            raise Exception('Welp, ran out of numbers to increment')

        arr[0] += 1
        if arr[0] > ZED:
            arr = [ALPHA] + increment(arr[1:])

        return arr

    print(f'Starting Password: {data} ({stringify(data)})')
    while True:
        data = increment(data)
        passes, _ = passes_rules(data)
        if passes:
            break

    print(f'Final Password: {data} ({stringify(data)})')

#endregion

#region 2015 - Day 12

@functions.start
def aoc_2015_12_1(data, **kwargs):
    """Balancing the elves' books..."""
    data = json.loads(data)

    flat = functions.flatten_json(data)
    only_numbers = [x for _, x in flat.items() if isinstance(x, numbers.Number)]

    print(f'Length of original flattened list: {len(flat)}')
    print(f'Length of only numbers: {len(only_numbers)}')
    print(sum(only_numbers))



@functions.start
def aoc_2015_12_2(data, **kwargs):
    """Balancing the elves' books now that they've screwed them all up......"""
    data = json.loads(data)

    def remove_red(nested):
        out = None
        if type(nested) is list:
            out = [remove_red(x) for x in nested]
        elif type(nested) is dict:
            out = {}
            for a,x in nested.items():
                if x == 'red': return {}
                else:
                    out[a] = remove_red(x)
        else:
            out = nested
        return out

    cleaned = remove_red(data)
    flat = functions.flatten_json(cleaned)
    nums = [x for _, x in flat.items() if isinstance(x, numbers.Number)]
    print(sum(nums))
#endregion

#region 2015 - Day 13

@functions.start
def aoc_2015_13_1(data, **kwargs):
    """Best seating arrangements..."""
    data = data.strip().split('\n')

    data = [
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

    REGEX_MATCHER = r'(\w+)\swould\s(gain|lose)\s(\d+)\shappiness units by sitting next to (\w+)\.'

    people = set()
    weights = {}
    for datum in data:
        matches = re.findall(REGEX_MATCHER, datum)
        if matches:
            left, action, value, right = list(matches[0])
            people.add(left)
            people.add(right)
            value = int(value) if action == 'gain' else -1 * int(value)
            weights[(left, right)] = value

    people = list(people)
    print(people)
    print(weights)

    first_person = people[0]
    seats = list(itertools.permutations(people[1:], 3))
    print(seats)

    for order in seats:
        group = [first_person] + list(order)
        print(f'Group: {group}')


@functions.start
def aoc_2015_13_2(data, **kwargs):
    """"""


#endregion

#region Year 2015 - Day 15
from collections import namedtuple
import re

Ingredient = namedtuple('Ingredient', 'name capacity durability flavor texture calories')

def calculate_score(recipe):
    capacity, durability, flavor, texture, calories = [0]*5

    for ingredient, count in recipe.items():
        capacity += count * ingredient.capacity
        durability += count * ingredient.durability
        flavor += count * ingredient.flavor
        texture += count * ingredient.texture
        calories += count * ingredient.calories

    if capacity < 0 or durability < 0 or flavor < 0 or texture < 0:
        return 0, 0

    return capacity * durability * flavor * texture, calories

def generate_recipe(ingredients):
    import itertools
    for combination in itertools.combinations_with_replacement(ingredients, 100):
        yield combination

@functions.start
def aoc_2015_15_1(data, **kwargs):
    """Let's make cookies. The best cookies. Better than any other cookie."""
    data = data.strip().split('\n')
    print(data)

    '''Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1'''
    PATTERN = r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'
    ingredients = []
    for line in data:
        matches = re.findall(PATTERN, line)
        if matches:
            stats = [matches[0][0], int(matches[0][1]), int(matches[0][2]), int(matches[0][3]), int(matches[0][4]), int(matches[0][5])]
            ingredients.append(Ingredient(*stats))

    import itertools
    from collections import defaultdict
    best_score, best_recipe = 0, None
    for ingredient_list in itertools.combinations_with_replacement(ingredients, 100):
        recipe = defaultdict(lambda: 0)
        for ingredient in ingredient_list:
            recipe[ingredient] += 1

        score, _ = calculate_score(recipe)
        if score > best_score:
            best_score = score
            best_recipe = recipe.copy()

    print(best_score)
    print(best_recipe)

@functions.start
def aoc_2015_15_2(data, **kwargs):
    """Let's make cookies, but this time with only 500 calories"""
    data = data.strip().split('\n')
    print(data)

    '''Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1'''
    PATTERN = r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'
    ingredients = []
    for line in data:
        matches = re.findall(PATTERN, line)
        if matches:
            stats = [matches[0][0], int(matches[0][1]), int(matches[0][2]), int(matches[0][3]), int(matches[0][4]), int(matches[0][5])]
            ingredients.append(Ingredient(*stats))

    import itertools
    from collections import defaultdict
    best_score, best_recipe = 0, None
    for ingredient_list in itertools.combinations_with_replacement(ingredients, 100):
        recipe = defaultdict(lambda: 0)
        for ingredient in ingredient_list:
            recipe[ingredient] += 1

        score, calories = calculate_score(recipe)
        if calories == 500 and score > best_score:
            best_score = score
            best_recipe = recipe.copy()

    print(best_score)
    print(best_recipe)
#endregion

#region Year 2015 - Day 16
MFSCAM_DATA = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

def build_aunt_list(data):
    aunts = []
    for line in data:
        aunt, _, info = line.partition(':')
        _, _, aunt_identifier = aunt.partition(' ')
        aunt_data_points = info.split(',')
        aunt_data = {}
        for ad in aunt_data_points:
            item, quantity = ad.split(':')
            item = item.strip()
            quantity = int(quantity.strip())
            aunt_data[item] = quantity
        aunts.append((aunt_identifier, aunt_data))
    return aunts

@functions.start
def aoc_2015_16_1(data, **kwargs):
    data = data.strip().split('\n')
    aunts = build_aunt_list(data)

    for key, value in MFSCAM_DATA.items():
        aunts_to_remove = []
        for aunt in aunts:
            _, aunt_data = aunt
            if key in aunt_data and aunt_data[key] != value:
                aunts_to_remove.append(aunt)

        for a in aunts_to_remove:
            aunts.remove(a)

    print(aunts)

@functions.start
def aoc_2015_16_2(data, **kwargs):
    data = data.strip().split('\n')
    aunts = build_aunt_list(data)

    for key, value in MFSCAM_DATA.items():
        aunts_to_remove = []
        for aunt in aunts:
            _, aunt_data = aunt
            if key in aunt_data:
                if key in ['cats', 'trees']:
                    if aunt_data[key] <= value:
                        print(f'removing {aunt} for cats|trees issue (must be gt {value})')
                        aunts_to_remove.append(aunt)
                elif key in ['pomeranians', 'goldfish']:
                    if aunt_data[key] >= value:
                        print(f'removing {aunt} for pomeranians|goldfish issue (must be less than {value})')
                        aunts_to_remove.append(aunt)
                else:
                    if aunt_data[key] != value:
                        print(f'removing {aunt} for value failure {key}, {value}')
                        aunts_to_remove.append(aunt)

        for a in aunts_to_remove:
            aunts.remove(a)

    print(aunts)

#endregion

#region Year 2015 - Day 17
def parse_data_17(data):
    return [int(x) for x in data.strip().split('\n')]

def create_combinations(data):
    import itertools
    all_combinations = []
    for s in range(1, len(data)+1):
        combinations = list(itertools.combinations(data, s))
        all_combinations += combinations

    return all_combinations

def get_combinations_matching(data, target):
    all_combinations = create_combinations(data)

    matching = [combination for combination in all_combinations if sum(combination) == target]
    return matching

@functions.start
def aoc_2015_17_1(data, **kwargs):
    """"""
    data = parse_data_17(data)
    TARGET_SIZE = 150
    matching_combinations = get_combinations_matching(data, TARGET_SIZE)

    print(f'found {len(matching_combinations)} matches')

@functions.start
def aoc_2015_17_2(data, **kwargs):
    """"""
    data = parse_data_17(data)
    TARGET_SIZE = 150

    matches = get_combinations_matching(data, TARGET_SIZE)
    print(f'Found {len(matches)} matches.')
    sizes = set([len(m) for m in matches])
    print(f'Found {len(sizes)} distinct sizes: {sizes}')

    smallest = min(sizes)
    print(f'Looking for combinations with size {smallest}')
    small_matches = [m for m in matches if len(m) == smallest]
    print(f'Found {len(small_matches)} matches')


#endregion


#region Year 2015 - Day 18
class Matrix:
    def __init__(self):
        from collections import defaultdict
        import itertools
        self.__internal = defaultdict(lambda: False)

        self.__size = (0,0)

    def __getitem__(self, key):
        return self.__internal[key]

    def get_surrounding(self, key):
        x,y = key
        surrounding = []
        for ix, iy in self.iterator(key=key):
            mx, my = ix-1, iy-1
            if mx == x and my == y:
                continue

            surrounding.append(self[(mx,my)])

        assert len(surrounding) == 8
        return surrounding

    def print(self):
        x,y = self.size
        for ix, iy in self.iterator():
            print('#' if self[(ix,iy)] else '.')

    def iterator(self, key=None):
        x, y = key if key is not None else self.size
        return itertools.product(range(x), range(y))

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value


    @property
    def x(self):
        x, _ = self.size
        return x

    @property
    def y(self):
        _, y = self.size
        return y

def generate_matrix(data):
    lines = data.strip().split('\n')
    matrix = Matrix()

    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            matrix[(x,y)] = char == '#'

    size = len(lines), len(lines[0])
    matrix.size = size

    return matrix



@functions.start
def aoc_2015_18_1(data, **kwargs):
    """Animating the lights..."""
    data = '.#.#.#\n...##.\n#....#\n..#...\n#.#..#\n####..'
    matrix = generate_matrix(data)
    print(matrix)

    import itertools

    for x,y in itertools.product(range(matrix.x), range(matrix.y)):
        s = matrix.get_surrounding((x,y))
        print(s)
