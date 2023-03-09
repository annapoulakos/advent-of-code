import pathlib
import queue

with open(pathlib.Path().cwd() / 'day-10.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

REGISTER:int = 1
CYCLE:int = 0
QUEUE:queue.SimpleQueue = queue.SimpleQueue()

def reset():
    global REGISTER, CYCLE, QUEUE
    REGISTER = 1
    CYCLE = 0
    QUEUE = queue.SimpleQueue()

def process_queue():
    global REGISTER, QUEUE, CYCLE

    if QUEUE.empty(): return

    value = QUEUE.get(block=False)
    REGISTER += value
    CYCLE += 1

def add_command(command):
    global QUEUE

    cmd,_,value = command.partition(' ')
    if cmd == 'noop':
        QUEUE.put(0)
    else:
        QUEUE.put(0)
        QUEUE.put(int(value))

def get_key_values():
    global REGISTER
    total = 0

    for x in range(1, 221):
        if x in [20,60,100,100,140,180,220]:
            total += (REGISTER * x)

        process_queue()

    return total

def generate_scanlines():
    global QUEUE, REGISTER, CYCLE
    scanlines = ''

    while not QUEUE.empty():
        if (REGISTER-1)<=(CYCLE%40)<=(REGISTER+1):
            scanlines += '#'
        else:
            scanlines += '.'
        process_queue()

    return scanlines

if __name__ == '__main__':
    reset()
    [add_command(command) for command in lines]

    print(f'{get_key_values()=}')

    reset()
    [add_command(command) for command in lines]
    scanlines = generate_scanlines()
    print(''.join(scanlines[i:i+40]+'\n' for i in range(0,len(scanlines), 40)))
