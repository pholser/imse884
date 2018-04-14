from lp_format import LPFormat
from problem_from_file import ProblemFromFile


class Representative(object):
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
