import cplex


class Problem(object):
    def __init__(self, format, path):
        self.format = format
        self.cplex = cplex.Cplex(path)

    def solve(self):
        self.cplex.solve()
        return self.format.solution(self.cplex.solution)
