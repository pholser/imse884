from textwrap import dedent

import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.formulation.colorassignment.lp_format import LPFormat


@pytest.fixture
def small_graph():
    return Parser().parse('tests/data/gc_4_1.col')


@pytest.fixture
def small_graph_format(small_graph):
    return LPFormat(small_graph)


@pytest.fixture
def lp_solve_format_ip(small_graph_format):
    return small_graph_format.emit_ip()


@pytest.fixture
def lp_solve_format_lr(small_graph_format):
    return small_graph_format.emit_lr()


def test_format_ip(lp_solve_format_ip):
    assert lp_solve_format_ip == dedent('''
        Minimize
        colors_used: w0 + w1 + w2 + w3 + w4
        Subject To
        n0: x0,0 + x0,1 + x0,2 + x0,3 + x0,4 = 1
        n1: x1,0 + x1,1 + x1,2 + x1,3 + x1,4 = 1
        n2: x2,0 + x2,1 + x2,2 + x2,3 + x2,4 = 1
        n3: x3,0 + x3,1 + x3,2 + x3,3 + x3,4 = 1
        n4: x4,0 + x4,1 + x4,2 + x4,3 + x4,4 = 1
        e0,1_0: x0,0 + x1,0 - w0 <= 0
        e0,1_1: x0,1 + x1,1 - w1 <= 0
        e0,1_2: x0,2 + x1,2 - w2 <= 0
        e0,1_3: x0,3 + x1,3 - w3 <= 0
        e0,1_4: x0,4 + x1,4 - w4 <= 0
        e1,2_0: x1,0 + x2,0 - w0 <= 0
        e1,2_1: x1,1 + x2,1 - w1 <= 0
        e1,2_2: x1,2 + x2,2 - w2 <= 0
        e1,2_3: x1,3 + x2,3 - w3 <= 0
        e1,2_4: x1,4 + x2,4 - w4 <= 0
        e1,3_0: x1,0 + x3,0 - w0 <= 0
        e1,3_1: x1,1 + x3,1 - w1 <= 0
        e1,3_2: x1,2 + x3,2 - w2 <= 0
        e1,3_3: x1,3 + x3,3 - w3 <= 0
        e1,3_4: x1,4 + x3,4 - w4 <= 0
        e3,4_0: x3,0 + x4,0 - w0 <= 0
        e3,4_1: x3,1 + x4,1 - w1 <= 0
        e3,4_2: x3,2 + x4,2 - w2 <= 0
        e3,4_3: x3,3 + x4,3 - w3 <= 0
        e3,4_4: x3,4 + x4,4 - w4 <= 0
        Binary
        x0,0 x0,1 x0,2 x0,3 x0,4
        x1,0 x1,1 x1,2 x1,3 x1,4
        x2,0 x2,1 x2,2 x2,3 x2,4
        x3,0 x3,1 x3,2 x3,3 x3,4
        x4,0 x4,1 x4,2 x4,3 x4,4
        w0 w1 w2 w3 w4
        End
    ''').strip()


def test_format_lr(lp_solve_format_lr):
    assert lp_solve_format_lr == dedent('''
        Minimize
        colors_used: w0 + w1 + w2 + w3 + w4
        Subject To
        n0: x0,0 + x0,1 + x0,2 + x0,3 + x0,4 = 1
        n1: x1,0 + x1,1 + x1,2 + x1,3 + x1,4 = 1
        n2: x2,0 + x2,1 + x2,2 + x2,3 + x2,4 = 1
        n3: x3,0 + x3,1 + x3,2 + x3,3 + x3,4 = 1
        n4: x4,0 + x4,1 + x4,2 + x4,3 + x4,4 = 1
        e0,1_0: x0,0 + x1,0 - w0 <= 0
        e0,1_1: x0,1 + x1,1 - w1 <= 0
        e0,1_2: x0,2 + x1,2 - w2 <= 0
        e0,1_3: x0,3 + x1,3 - w3 <= 0
        e0,1_4: x0,4 + x1,4 - w4 <= 0
        e1,2_0: x1,0 + x2,0 - w0 <= 0
        e1,2_1: x1,1 + x2,1 - w1 <= 0
        e1,2_2: x1,2 + x2,2 - w2 <= 0
        e1,2_3: x1,3 + x2,3 - w3 <= 0
        e1,2_4: x1,4 + x2,4 - w4 <= 0
        e1,3_0: x1,0 + x3,0 - w0 <= 0
        e1,3_1: x1,1 + x3,1 - w1 <= 0
        e1,3_2: x1,2 + x3,2 - w2 <= 0
        e1,3_3: x1,3 + x3,3 - w3 <= 0
        e1,3_4: x1,4 + x3,4 - w4 <= 0
        e3,4_0: x3,0 + x4,0 - w0 <= 0
        e3,4_1: x3,1 + x4,1 - w1 <= 0
        e3,4_2: x3,2 + x4,2 - w2 <= 0
        e3,4_3: x3,3 + x4,3 - w3 <= 0
        e3,4_4: x3,4 + x4,4 - w4 <= 0
        Bounds
        0 <= x0,0 <= 1
        0 <= x0,1 <= 1
        0 <= x0,2 <= 1
        0 <= x0,3 <= 1
        0 <= x0,4 <= 1
        0 <= x1,0 <= 1
        0 <= x1,1 <= 1
        0 <= x1,2 <= 1
        0 <= x1,3 <= 1
        0 <= x1,4 <= 1
        0 <= x2,0 <= 1
        0 <= x2,1 <= 1
        0 <= x2,2 <= 1
        0 <= x2,3 <= 1
        0 <= x2,4 <= 1
        0 <= x3,0 <= 1
        0 <= x3,1 <= 1
        0 <= x3,2 <= 1
        0 <= x3,3 <= 1
        0 <= x3,4 <= 1
        0 <= x4,0 <= 1
        0 <= x4,1 <= 1
        0 <= x4,2 <= 1
        0 <= x4,3 <= 1
        0 <= x4,4 <= 1
        0 <= w0 <= 1
        0 <= w1 <= 1
        0 <= w2 <= 1
        0 <= w3 <= 1
        0 <= w4 <= 1
        End
    ''').strip()


def test_all_vars(small_graph_format):
    expected = [
        'x0,0', 'x0,1', 'x0,2', 'x0,3', 'x0,4',
        'x1,0', 'x1,1', 'x1,2', 'x1,3', 'x1,4',
        'x2,0', 'x2,1', 'x2,2', 'x2,3', 'x2,4',
        'x3,0', 'x3,1', 'x3,2', 'x3,3', 'x3,4',
        'x4,0', 'x4,1', 'x4,2', 'x4,3', 'x4,4',
        'w0', 'w1', 'w2', 'w3', 'w4'
    ]
    assert expected == small_graph_format.all_vars()
