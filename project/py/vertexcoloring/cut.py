from abc import ABCMeta, abstractmethod


class Cut:
    __metaclass__ = ABCMeta

    @abstractmethod
    def allows(self, solution):
        pass
