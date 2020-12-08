import click
from app import helpers

def load_data():
    program_raw = helpers.file_to_lines('inputs', '2020-12-08.txt')

    program = []
    for line in program_raw:
        cmd, _, value = line.partition(' ')
        value = int(value)
        program.append((cmd, value))

    return program

@click.group()
def d8(): pass

@d8.command()
def p1():
    """Day 8, Part 1
    Find the accumulator value immediately before a command is run twice
    """
    program = load_data()
    accumulator = 0
    visited = []
    index = 0

    while index not in visited:
        visited.append(index)

        cmd, value = program[index]

        if cmd == 'jmp':
            index += value
        elif cmd == 'acc':
            accumulator += value
            index += 1
        else:
            index += 1


    print(f'accumulator: {accumulator}')

@d8.command()
def p2():
    """Day 8, Part 2
    change exactly one nop->jmp or jmp->nop to make the program work
    """
    program = load_data()

    try:
        for change in ['nop', 'jmp']:
            cmds = [i for i,(c,_) in enumerate(program) if c == change]

            for cmd in cmds:
                index = 0
                visited = []
                accumulator = 0

                while index not in visited:
                    if index > len(program): break

                    visited.append(index)
                    c,v = program[index]

                    if index == cmd:
                        c = 'nop' if c == 'jmp' else 'jmp'

                    if c == 'jmp':
                        index += v
                    elif c == 'acc':
                        accumulator += v
                        index += 1
                    else:
                        index += 1


    except:
        print(f'accumulator: {accumulator}')
