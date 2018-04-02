import pytest

from vertexcoloring.dimacs.parser import Parser


@pytest.fixture
def a_parser():
    return Parser()


@pytest.fixture
def small_graph(a_parser):
    return a_parser.parse('tests/data/gc_4_1.col')


def test_edge_count(small_graph):
    assert len(small_graph.edges) == 4
