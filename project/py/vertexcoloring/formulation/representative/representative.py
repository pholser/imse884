from vertexcoloring.formulation.representative.lp_format import LPFormat
from vertexcoloring.formulation.representative.problem import Problem


class Representative(object):
    def __init__(self, graph):
        self.graph = graph
        self.format = LPFormat(graph)

    def emit_lpsolve_to(self, path):
        with open(path, 'w') as f:
            f.write(self.format.emit_ip())

    def problem_from_lpsolve(self, path):
        return Problem(self.format, path)
