import click
import utils

from collections import namedtuple

#Reindeer = namedtuple('Reindeer', 'name speed max_time rest_time')

class Reindeer:
    def __init__(self, name, spd, mt, rt):
        self.name = name
        self.speed = spd
        self.max_time = mt
        self.rest_time = rt

        self.distance = 0
        self.current_timer = 0
        self.points = 0
        self.resting = False

    def move(self):
        self.current_timer += 1

        if self.resting:
            if self.current_timer >= self.rest_time:
                self.resting = False
                self.current_timer = 0
        else:
            self.distance += self.speed
            if self.current_timer >= self.max_time:
                self.resting = True
                self.current_timer = 0

    def score(self):
        self.points += 1

    def __str__(self):
        return f'{self.name}: {self.distance} km, {self.points} points'

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


# def distance_traveled(reindeer, max_time=2503):
#     time = 0
#     distance = 0
#     while max_time > time:
#         distance += reindeer.speed * reindeer.max_time
#         time += reindeer.max_time

#         if time >= max_time:
#             time -= reindeer.max_time
#             distance -= reindeer.speed * reindeer.max_time
#             for _ in range(reindeer.max_time):
#                 distance += reindeer.speed
#                 time += 1
#                 if time >= max_time:
#                     return distance

#         time += reindeer.rest_time

#     return distance





@click.command()
def cli():
    for _ in range(2503):
        for reindeer in DATA:
            reindeer.move()

        furthest = max([r.distance for r in DATA])
        for r in DATA:
            if r.distance == furthest:
                r.score()

    for r in DATA:
        print(r)


if __name__ == '__main__':
    cli()
