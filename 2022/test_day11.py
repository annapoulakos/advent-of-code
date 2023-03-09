import importlib

import pytest

module = importlib.import_module('day-11')


@pytest.fixture
def data():
    return [
        'Monkey 0:',
        '  Starting items: 79, 98',
        '  Operation: new = old * 19',
        '  Test: divisible by 23',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 3',
        '',
        'Monkey 1:',
        '  Starting items: 54, 65, 75, 74',
        '  Operation: new = old + 6',
        '  Test: divisible by 19',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 0',
        '',
        'Monkey 2:',
        '  Starting items: 79, 60, 97',
        '  Operation: new = old * old',
        '  Test: divisible by 13',
        '    If true: throw to monkey 1',
        '    If false: throw to monkey 3',
        '',
        'Monkey 3:',
        '  Starting items: 74',
        '  Operation: new = old + 3',
        '  Test: divisible by 17',
        '    If true: throw to monkey 0',
        '    If false: throw to monkey 1',
        '',
    ]

def test_parse_data_is_correct(data):
    # given
    module.reset()

    # when
    module.parse_input(data)

    # then
    assert len(module.MONKEYS) == 4
    assert len(module.MONKEYS[0].items) == 2
    assert module.MONKEYS[0].items.popleft() == 79
    assert module.MONKEYS[0].items.popleft() == 98
    assert module.MONKEYS[0].lhs == 'old'
    assert module.MONKEYS[0].rhs == 19
    assert module.MONKEYS[0].op == '*'
    assert module.MONKEYS[0].divisor == 23
    assert module.MONKEYS[0].truthy == 2
    assert module.MONKEYS[0].falsey == 3

def test_monkey_worry_update_returns_correct_value(data):
    # given
    module.reset()
    module.parse_input(data)
    sample = 20
    monkey0 = module.MONKEYS[0]
    monkey1 = module.MONKEYS[1]
    monkey2 = module.MONKEYS[2]

    # when
    worry0 = monkey0.worry_update(sample)
    worry1 = monkey1.worry_update(sample)
    worry2 = monkey2.worry_update(sample)

    # then
    assert worry0 == 380
    assert worry1 == 26
    assert worry2 == 400

@pytest.mark.parametrize(
    'value,expected',
    [
        (1501,False),
        (460,True)
    ]
)
def test_monkey_is_divisible_returns_correct_value(value, expected, data):
    # given
    module.reset()
    module.parse_input(data)
    monkey = module.MONKEYS[0]

    # when
    actual = monkey.is_divisible(value)

    # then
    assert actual == expected

def test_monkey_throws_to_correct_monkey(data):
    # given
    module.reset()
    module.parse_input(data)
    monkey = module.MONKEYS[0]
    item = monkey.items.popleft()

    # when
    item, target = monkey.throws_to(item)

    # then
    assert target == 3
    assert item == 500

def test_do_round_resolves_correctly(data):
    # given
    module.reset()
    module.parse_input(data)

    # when
    module.do_round()

    # then
    assert module.MONKEYS[0].tolist() == [20, 23, 27, 26]

def test_do_round_twenty_times_resolves_correctly(data):
    # given
    module.reset()
    module.parse_input(data)

    # when
    for _ in range(20):
        module.do_round()

    # then
    assert module.MONKEYS[0].tolist() == [10, 12, 14, 26, 34]

def test_monkey_activity_resolves_correctly(data):
    # given
    module.reset()
    module.parse_input(data)

    # when
    for _ in range(20):
        module.do_round()

    inspections = [monkey.inspections for monkey in module.MONKEYS]

    # then
    assert max(inspections) == 105

def test_part_one_result_is_correct(data):
    # given
    module.reset()
    module.parse_input(data)

    # when
    for _ in range(20):
        module.do_round()

    inspections = [monkey.inspections for monkey in module.MONKEYS]
    first,second = sorted(inspections)[::-1][:2]

    # then
    assert first * second == 10605

def test_exceeding_worry_20_rounds(data):
    # given
    module.reset()
    module.parse_input(data)
    module.EXTRA_WORRY = True

    # when
    for _ in range(20):
        module.do_round()

    inspections = [monkey.inspections for monkey in module.MONKEYS]

    # then
    assert inspections == [99, 97, 8, 103]

# def test_exceeding_worry_2000_rounds(data):
#     # given
#     module.reset()
#     module.parse_input(data)
#     module.EXTRA_WORRY = True

#     # when
#     for _ in range(2000):
#         module.do_round()

#     inspections = [monkey.inspections for monkey in module.MONKEYS]

#     # then
#     assert inspections == [10419,9577,392,10391]
