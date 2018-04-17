import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.representative import Problem


@pytest.fixture
def small_graph():
    return Parser().parse('tests/data/7_with_k5.col')


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
    assert 2 == len(clique_cuts)
    assert any([
        [3, 4, 5, 6, 7] == c.clique and 1 == c.node
        for c in clique_cuts
    ])
    assert any([
        [4, 5, 6, 7] == c.clique and 2 == c.node
        for c in clique_cuts
    ])


def test_allows(clique_cuts, small_solution):
    assert not clique_cuts[0].allows(small_solution)
    assert not clique_cuts[1].allows(small_solution)
