import pathlib

with open(pathlib.Path().cwd() / 'day-02.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

data = ['B X', 'C Y', 'A Z', 'A X', 'B Y', 'C Z', 'C X', 'A Y', 'B Z']
part_1_score = sum([data.index(line)+1 for line in lines])
print(part_1_score)

data = ['B X', 'C X', 'A X', 'A Y', 'B Y', 'C Y', 'C Z', 'A Z', 'B Z']
part_2_score = sum([data.index(line)+1 for line in lines])
print(part_2_score)
