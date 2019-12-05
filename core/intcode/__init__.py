import logging
import pathlib
from importlib import import_module

logger = logging.getLogger('intcode:computer')
base_path = pathlib.Path(__file__).parent

class Computer:
    def __init__(self, program, input_value=None):
        self.program = program
        self.input_value = input_value

        # TODO: Load available operations
        self.operations = {}
        filenames = (base_path / 'operations').glob('*.py')
        for filename in filenames:
            if filename.stem in ['__init__', 'utils']:
                continue

            module = import_module(f'core.intcode.operations.{filename.stem}')
            self.operations[module.__operation__] = module.execute


    def __getitem__(self, index):
        return self.program[index]

    def parse_instruction(self, instruction):
        opcode = f'{instruction:0>5}'
        logger.info(f'instruction ({instruction}) -- opcode ({opcode})')

        command = opcode[-2:]
        modes = reversed(opcode[:3])

        return command, list(modes)
