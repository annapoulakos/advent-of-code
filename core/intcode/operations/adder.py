"""core.intcode.operations.adder"""
# pylint: disable=invalid-name,logging-format-interpolation

import core.intcode.operations.utils as utils
__operation__ = 'core.intcode.operations.adder'
__opcode__ = '01'

logger = utils.get_logger(__operation__)

def execute(index, modes, computer):
    """Adder executor: returns next index pointer"""
    logger.info(f'executing adder function for {index} and modes {modes}')
    op, left, right, target = computer[index:index+4]

    logger.info(f'params: {op}, {left}, {right}, {target}')

    if modes[0] == '0':
        left = computer[left]
    if modes[1] == '0':
        right = computer[right]

    logger.info(f'setting index [{target}] to value [{left + right}]')
    computer[target] = left + right

    return index + 4
