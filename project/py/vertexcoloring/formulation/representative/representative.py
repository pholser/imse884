from lp_format import LPFormat
from problem import Problem


class Representative(object):
    def __init__(self, graph):
        self.graph = graph
        self.format = LPFormat(graph)

    def emit_to(self, path, problem_type):
        with open(path, 'w') as f:
            if 'lr' == problem_type:
                f.write(self.format.emit_lr())
            else:
                f.write(self.format.emit_ip())

    def problem_from_file(self, path):
        return Problem(self.format, path)
