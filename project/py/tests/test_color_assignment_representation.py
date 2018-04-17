import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.colorassignment import Problem


@pytest.fixture
def small_graph():
    return Parser().parse('tests/data/gc_4_1.col')


@pytest.fixture
def small_problem(small_graph):
    return Problem(small_graph, 'lr')


def test_objective(small_problem):
    assert [0.0] * 25 + [1.0] * 5 == small_problem.cx.objective.get_linear()


def test_sense(small_problem):
    assert small_problem.cx.objective.sense.minimize \
           == small_problem.cx.objective.get_sense()


def test_variables(small_problem):
    assert [
        'x0,0', 'x0,1', 'x0,2', 'x0,3', 'x0,4',
        'x1,0', 'x1,1', 'x1,2', 'x1,3', 'x1,4',
        'x2,0', 'x2,1', 'x2,2', 'x2,3', 'x2,4',
        'x3,0', 'x3,1', 'x3,2', 'x3,3', 'x3,4',
        'x4,0', 'x4,1', 'x4,2', 'x4,3','x4,4',
        'w0', 'w1', 'w2', 'w3', 'w4'
    ] == small_problem.cx.variables.get_names()


def test_lower_bounds(small_problem):
    lowers = small_problem.cx.variables.get_lower_bounds()
    assert all([i == 0.0 for i in lowers])


def test_upper_bounds(small_problem):
    uppers = small_problem.cx.variables.get_upper_bounds()
    assert all([i == 1.0 for i in uppers])


def test_constraint_names(small_problem):
    assert [
        'n0', 'n1', 'n2', 'n3', 'n4',
        'e0,1_0', 'e0,1_1', 'e0,1_2', 'e0,1_3', 'e0,1_4',
        'e1,2_0', 'e1,2_1', 'e1,2_2', 'e1,2_3', 'e1,2_4',
        'e1,3_0', 'e1,3_1', 'e1,3_2', 'e1,3_3', 'e1,3_4',
        'e3,4_0', 'e3,4_1', 'e3,4_2', 'e3,4_3', 'e3,4_4',
        's1_0', 's1_1', 's1_2', 's1_3', 's1_4',
        's2_0', 's2_1', 's2_2', 's2_3'
    ] == small_problem.cx.linear_constraints.get_names()


def test_node_getting_color_constraint_terms(small_problem):
    pairs = small_problem.cx.linear_constraints.get_rows(
        ['n0', 'n1', 'n2', 'n3', 'n4']
    )

    assert [0, 1, 2, 3, 4] == pairs[0].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0] == pairs[0].val
    assert [5, 6, 7, 8, 9] == pairs[1].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0] == pairs[1].val
    assert [10, 11, 12, 13, 14] == pairs[2].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0] == pairs[2].val
    assert [15, 16, 17, 18, 19] == pairs[3].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0] == pairs[3].val
    assert [20, 21, 22, 23, 24] == pairs[4].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0] == pairs[4].val


def test_node_getting_color_constraint_senses(small_problem):
    senses = small_problem.cx.linear_constraints.get_senses(
        ['n0', 'n1', 'n2', 'n3', 'n4']
    )

    assert ['E', 'E', 'E', 'E', 'E'] == senses


def test_node_getting_color_constraint_right_hand_sides(small_problem):
    rights = small_problem.cx.linear_constraints.get_rhs(
        ['n0', 'n1', 'n2', 'n3', 'n4']
    )

    assert [1.0, 1.0, 1.0, 1.0, 1.0] == rights


def test_adjacent_node_color_constraint_terms(small_problem):
    pairs = small_problem.cx.linear_constraints.get_rows(
        [
            'e0,1_0', 'e0,1_1', 'e0,1_2', 'e0,1_3', 'e0,1_4',
            'e1,2_0', 'e1,2_1', 'e1,2_2', 'e1,2_3', 'e1,2_4',
            'e1,3_0', 'e1,3_1', 'e1,3_2', 'e1,3_3', 'e1,3_4',
            'e3,4_0', 'e3,4_1', 'e3,4_2', 'e3,4_3', 'e3,4_4'
        ]
    )

    assert [0, 5, 25] == pairs[0].ind
    assert [1.0, 1.0, -1.0] == pairs[0].val
    assert [1, 6, 26] == pairs[1].ind
    assert [1.0, 1.0, -1.0] == pairs[1].val
    assert [2, 7, 27] == pairs[2].ind
    assert [1.0, 1.0, -1.0] == pairs[2].val
    assert [3, 8, 28] == pairs[3].ind
    assert [1.0, 1.0, -1.0] == pairs[3].val
    assert [4, 9, 29] == pairs[4].ind
    assert [1.0, 1.0, -1.0] == pairs[4].val
    assert [5, 10, 25] == pairs[5].ind
    assert [1.0, 1.0, -1.0] == pairs[5].val
    assert [6, 11, 26] == pairs[6].ind
    assert [1.0, 1.0, -1.0] == pairs[6].val
    assert [7, 12, 27] == pairs[7].ind
    assert [1.0, 1.0, -1.0] == pairs[7].val
    assert [8, 13, 28] == pairs[8].ind
    assert [1.0, 1.0, -1.0] == pairs[8].val
    assert [9, 14, 29] == pairs[9].ind
    assert [1.0, 1.0, -1.0] == pairs[9].val
    assert [5, 15, 25] == pairs[10].ind
    assert [1.0, 1.0, -1.0] == pairs[10].val
    assert [6, 16, 26] == pairs[11].ind
    assert [1.0, 1.0, -1.0] == pairs[11].val
    assert [7, 17, 27] == pairs[12].ind
    assert [1.0, 1.0, -1.0] == pairs[12].val
    assert [8, 18, 28] == pairs[13].ind
    assert [1.0, 1.0, -1.0] == pairs[13].val
    assert [9, 19, 29] == pairs[14].ind
    assert [1.0, 1.0, -1.0] == pairs[14].val
    assert [15, 20, 25] == pairs[15].ind
    assert [1.0, 1.0, -1.0] == pairs[15].val
    assert [16, 21, 26] == pairs[16].ind
    assert [1.0, 1.0, -1.0] == pairs[16].val
    assert [17, 22, 27] == pairs[17].ind
    assert [1.0, 1.0, -1.0] == pairs[17].val
    assert [18, 23, 28] == pairs[18].ind
    assert [1.0, 1.0, -1.0] == pairs[18].val
    assert [19, 24, 29] == pairs[19].ind
    assert [1.0, 1.0, -1.0] == pairs[19].val


def test_adjacent_node_color_constraint_senses(small_problem):
    senses = small_problem.cx.linear_constraints.get_senses(
        [
            'e0,1_0', 'e0,1_1', 'e0,1_2', 'e0,1_3', 'e0,1_4',
            'e1,2_0', 'e1,2_1', 'e1,2_2', 'e1,2_3', 'e1,2_4',
            'e1,3_0', 'e1,3_1', 'e1,3_2', 'e1,3_3', 'e1,3_4',
            'e3,4_0', 'e3,4_1', 'e3,4_2', 'e3,4_3', 'e3,4_4'
        ]
    )

    assert ['L', 'L', 'L', 'L', 'L',
            'L', 'L', 'L', 'L', 'L',
            'L', 'L', 'L', 'L', 'L',
            'L', 'L', 'L', 'L', 'L'
            ] == senses


def test_adjacent_node_color_constraint_right_hand_sides(small_problem):
    rights = small_problem.cx.linear_constraints.get_rhs(
        [
            'e0,1_0', 'e0,1_1', 'e0,1_2', 'e0,1_3', 'e0,1_4',
            'e1,2_0', 'e1,2_1', 'e1,2_2', 'e1,2_3', 'e1,2_4',
            'e1,3_0', 'e1,3_1', 'e1,3_2', 'e1,3_3', 'e1,3_4',
            'e3,4_0', 'e3,4_1', 'e3,4_2', 'e3,4_3', 'e3,4_4'
        ]
    )

    assert [0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0] == rights


def test_color_used_only_if_marked_node_constraint_terms(small_problem):
    pairs = small_problem.cx.linear_constraints.get_rows(
        ['s1_0', 's1_1', 's1_2', 's1_3', 's1_4']
    )

    assert [0, 5, 10, 15, 20, 25] == pairs[0].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0, -1.0] == pairs[0].val
    assert [1, 6, 11, 16, 21, 26] == pairs[1].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0, -1.0] == pairs[1].val
    assert [2, 7, 12, 17, 22, 27] == pairs[2].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0, -1.0] == pairs[2].val
    assert [3, 8, 13, 18, 23, 28] == pairs[3].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0, -1.0] == pairs[3].val
    assert [4, 9, 14, 19, 24, 29] == pairs[4].ind
    assert [1.0, 1.0, 1.0, 1.0, 1.0, -1.0] == pairs[4].val


def test_color_used_only_if_marked_node_constraint_senses(small_problem):
    senses = small_problem.cx.linear_constraints.get_senses(
        ['s1_0', 's1_1', 's1_2', 's1_3', 's1_4']
    )

    assert ['G', 'G', 'G', 'G', 'G'] == senses


def test_color_used_only_if_marked_node_constraint_terms_right_hand_sides(small_problem):
    rights = small_problem.cx.linear_constraints.get_rhs(
        ['s1_0', 's1_1', 's1_2', 's1_3', 's1_4']
    )

    assert [0.0, 0.0, 0.0, 0.0, 0.0] == rights


def test_use_lower_numbered_color_first_constraint_terms(small_problem):
    pairs = small_problem.cx.linear_constraints.get_rows(
        ['s2_0', 's2_1', 's2_2', 's2_3']
    )

    assert [25, 26] == pairs[0].ind
    assert [1.0, -1.0] == pairs[0].val
    assert [26, 27] == pairs[1].ind
    assert [1.0, -1.0] == pairs[1].val
    assert [27, 28] == pairs[2].ind
    assert [1.0, -1.0] == pairs[2].val
    assert [28, 29] == pairs[3].ind
    assert [1.0, -1.0] == pairs[3].val


def test_use_lower_numbered_color_first_constraint_senses(small_problem):
    senses = small_problem.cx.linear_constraints.get_senses(
        ['s2_0', 's2_1', 's2_2', 's2_3']
    )

    assert ['G', 'G', 'G', 'G'] == senses


def test_use_lower_numbered_color_first_constraint_terms_right_hand_sides(small_problem):
    rights = small_problem.cx.linear_constraints.get_rhs(
        ['s2_0', 's2_1', 's2_2', 's2_3']
    )

    assert [0.0, 0.0, 0.0, 0.0] == rights


@pytest.mark.skip(reason='For manual checks only')
def test_emit(small_problem):
    small_problem.emit_to('/Users/prholser/x.lp')
