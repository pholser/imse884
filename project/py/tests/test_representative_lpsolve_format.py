from textwrap import dedent

import pytest

from vertexcoloring.dimacs.parser import Parser
from vertexcoloring.formulation.representative.lp_format import LPFormat


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
        color_reps: x0,0 + x1,1 + x2,2 + x3,3 + x4,4
        Subject To
        rep0: x0,0 + x3,0 + x2,0 + x4,0 >= 1
        rep1: x1,1 + x4,1 >= 1
        rep2: x2,2 + x0,2 + x3,2 + x4,2 >= 1
        rep3: x3,3 + x0,3 + x2,3 >= 1
        rep4: x4,4 + x1,4 + x0,4 + x2,4 >= 1
        uqrep0_3,4: x0,3 + x0,4 - x0,0 <= 0
        uqrep2_3,4: x2,3 + x2,4 - x2,2 <= 0
        uqrep4_1,0: x4,1 + x4,0 - x4,4 <= 0
        uqrep4_1,2: x4,1 + x4,2 - x4,4 <= 0
        Binary
        x0,0 x0,2 x0,3 x0,4
        x1,1 x1,4
        x2,0 x2,2 x2,3 x2,4
        x3,0 x3,2 x3,3
        x4,0 x4,1 x4,2 x4,4
        End
    ''').strip()


def test_format_lr(lp_solve_format_lr):
    assert lp_solve_format_lr == dedent('''
        Minimize
        color_reps: x0,0 + x1,1 + x2,2 + x3,3 + x4,4
        Subject To
        rep0: x0,0 + x3,0 + x2,0 + x4,0 >= 1
        rep1: x1,1 + x4,1 >= 1
        rep2: x2,2 + x0,2 + x3,2 + x4,2 >= 1
        rep3: x3,3 + x0,3 + x2,3 >= 1
        rep4: x4,4 + x1,4 + x0,4 + x2,4 >= 1
        uqrep0_3,4: x0,3 + x0,4 - x0,0 <= 0
        uqrep2_3,4: x2,3 + x2,4 - x2,2 <= 0
        uqrep4_1,0: x4,1 + x4,0 - x4,4 <= 0
        uqrep4_1,2: x4,1 + x4,2 - x4,4 <= 0
        Bounds
        0 <= x0,0 <= 1
        0 <= x0,2 <= 1
        0 <= x0,3 <= 1
        0 <= x0,4 <= 1
        0 <= x1,1 <= 1
        0 <= x1,4 <= 1
        0 <= x2,0 <= 1
        0 <= x2,2 <= 1
        0 <= x2,3 <= 1
        0 <= x2,4 <= 1
        0 <= x3,0 <= 1
        0 <= x3,2 <= 1
        0 <= x3,3 <= 1
        0 <= x4,0 <= 1
        0 <= x4,1 <= 1
        0 <= x4,2 <= 1
        0 <= x4,4 <= 1
        End
    ''').strip()


def test_all_vars(small_graph_format):
    expected = [
        'x0,0', 'x0,2', 'x0,3', 'x0,4',
        'x1,1', 'x1,4',
        'x2,0', 'x2,2', 'x2,3', 'x2,4',
        'x3,0', 'x3,2', 'x3,3',
        'x4,0', 'x4,1', 'x4,2', 'x4,4'
    ]
    assert expected == small_graph_format.all_vars()
