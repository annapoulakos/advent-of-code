import core.intcode.operations.utils as utils

__operation__ = 'adder.1'

def execute(index, modes, computer):
    params = computer[index:index+4]

    return index, modes, params
