import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.formulation.representative.problem import Problem


@pytest.fixture
def small_graph():
    return Parser().parse('tests/data/gc_4_1.col')


@pytest.fixture
def small_problem(small_graph):
    return Problem(small_graph, 'lr')


def test_objective(small_problem):
    assert [
        1.0, 0.0, 0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 0.0, 1.0] == small_problem.cx.objective.get_linear()


def test_sense(small_problem):
    assert small_problem.cx.objective.sense.minimize \
           == small_problem.cx.objective.get_sense()


def test_variables(small_problem):
    assert [
        'x0,0', 'x0,2', 'x0,3', 'x0,4',
        'x1,1', 'x1,4',
        'x2,0', 'x2,2', 'x2,3', 'x2,4',
        'x3,0', 'x3,2', 'x3,3',
        'x4,0', 'x4,1', 'x4,2', 'x4,4'
    ] == small_problem.cx.variables.get_names()


def test_lower_bounds(small_problem):
    lowers = small_problem.cx.variables.get_lower_bounds()
    assert all([i == 0.0 for i in lowers])


def test_upper_bounds(small_problem):
    uppers = small_problem.cx.variables.get_upper_bounds()
    assert all([i == 1.0 for i in uppers])


def test_constraint_names(small_problem):
    assert [
        'rep0', 'rep1', 'rep2', 'rep3', 'rep4',
        'uqrep0_3,4',
        'uqrep2_3,4',
        'uqrep4_0,1', 'uqrep4_1,2'
    ] == small_problem.cx.linear_constraints.get_names()


def test_representative_constraint_terms(small_problem):
    pairs = small_problem.cx.linear_constraints.get_rows(
        ['rep0', 'rep1', 'rep2', 'rep3', 'rep4']
    )

    assert [0, 6, 10, 13] == pairs[0].ind
    assert [1.0, 1.0, 1.0, 1.0] == pairs[0].val
    assert [4, 14] == pairs[1].ind
    assert [1.0, 1.0] == pairs[1].val
    assert [1, 7, 11, 15] == pairs[2].ind
    assert [1.0, 1.0, 1.0, 1.0] == pairs[2].val
    assert [2, 8, 12] == pairs[3].ind
    assert [1.0, 1.0, 1.0] == pairs[3].val
    assert [3, 5, 9, 16] == pairs[4].ind
    assert [1.0, 1.0, 1.0, 1.0] == pairs[4].val


def test_representative_constraint_senses(small_problem):
    senses = small_problem.cx.linear_constraints.get_senses(
        ['rep0', 'rep1', 'rep2', 'rep3', 'rep4']
    )

    assert ['G', 'G', 'G', 'G', 'G'] == senses


def test_representative_constraint_right_hand_sides(small_problem):
    rights = small_problem.cx.linear_constraints.get_rhs(
        ['rep0', 'rep1', 'rep2', 'rep3', 'rep4']
    )

    assert [1.0, 1.0, 1.0, 1.0, 1.0] == rights


def test_distinct_representatives_for_neighbors_constraint_terms(small_problem):
    pairs = small_problem.cx.linear_constraints.get_rows(
        [
            'uqrep0_3,4',
            'uqrep2_3,4',
            'uqrep4_0,1', 'uqrep4_1,2'
        ]
    )

    assert [0, 2, 3] == pairs[0].ind
    assert [-1.0, 1.0, 1.0] == pairs[0].val
    assert [7, 8, 9] == pairs[1].ind
    assert [-1.0, 1.0, 1.0] == pairs[1].val
    assert [13, 14, 16] == pairs[2].ind
    assert [1.0, 1.0, -1.0] == pairs[2].val
    assert [14, 15, 16] == pairs[3].ind
    assert [1.0, 1.0, -1.0] == pairs[3].val


def test_adjacent_node_color_constraint_senses(small_problem):
    senses = small_problem.cx.linear_constraints.get_senses(
        [
            'uqrep0_3,4',
            'uqrep2_3,4',
            'uqrep4_0,1', 'uqrep4_1,2'
        ]
    )

    assert ['L', 'L', 'L', 'L'] == senses


def test_adjacent_node_color_constraint_right_hand_sides(small_problem):
    rights = small_problem.cx.linear_constraints.get_rhs(
        [
            'uqrep0_3,4',
            'uqrep2_3,4',
            'uqrep4_0,1', 'uqrep4_1,2'
        ]
    )

    assert [0.0, 0.0, 0.0, 0.0] == rights


@pytest.mark.skip(reason='For manual checks only')
def test_emit(small_problem):
    small_problem.emit_to('/Users/prholser/x.lp')
