from abc import ABCMeta, abstractmethod


class Constraint:
    __metaclass__ = ABCMeta

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def terms(self):
        pass

    @abstractmethod
    def rhs(self):
        pass

    @abstractmethod
    def sense(self):
        pass
