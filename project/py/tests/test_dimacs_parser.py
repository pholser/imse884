import pytest

from vertexcoloring.dimacs.parser import Parser


@pytest.fixture
def a_parser():
    return Parser()


@pytest.fixture
def small_graph(a_parser):
    return a_parser.parse('tests/data/gc_4_1.col')


def test_edges(small_graph):
    assert len(small_graph.edges) == 4
    assert small_graph.has_edge('0', '1')
    assert small_graph.has_edge('1', '2')
    assert small_graph.has_edge('1', '3')
    assert small_graph.has_edge('3', '4')


def test_nodes(small_graph):
    assert set(small_graph.nodes) == {'0', '1', '2', '3', '4'}
