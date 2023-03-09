import importlib

import pytest

module = importlib.import_module('day-09')

@pytest.fixture
def instructions():
    return [
        'R 4',
        'U 4',
        'L 3',
        'D 1',
        'R 4',
        'D 1',
        'L 5',
        'R 2',
    ]

@pytest.fixture
def instructions2():
    return [
        'R 5',
        'U 8',
        'L 8',
        'D 3',
        'R 17',
        'D 10',
        'L 25',
        'U 20',
    ]

def test_working():
    assert True == True


@pytest.mark.parametrize(
    'instruction,expected',
    [
        ('R 4', ((0,1), 4)),
        ('L 3', ((0,-1), 3)),
        ('U 2', ((1,0), 2)),
        ('D 5', ((-1,0), 5)),
    ]
)
def test_parse_instruction_parses_correctly(instruction, expected):
    # given

    # when
    result = module.parse_instruction(instruction)

    # then
    assert result == expected

def test_move_ends_with_correct_location_for_head(instructions):
    # given
    expected_head = (2,2)
    head = (0,0)
    tail = (0,0)

    # when
    for instruction in instructions:
        head,tail = module.move(instruction, head, tail)

    # then
    assert head == expected_head

@pytest.mark.parametrize(
    'head,tail,expected',
    [
        ((2,0), (0,0), (1,0)),
        ((-2,0), (0,0), (-1,0)),
        ((0,2), (0,0), (0,1)),
        ((0,-2), (0,0), (0,-1)),
        ((0,0), (0,0), (0,0)),
        ((1,2),(0,0),(1,1)),
        ((2,-1),(0,0),(1,-1)),
        ((-2,1),(0,0),(-1,1)),
        ((-2,-1),(0,0),(-1,-1)),
    ]
)
def test_follow_ends_with_correct_locations(head, tail, expected):
    # given

    # when
    tail = module.follow_head(head, tail)

    # then
    assert tail == expected

def test_move_ends_with_correct_location_for_tail(instructions):
    # given
    expected_tail = (2,1)
    head, tail = (0,0), (0,0)

    # when
    for instruction in instructions:
        head,tail = module.move(instruction, head, tail)

    # then
    assert tail == expected_tail

def test_location_history_returns_unique_visits(instructions):
    # given
    expected = 13
    head, tail = (0,0), (0,0)

    # when
    for instruction in instructions:
        head,tail = module.move(instruction, head, tail)

    # then
    assert len(module.visits) == expected

def test_move_long_ends_with_correct_location_for_tail_small(instructions):
    # given
    expected_tail = (0,0)
    expected_moves = 1
    positions = [(0,0)]*10
    module.visits = set()

    # when
    for instruction in instructions:
        positions = module.move_long(instruction, *positions)

    # then
    assert positions[-1] == expected_tail
    assert len(module.visits) == expected_moves

def test_move_long_ends_with_correct_location_for_tail_large(instructions2):
    # given
    expected_tail = (6, -11)
    expected_visits = 36
    positions = [(0,0)]*10
    module.visits = set()

    # when
    for instruction in instructions2:
        positions = module.move_long(instruction, *positions)

    # then
    assert positions[-1] == expected_tail
    assert len(module.visits) == expected_visits
