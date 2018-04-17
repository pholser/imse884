import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.colorassignment import Problem


@pytest.fixture
def small_graph():
    return Parser().parse('tests/data/gc_4_triangle.col')


@pytest.fixture
def small_problem(small_graph):
    return Problem(small_graph, 'lr')


@pytest.fixture
def small_solution(small_problem):
    return small_problem.solve()


@pytest.fixture
def clique_cuts(small_problem):
    return [c for c in small_problem.clique_cuts()]


def test_clique_cuts(clique_cuts):
    assert 4 == len(clique_cuts)
    assert all([[1, 3, 4] == c.clique for c in clique_cuts])
    assert {1, 2, 3, 4} == {c.color for c in clique_cuts}


def test_allows(clique_cuts, small_solution):
    assert not clique_cuts[0].allows(small_solution)
    assert not clique_cuts[1].allows(small_solution)
    assert not clique_cuts[2].allows(small_solution)
    assert clique_cuts[3].allows(small_solution)
