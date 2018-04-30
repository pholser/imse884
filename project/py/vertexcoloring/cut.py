from abc import ABCMeta, abstractmethod

from constraint import Constraint


class Cut(Constraint):
    __metaclass__ = ABCMeta

    @abstractmethod
    def allows(self, solution):
        pass
