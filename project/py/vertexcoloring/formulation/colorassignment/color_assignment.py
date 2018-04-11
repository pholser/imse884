from vertexcoloring.formulation.colorassignment.lp_format import LPFormat
from vertexcoloring.formulation.colorassignment.problem import Problem


class ColorAssignment(object):
    def __init__(self, graph):
        self.graph = graph
        self.format = LPFormat(graph)

    def emit_ip_to(self, path):
        with open(path, 'w') as f:
            f.write(self.format.emit_ip())

    def problem_from_lpsolve(self, path):
        return Problem(self.format, path)
