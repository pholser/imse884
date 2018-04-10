from networkx.algorithms.operators.unary import complement
from vertexcoloring.formulation.representative.solution import Solution

class LPFormat(object):
    def __init__(self, graph):
        self.graph = graph
        self.antigraph = complement(graph)

    def emit(self):
        lines = []

        self.emit_objective(lines)
        self.emit_constraints(lines)
        self.emit_bounds(lines)
        self.emit_end(lines)

        return "\n".join(lines)

    def emit_objective(self, lines):
        lines.append('Minimize')

    def emit_constraints(self, lines):
        lines.append('Subject To')

    def emit_bounds(self, lines):
        lines.append('Bounds')

    def emit_end(self, lines):
        lines.append('End')

    def solution(self, cplex_solution):
        return Solution(self, cplex_solution)
