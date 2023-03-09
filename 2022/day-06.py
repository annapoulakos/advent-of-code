import pathlib

with open(pathlib.Path().cwd() / 'day-06.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

# lines = [
#     'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
#     'bvwbjplbgvbhsrlpgdmjqwftvncz',
#     'nppdvjthqldpwncqszvftbrmjlhg',
#     'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
#     'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',
# ]
line = lines[0]

fn = lambda l,s: sum([(x if len(l[x:x+s])==len(set(l[x:x+s])) else 0) for x in range(0,len(l)-s)])
print(fn(line,4))
print(fn(line,14))
