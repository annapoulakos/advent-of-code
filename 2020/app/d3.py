import click
from app import helpers

@click.group()
def d3(): pass


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, right, down):
        self.x += right
        self.y += down

    def __str__(self):
        return f'({self.x}, {self.y})'

def load_data():
    tree_map = helpers.file_to_lines('inputs', '2020-12-03.txt')
    location = Point()
    max_d = len(tree_map)
    modulo = len(tree_map[0])

    return tree_map, location, max_d, modulo

@d3.command()
def p1():
    """Day 3, Part 1
    Take a map, determine number of trees in path of 3r1d
    """
    trees, loc, maxd, mod = load_data()
    tree_count = 0

    while True:
        loc.move(3, 1)
        if loc.y >= maxd: break

        x = loc.x % mod
        if trees[loc.y][x] == '#':
            tree_count += 1

    print(f'crashed into {tree_count} trees... welp')

@d3.command()
def p2():
    """Day 3, Part 2
    Take a map, determine the number of trees
    for each of these routes (1,1), (3,1), (5,1), (7,1), (1,2)
    multiply them together
    """
    routes = {
        (1,1): 0,
        (3,1): 0,
        (5,1): 0,
        (7,1): 0,
        (1,2): 0,
    }

    trees, _, maxd, mod = load_data()

    for route in routes:
        loc = Point()

        while True:
            loc.move(route[0], route[1])

            if loc.y >= maxd: break

            x = loc.x % mod
            if trees[loc.y][x] == '#':
                routes[route] += 1


    print('Route counts:')
    for k,v in routes.items():
        print(f'Route {k} -> Trees {v}')

    import functools
    output = functools.reduce(lambda a,b: a*b, routes.values(), 1)

    print(f'Output: {output}')
