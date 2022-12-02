import itertools
import pathlib


with open(pathlib.Path().cwd()/'day-01.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

grouped = [list(sub) for ele,sub in itertools.groupby(lines, key=bool) if ele]
calories = [sum([int(y) for y in x]) for x in grouped]
print(max(calories))
print(sum(sorted(calories)[::-1][:3]))
