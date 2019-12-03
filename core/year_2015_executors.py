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
@dataclass
class Node:
    name: str
    index: int = field(default=None)

class BinaryTree:
    def __init__(self, nodes = []):
        self.nodes = nodes

    def root(self):
        return self.nodes[0]

    def iparent(self, i):
        return (i - 1) // 2

    def ileft(self, i):
        return 2*i + 1

    def iright(self, i):
        return 2*i + 2

    def left(self, i):
        return self.node_at_index(self.ileft(i))

    def right(self, i):
        return self.node_at_index(self.iright(i))

    def parent(self, i):
        return self.node_at_index(self.iparent(i))

    def node_at_index(self, i):
        return self.nodes[i]

    def size(self):
        return len(self.nodes)

class MinHeap(BinaryTree):
    def __init__(self, nodes, is_less_than=lambda a,b:a<b, get_index=None, update_node=lambda n,v: v):
        super().__init__(nodes)
        self.order_mapping = list(range(len(nodes)))
        self.is_less_than, self.get_index, self.update_node = is_less_than, get_index, update_node
        self.heapify()

    def heapify(self):
        for i in range(len(self.nodes), -1, -1):
            self.heapify_subtree(i)

    def heapify_subtree(self, index):
        size = self.size()
        ileft = self.ileft(index)
        iright = self.iright(index)
        imin = index
        if ileft < size and self.is_less_than(self.nodes[ileft], self.nodes[imin]):
            imin = ileft
        if iright < size and self.is_less_than(self.nodes[iright], self.nodes[imin]):
            imin = iright
        if imin != index:
            self.nodes[index], self.nodes[imin] = self.nodes[imin], self.nodes[index]
            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[imin])] = imin
                self.order_mapping[self.get_index(self.nodes[index])] = index
            self.heapify_subtree(imin)

    def min(self):
        return self.root()

    def pop(self):
        min_node = self.nodes[0]
        if self.size() > 1:
            self.nodes[0] = self.nodes[-1]
            self.nodes.pop()
            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[0])] = 0
            self.heapify_subtree(0)
        elif self.size() == 1:
            self.nodes.pop()
        else:
            return None

        if self.get_index is not None:
            self.order_mapping[self.get_index(min_node)] = None
        return min_node

    def decrease_key(self, index, value):
        self.nodes[index] = self.update_node(self.nodes[index], value)
        iparent = self.iparent(index)

        while index != 0 and self.is_less_than(self.nodes[iparent], self.nodes[index]):
            self.nodes[iparent], self.nodes[index] = self.nodes[index], self.nodes[iparent]

            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[iparent])] = iparent
                self.order_mapping[self.get_index(self.nodes[index])] = index

            index = iparent
            iparent = self.iparent(index) if index > 0 else None

class DijkstraNodeDecorator:
    def __init__(self, node):
        self.node = node
        self.prov_dist = float('inf')
        self.hops = []

    @property
    def index(self):
        return self.node.index

    @property
    def name(self):
        return self.node.name

    def update_data(self, data):
        self.prov_dist = data['prov_dist']
        self.hops = data['hops']
        return self

class Graph:
    def __init__(self, nodes):
        self.adjacency_list = [[node, []] for node in nodes]
        for i in range(len(nodes)):
            nodes[i].index = i

    def connect_dir(self, n1, n2, w=1):
        n1, n2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        self.adjacency_list[n1][1].append((n2, w))

    def connect(self, n1, n2, w=1):
        self.connect_dir(n1, n2, w)
        self.connect_dir(n2, n1, w)

    def connections(self, node):
        node = self.get_index_from_node(node)
        return self.adjacency_list[node][1]

    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError('node must be an int or Node object')

        if isinstance(node, int):
            return node
        else:
            return node.index

    def dijkstra(self, source):
        source_index = self.get_index_from_node(source)
        # print(self.adjacency_list)

        dnodes = [DijkstraNodeDecorator(node_edges[0]) for node_edges in self.adjacency_list]
        dnodes[source_index].prov_dist = 0
        dnodes[source_index].hops.append(dnodes[source_index].node)

        is_less_than = lambda a,b: a.prov_dist < b.prov_dist
        get_index = lambda node: node.index
        update_node = lambda node, data: node.update_data(data)

        heap = MinHeap(dnodes, is_less_than, get_index, update_node)

        min_dist_list = []

        while heap.size() > 0:
            min_decorated_node = heap.pop()
            min_dist = min_decorated_node.prov_dist
            hops = min_decorated_node.hops

            min_dist_list.append([min_dist, hops])
            connections = self.connections(min_decorated_node.node)
            for inode, weight in connections:
                node = self.adjacency_list[inode][0]
                heap_location = heap.order_mapping[inode]

                if heap_location is not None:
                    total_distance = weight + min_dist
                    # print(f'Distance: {total_distance}')
                    # print(f'Target: {heap.nodes[heap_location].prov_dist}')
                    if total_distance < heap.nodes[heap_location].prov_dist:
                        hops_copy = list(hops)
                        hops_copy.append(node)
                        # print(hops_copy)
                        data = {'prov_dist': total_distance, 'hops': hops}
                        heap.decrease_key(heap_location, data)

        return min_dist_list

def aoc_2015_9_1(year, day, **kwargs):
    greet(year, day, **kwargs)

    data = load_data('2015.9.test.txt').strip('\n').split('\n')

    graph_data = []
    for datum in data:
        route, _, distance = datum.rpartition('=')
        distance = int(distance.strip())
        left, right = route.split('to')
        left = left.strip()
        right = right.strip()
        graph_data.append((left, right, distance))

    node_map = {}
    cities = set()
    adjacency_list = {}
    first = None
    distance_map = {}
    for left, right, distance in graph_data:
        if first is None:
            first = left
        if left not in node_map:
            node_map[left] = Node(left)
        if right not in node_map:
            node_map[right] = Node(right)

        cities.add(left)
        cities.add(right)

        if left not in adjacency_list:
            adjacency_list[left] = []
        if right not in adjacency_list:
            adjacency_list[right] = []

        adjacency_list[left].append(right)
        adjacency_list[right].append(left)

        distance_map[(left,right)] = distance
        distance_map[(right,left)] = distance

    print(node_map)
    print(adjacency_list)
    print(distance_map)
    print(cities)
    print('-----------------------')

    routes = []
    for city in cities:
        unvisited = cities.copy()
        unvisited.remove(city)
        route = set(city)

        while unvisited:
            break

        # min_dist = None, float('inf')
        # while unvisited:
        #     for uncity in unvisited:
        #         distance = distance_map[(city, uncity)]
        #         if distance < min_dist:
        #             min_dist = uncity, distance

        #     route.add(uncity)
        #     unvisited.remove(uncity)

        # routes.append(route)

    print(routes)


    # nodes = [node for _, node in node_map.items()]
    # print(nodes)
    # graph = Graph(nodes)

    # for left, right, distance in graph_data:
    #     print(f'connecting: {left} -> {right} -- {distance}')
    #     graph.connect(node_map[left], node_map[right], distance)

    # print('----------------')
    # for node, weight in graph.dijkstra(node_map[first]):
    #     print(node)
    #     print(weight)

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
