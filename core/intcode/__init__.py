import logging
import pathlib
from importlib import import_module
from types import SimpleNamespace

logger = logging.getLogger('intcode:computer')
base_path = pathlib.Path(__file__).parent

OperationModes = SimpleNamespace(
    POSITION='0',
    IMMEDIATE='1',
)

class Computer:
    def __init__(self, program, input_value=None):
        self.program = program
        self.input_value = input_value

        # TODO: Load available operations
        self.operations = []
        filenames = (base_path / 'operations').glob('*.py')
        for filename in filenames:
            if filename.stem in ['__init__', 'utils']:
                continue

            module = import_module(f'core.intcode.operations.{filename.stem}')
            self.operations.append(module)


    def __getitem__(self, index):
        return self.program[index]

    def __setitem__(self, index, value):
        self.program[index] = value

    def value_by_mode(self, value, mode):
        return {
            OperationModes.POSITION: self[value],
            OperationModes.IMMEDIATE: value,
        }.get(mode, None)

    def parse_instruction(self, instruction):
        opcode = f'{instruction:0>5}'
        logger.info(f'instruction ({instruction}) -- opcode ({opcode})')

        command = opcode[-2:]
        modes = reversed(opcode[:3])

        return command, list(modes)

    def get_operation(self, command):
        return next((op for op in self.operations if op.__opcode__ == command), None)
