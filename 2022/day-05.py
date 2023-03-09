from collections import deque
import itertools
import pathlib
import re

with open(pathlib.Path().cwd() / 'day-05.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

# lines = [
#     '    [D]    ',
#     '[N] [C]    ',
#     '[Z] [M] [P]',
#     ' 1   2   3 ',
#     '',
#     'move 1 from 2 to 1',
#     'move 3 from 1 to 3',
#     'move 2 from 2 to 1',
#     'move 1 from 1 to 2',
# ]

layout,instructions = [list(sub) for ele,sub in itertools.groupby(lines, key=bool) if ele]
identifiers = [int(x) for x in layout[-1].split(' ') if x]
stacks = [deque() for _ in identifiers]
keys = [x for x in range(1,4*len(identifiers)+1, 4)]

for line in layout[::-1][1:]:
    for key in identifiers:
        value = line[keys[key-1]]
        if value != ' ':
            stacks[key-1].append(value)
list_stacks = [list(stack) for stack in stacks]

pattern = re.compile(r'move (?P<mv>\d+) from (?P<src>\d+) to (?P<dst>\d+)')

for instruction in instructions:
    ins = pattern.match(instruction).groupdict()
    for x in range(0,int(ins['mv'])):
        ele = stacks[int(ins['src'])-1].pop()
        stacks[int(ins['dst'])-1].append(ele)

letters = [s.pop() for s in stacks]
print(''.join(letters))


for instruction in instructions:
    ins = pattern.match(instruction).groupdict()
    mov, src, dst = -1*int(ins['mv']), int(ins['src'])-1, int(ins['dst'])-1
    list_stacks[src], to_move = list_stacks[src][:mov], list_stacks[src][mov:]
    list_stacks[dst] += to_move

letters = [s[-1] for s in list_stacks]
print(''.join(letters))
