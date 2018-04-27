from abc import ABCMeta, abstractmethod


class VertexColoringSolution:
    __metaclass__ = ABCMeta

    @abstractmethod
    def objective_value(self):
        pass

    @abstractmethod
    def values(self):
        pass

    @abstractmethod
    def show(self, to):
        pass

    @abstractmethod
    def value_of(self, *variable_names):
        pass

    @abstractmethod
    def is_integer(self):
        pass

    @abstractmethod
    def used_colors(self):
        pass

    @abstractmethod
    def colors_by_node(self):
        pass

    @abstractmethod
    def nodes_by_color(self):
        pass
