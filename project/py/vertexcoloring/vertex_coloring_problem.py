from abc import ABCMeta, abstractmethod


class VertexColoringProblem:
    __metaclass__ = ABCMeta

    @abstractmethod
    def clique_cuts(self):
        pass

    @abstractmethod
    def add_cuts(self, cuts):
        pass

    @abstractmethod
    def suppress_output(self):
        pass

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def emit_to(self, file_path):
        pass
