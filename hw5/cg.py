import sys
from fractions import Fraction
from itertools import permutations
from math import floor


class CGCut(object):
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def __add__(self, other):
        return CGCut(
            tuple(
                self.coefficients[i] + other.coefficients[i]
                for i in xrange(0, len(self.coefficients))
            )
        )

    def __mul__(self, u):
        return CGCut(
            tuple(c * u for c in self.coefficients)
        )

    def equivalent_to(self, target):
        return tuple(int(floor(c)) for c in self.coefficients) == target

    def __repr__(self):
        return str(self.coefficients)


if __name__ == '__main__':
    a = CGCut((4, 1, 28))
    b = CGCut((1, 4, 27))
    c = CGCut((1, -1, 1)) 
    cuts = [a, b, c]
    target = (1, 2, 15)

    while True:
        for a, b, c in permutations(cuts, 3):
            for n1 in xrange(0, 6):
                u1 = Fraction(n1, 6)
                print u1
                print len(cuts)

                for n2 in xrange(0, 6):
                    u2 = Fraction(n2, 6)

                    for n3 in xrange(0, 6):
                        u3 = Fraction(n3, 6)

                        abc = a * u1 + b * u2 + c * u3
                        if abc.equivalent_to(target):
                            print u1
                            print u2
                            print u3
                            print abc
                            exit(0)
                        cuts.append(abc)

