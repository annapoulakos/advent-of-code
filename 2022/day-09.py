import operator
import pathlib

with open(pathlib.Path().cwd() / 'day-09.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

visits = set()
visits_list = []

def parse_instruction(instruction):
    direction,_,magnitude = instruction.partition(' ')

    return {
        'R': (0,1),
        'L': (0,-1),
        'U': (1,0),
        'D': (-1,0),
    }.get(direction), int(magnitude)


check = lambda x: list(range(x-1,x+2))


def follow_head(head, tail):
    print(f'{head=} -- {tail=}')
    if head == tail or (head[0] in check(tail[0]) and head[1] in check(tail[1])): return tail
    if head[1] == tail[1]:
        x = 1 if head[0]>tail[0] else -1
        return tail[0]+x, tail[1]
    if head[0] == tail[0]:
        y = 1 if head[1]>tail[1] else -1
        return tail[0],tail[1]+y

    if head[0]>tail[0] and head[1]>tail[1]:
        return tail[0]+1,tail[1]+1

    if head[0]>tail[0] and head[1]<tail[1]:
        return tail[0]+1,tail[1]-1

    if head[0]<tail[0] and head[1]>tail[1]:
        return tail[0]-1,tail[1]+1

    return tail[0]-1,tail[1]-1


def move(instruction, head, tail):
    global visits
    direction,magnitude = parse_instruction(instruction)

    for _ in range(magnitude):
        head = tuple(map(operator.add, head, direction))
        tail = follow_head(head, tail)
        visits.add(tail)

    return head, tail


def move_long(instruction, head, one, two, three, four, five, six, seven, eight, tail):
    global visits
    direction,magnitude = parse_instruction(instruction)

    for _ in range(magnitude):
        head = tuple(map(operator.add, head, direction))
        one = follow_head(head, one)
        two = follow_head(one, two)
        three = follow_head(two, three)
        four = follow_head(three, four)
        five = follow_head(four, five)
        six = follow_head(five, six)
        seven = follow_head(six, seven)
        eight = follow_head(seven, eight)
        tail = follow_head(eight, tail)
        visits.add(tail)
        visits_list.append(tail)

    return [head, one, two, three, four, five, six, seven, eight, tail]

if __name__ == '__main__':
    head, tail = (0,0), (0,0)

    for instruction in lines:
        head, tail = move(instruction, head, tail)

    print(f'{len(visits)=}')
    print(f'{visits=}')

    visits = set()
    positions = [(0,0)]*10
    for instruction in lines:
        postitions = move_long(instruction, *positions)

    print(f'{len(visits)=}')
    print(f'{visits=}')
