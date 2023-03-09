import importlib

import pytest

module = importlib.import_module('day-08')

@pytest.fixture
def lines():
    return ['30373','25512','65332','33549','35390']


def test_working():
    assert True == True


def test_matrix_rotate_returns_correct_matrix(lines):
    # given
    expected = [(3,2,6,3,3), (0,5,5,3,5), (3,5,3,5,3), (7,1,3,4,9), (3,2,2,9,0)]

    # when
    result = module.matrix_rotate(module.convert_input(lines))

    # then
    assert expected == result

def test_convert_input_returns_correct_matrix(lines):
    # given
    expected = [(3,0,3,7,3), (2,5,5,1,2), (6,5,3,3,2), (3,3,5,4,9),(3,5,3,9,0)]

    # when
    result = module.convert_input(lines)

    # then
    assert expected == result

@pytest.mark.parametrize(
    'line,expected',
    [
        ((3,0,3,7,3), [True,False,False,True,True]),
        ((2,5,5,1,2), [True,True,True,False,True]),
        ((6,5,3,3,2), [True,True,False,True,True]),
        ((3,3,5,4,9), [True,False,True,False,True]),
        ((3,5,3,9,0), [True,True,False,True,True]),
    ]
)
def test_row_visibility_returns_correct_result(line,expected):
    # given

    # when
    result = module.row_visibility(line)

    # then
    assert expected == result

def test_grid_visibility_returns_correct_matrix(lines):
    # given
    expected = [
        [True,True,True,True,True],
        [True,True,True,False,True],
        [True,True,False,True,True],
        [True,False,True,False,True],
        [True,True,True,True,True],
    ]

    # when
    result = module.grid_visibility(lines)

    # then
    assert expected == result


def test_get_visible_count_returns_correct_count(lines):
    # given
    expected = 21

    # when
    result = module.get_visible_count(lines)

    # then
    assert expected == result

@pytest.mark.parametrize(
    'row,index,expected',
    [
        ([2,5,5,1,2], 2, 2),
        ([6,5,3,3,2], 1, 3),
        ([3,3,5,4,9], 3, 1),
    ]
)
def test_get_cell_score_returns_correct_value(row,index,expected):
    # given

    # when
    result = module.get_cell_score(row, index)

    # then
    assert expected == result


def test_get_scenic_scores_returns_correct_value(lines):
    # given
    expected = [0, 0, 0, 0, 0, 0, 1, 4, 1, 0, 0, 6, 1, 2, 0, 0, 1, 8, 3, 0, 0, 0, 0, 0, 0]

    # when
    result = module.get_scenic_scores(lines)

    # then
    assert expected == result
