import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.colorassignment import Problem


@pytest.fixture
def small_graph():
    return Parser().parse('tests/data/gc_4_1.col')


@pytest.fixture
def small_problem(small_graph):
    problem = Problem(small_graph, 'lr')
    problem.suppress_output()
    return problem


@pytest.fixture
def small_solution(small_problem):
    return small_problem.solve()


def test_objective(small_solution):
    assert 2.0 == small_solution.objective_value()


def test_color_markings(small_solution):
    used_colors = small_solution.used_colors()
    assert small_solution.objective_value() == len(used_colors)

    node_colors = small_solution.colors_by_node()
    assert set(used_colors) == set(node_colors.values())

    by_color = small_solution.nodes_by_color()
    color_classes = by_color.values()
    assert [0, 2, 3] in color_classes
    assert [1, 4] in color_classes
