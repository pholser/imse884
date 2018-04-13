import networkx as nx

from vertexcoloring.dimacs.formatter import Formatter


def test_format_clique():
    g = nx.fast_gnp_random_graph(5, 1)

    formatted = Formatter().format(g)

    assert [
        'p edge 5 10',
        'e 0 1',
        'e 0 2',
        'e 0 3',
        'e 0 4',
        'e 1 2',
        'e 1 3',
        'e 1 4',
        'e 2 3',
        'e 2 4',
        'e 3 4'
    ] == formatted.splitlines()
