import click
import utils

from collections import namedtuple

Reindeer = namedtuple('Reindeer', 'name speed max_time rest_time')
DATA = [
    Reindeer('Comet', 14, 10, 127),
    Reindeer('Dancer', 16, 11, 162),
]

import re
PATTERN = r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.'

DATA = []
import pathlib
with open(pathlib.Path(__file__).parent / 'utils' / 'day-14.txt') as handle:
    lines = handle.read().strip().split('\n')
    for line in lines:
        matches = list(re.findall(PATTERN, line))
        if matches:
            name, spd, mt, rt = matches[0]
            DATA.append(Reindeer(name, int(spd), int(mt), int(rt)))

'''Dancer can fly 7 km/s for 20 seconds, but then must rest for 119 seconds.'''

def distance_traveled(reindeer, max_time=2503):
    time = 0
    distance = 0
    while max_time > time:
        distance += reindeer.speed * reindeer.max_time
        time += reindeer.max_time

        if time >= max_time:
            time -= reindeer.max_time
            distance -= reindeer.speed * reindeer.max_time
            for _ in range(reindeer.max_time):
                distance += reindeer.speed
                time += 1
                if time >= max_time:
                    return distance

        time += reindeer.rest_time

    return distance



@click.command()
def cli():
    distances = {}

    for reindeer in DATA:
        traveled = distance_traveled(reindeer)
        distances[reindeer] = traveled

    for k,v in distances.items():
        print(f'{k.name}: {v}')



if __name__ == '__main__':
    cli()
