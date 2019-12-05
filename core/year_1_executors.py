import core.functions as functions
import core.intcode as ic

import logging
logging.basicConfig(level=logging.INFO)
def aoc_1_1_1(**kwargs):
    instructions = [1,2,3, 101, 1001]

    pc = ic.Computer(instructions)

    for instruction in instructions:
        print(pc.parse_instruction(instruction))

def aoc_1_1_2(**kw):
    program = list(range(10))
    pc = ic.Computer(program)

    print(pc[1:3])
    print(pc[3:7])

def aoc_1_1_3(**kw):
    program = [1,2,3,4,5,6,7]
    pc = ic.Computer(program)

    fn = pc.operations['adder.1']

    i,m,p = fn(2, [0,1], pc)
    print(i,m,p)
