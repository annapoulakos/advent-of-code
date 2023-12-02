from __future__ import annotations
import click, time, json, functools
from modules import fileutils
from collections import defaultdict

def log(**kw):
    if not kw:
        print('='*40)
        return
    for k,v in kw.items():
        print(f'{k} => {v}')

PATHS = []

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def count_paths(self, allow_double:bool=False):
        @functools.lru_cache()
        def drop(node:str, visited:frozenset, twice:bool) -> int:
            count = 0
            for child in self.graph[node]:
                if child == 'start': continue
                elif child == 'end': count += 1
                elif child.isupper(): count += drop(child, visited, twice)
                elif child not in visited: count += drop(child, frozenset(visited | {child}), twice)
                elif not twice: count += drop(child, visited, True)
            return count

        paths = drop('start', frozenset(), not allow_double)
        log(num_paths=paths)


def build_graph(data) -> Graph:
    graph = Graph()

    for line in data:
        left,_,right = line.partition('-')

        graph.add_edge(left, right)

    return graph

def part_1(data):
    """Part 1"""
    start = time.perf_counter()

    # CODE HERE
    graph = build_graph(data)
    graph.count_paths(False)

    end = time.perf_counter()

    # OUTPUT HERE
    log(elapsed=f'{end-start:.4f}')


def part_2(data):
    """Part 2"""
    start = time.perf_counter()

    # CODE HERE
    graph = build_graph(data)
    graph.count_paths(True)

    end = time.perf_counter()

    # OUTPUT HERE
    log(elapsed=f'{end-start:.4f}')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False)
@click.argument('part', type=int)
def d12(test, part):
    """Day 12 commands"""
    print(f'AoC :: Day 12 :: Part {part} {":: (test)" if test else ""}')
    data = fileutils.load_lines(12, test)

    fn = {
        1: part_1,
        2: part_2,
    }.get(part)

    fn(data)
