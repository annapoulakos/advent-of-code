import pathlib

with open(pathlib.Path().cwd() / 'day-03.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

# lines = [
#     'vJrwpWtwJgWrhcsFMMfFFhFp',
#     'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
#     'PmmdzqPrVvPwwTWBwg',
#     'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
#     'ttgJtRGJQctTZtZT',
#     'CrZsJsPPZsGzwwsLwLmpwMDw',
# ]

convert = lambda l: ord(l) - 38 if ord(l)<97 else ord(l)-96

def chunk(l,n):
    for i in range(0,len(l), n):
        yield l[i:i+n]

results = []

for line in lines:
    left,right = line[slice(0,len(line)//2)], line[slice(len(line)//2, len(line))]
    results.append([convert(l) for l in set(left) if l in right][0])
print(sum(results))

groups = list(chunk(lines, 3))
group_results = []
for a,b,c in groups:
    letters = set().union(*(a+b+c))
    group_results.append([convert(l) for l in set(a) if l in b and l in c][0])
print(sum(group_results))
