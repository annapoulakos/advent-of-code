import pathlib
import re

with open(pathlib.Path().cwd() / 'day-04.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

# lines = [
#     '2-4,6-8',
#     '2-3,4-5',
#     '5-7,7-9',
#     '2-8,3-7',
#     '6-6,4-6',
#     '2-6,4-8',
# ]

pattern = re.compile(r'(?P<a>\d+)-(?P<b>\d+),(?P<x>\d+)-(?P<y>\d+)')
convert = lambda l: [int(x) for x in pattern.match(l).groups()]
converted = [convert(line) for line in lines]

contains = lambda a,b,x,y: (x>=a and y<= b) or (a>=x and b<=y)
results = [contains(*row) for row in converted]
print(len([x for x in results if x]))

overlaps = lambda a,b,x,y: a<=x<=b or a<=y<=b or x<=a<=y or x<=b<=y
results = [overlaps(*row) for row in converted]
print(len([x for x in results if x]))
