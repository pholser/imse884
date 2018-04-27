import pytest

from vertexcoloring.dimacs.parser import Parser


@pytest.fixture
def a_parser():
    return Parser()


@pytest.fixture
def small_graph(a_parser):
    return a_parser.parse('tests/data/gc_4_1.col')


@pytest.fixture
def some_disconnected_graph(a_parser):
    return a_parser.parse('tests/data/5_with_2_disconnected.col')


@pytest.fixture
def all_disconnected_graph(a_parser):
    return a_parser.parse('tests/data/10_no_edges.col')


def test_edges(small_graph):
    assert len(small_graph.edges) == 4
    assert small_graph.has_edge(0, 1)
    assert small_graph.has_edge(1, 2)
    assert small_graph.has_edge(1, 3)
    assert small_graph.has_edge(3, 4)


def test_nodes(small_graph):
    assert set(small_graph.nodes) == {0, 1, 2, 3, 4}


def test_some_disconnected(some_disconnected_graph):
    assert set(some_disconnected_graph.nodes()) == {0, 1, 2, 3, 4}
    assert len(some_disconnected_graph.edges()) == 2
    assert some_disconnected_graph.has_edge(0, 1)
    assert some_disconnected_graph.has_edge(0, 2)


def all_disconnected(all_disconnected_graph):
    assert set(some_disconnected_graph.nodes()) == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    assert len(some_disconnected_graph.edges()) == 0
