import importlib

import pytest

module = importlib.import_module('day-10')

@pytest.fixture
def test_case_1():
    return [
        'noop',
        'addx 3',
        'addx -5',
    ]

@pytest.fixture
def test_case_2():
    return [
        'addx 15',
        'addx -11',
        'addx 6',
        'addx -3',
        'addx 5',
        'addx -1',
        'addx -8',
        'addx 13',
        'addx 4',
        'noop',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx -35',
        'addx 1',
        'addx 24',
        'addx -19',
        'addx 1',
        'addx 16',
        'addx -11',
        'noop',
        'noop',
        'addx 21',
        'addx -15',
        'noop',
        'noop',
        'addx -3',
        'addx 9',
        'addx 1',
        'addx -3',
        'addx 8',
        'addx 1',
        'addx 5',
        'noop',
        'noop',
        'noop',
        'noop',
        'noop',
        'addx -36',
        'noop',
        'addx 1',
        'addx 7',
        'noop',
        'noop',
        'noop',
        'addx 2',
        'addx 6',
        'noop',
        'noop',
        'noop',
        'noop',
        'noop',
        'addx 1',
        'noop',
        'noop',
        'addx 7',
        'addx 1',
        'noop',
        'addx -13',
        'addx 13',
        'addx 7',
        'noop',
        'addx 1',
        'addx -33',
        'noop',
        'noop',
        'noop',
        'addx 2',
        'noop',
        'noop',
        'noop',
        'addx 8',
        'noop',
        'addx -1',
        'addx 2',
        'addx 1',
        'noop',
        'addx 17',
        'addx -9',
        'addx 1',
        'addx 1',
        'addx -3',
        'addx 11',
        'noop',
        'noop',
        'addx 1',
        'noop',
        'addx 1',
        'noop',
        'noop',
        'addx -13',
        'addx -19',
        'addx 1',
        'addx 3',
        'addx 26',
        'addx -30',
        'addx 12',
        'addx -1',
        'addx 3',
        'addx 1',
        'noop',
        'noop',
        'noop',
        'addx -9',
        'addx 18',
        'addx 1',
        'addx 2',
        'noop',
        'noop',
        'addx 9',
        'noop',
        'noop',
        'noop',
        'addx -1',
        'addx 2',
        'addx -37',
        'addx 1',
        'addx 3',
        'noop',
        'addx 15',
        'addx -21',
        'addx 22',
        'addx -6',
        'addx 1',
        'noop',
        'addx 2',
        'addx 1',
        'noop',
        'addx -10',
        'noop',
        'noop',
        'addx 20',
        'addx 1',
        'addx 2',
        'addx 2',
        'addx -6',
        'addx -11',
        'noop',
        'noop',
        'noop',
    ]

def test_add_command_sets_queue_correctly_short(test_case_1):
    # given
    module.reset()

    # when
    for command in test_case_1:
        module.add_command(command)

    # then
    assert module.QUEUE.qsize() == 5

def test_process_queue_processes_single_entry_short(test_case_1):
    # given
    module.reset()
    [module.add_command(command) for command in test_case_1]

    # when
    module.process_queue()

    # then
    assert module.CYCLE == 1
    assert module.REGISTER == 1
    assert module.QUEUE.qsize() == 4

def test_process_queue_processes_single_entry_long(test_case_2):
    # given
    module.reset()
    [module.add_command(command) for command in test_case_2]

    # when
    module.process_queue()

    # then
    assert module.CYCLE == 1
    assert module.REGISTER == 1
    assert module.QUEUE.qsize() == 239

def test_short_case_returns_correct_register(test_case_1):
    # given
    module.reset()
    [module.add_command(command) for command in test_case_1]

    # when
    while not module.QUEUE.empty():
        module.process_queue()

    # then
    assert module.CYCLE == 5
    assert module.REGISTER == -1

@pytest.mark.parametrize(
    'cycle,value,expected',
    [
        (20,21,420),
        (60,19,1140),
        (100,18,1800),
        (140,21,2940),
        (180,16,2880),
        (220,18,3960),
    ]
)
def test_long_case_returns_correct_register_per_cycle(cycle, value, expected, test_case_2):
    # given
    module.reset()
    [module.add_command(command) for command in test_case_2]

    # when
    for _ in range(cycle-1):
        module.process_queue()

    actual = cycle * module.REGISTER

    # then
    assert value == module.REGISTER
    assert actual == expected


def test_summation_of_keys_is_correct(test_case_2):
    # given
    module.reset()
    [module.add_command(command) for command in test_case_2]

    # when
    total = module.get_key_values()

    # then
    assert total == 13140

def test_generate_scanline_creates_correct_scanline(test_case_2):
    # given
    module.reset()
    [module.add_command(command) for command in test_case_2]
    expected = ('##..##..##..##..##..##..##..##..##..##..'
        '###...###...###...###...###...###...###.'
        '####....####....####....####....####....'
        '#####.....#####.....#####.....#####.....'
        '######......######......######......####'
        '#######.......#######.......#######.....')

    # when
    scanlines = module.generate_scanlines()

    # then
    assert scanlines == expected
