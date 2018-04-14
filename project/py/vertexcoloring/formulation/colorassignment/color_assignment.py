from lp_format import LPFormat
from problem import Problem
from problem_from_file import ProblemFromFile


class ColorAssignment(object):
    def __init__(self, graph):
        self.graph = graph
        self.format = LPFormat(graph)

    def emit_to(self, path, solve_as):
        with open(path, 'w') as f:
            if 'lr' == solve_as:
                f.write(self.format.emit_lr())
            else:
                f.write(self.format.emit_ip())

    def problem_from_file(self, path):
        return ProblemFromFile(self.format, path)

    def problem(self, solve_as):
        return Problem(self.graph, solve_as)
