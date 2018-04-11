class Solution(object):
    def __init__(self, format, cplex_solution):
        self.format = format
        self.cplex_solution = cplex_solution

    def objective_value(self):
        return self.cplex_solution.get_objective_value()

    def values(self):
        return {
            v: self.cplex_solution.get_values(v)
            for v in self.format.all_vars()
        }
