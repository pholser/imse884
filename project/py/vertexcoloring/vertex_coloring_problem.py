import cplex

from abc import ABCMeta, abstractmethod


class VertexColoringProblem:
    __metaclass__ = ABCMeta

    def __init__(self, solve_as):
        self.cx = cplex.Cplex()
        self.solve_as = solve_as

    def set_sense_minimize(self):
        self.cx.objective.set_sense(self.cx.objective.sense.minimize)

    def set_objective(self, coefficients, var_names):
        if 'ip' == self.solve_as:
            self.cx.variables.add(
                obj=coefficients,
                types=[self.cx.variables.type.binary] * len(var_names),
                names=var_names
            )
        else:
            self.cx.variables.add(
                obj=coefficients,
                ub=[1.0] * len(var_names),
                names=var_names
            )

    def add_constraints(self, constraints):
        self.cx.linear_constraints.add(
            lin_expr=map(lambda c: c.terms(), constraints),
            senses=map(lambda c: c.sense(), constraints),
            rhs=map(lambda c: c.rhs(), constraints),
            names=map(lambda c: c.name(), constraints)
        )

    def suppress_output(self):
        self.cx.set_log_stream(None)
        self.cx.set_error_stream(None)
        self.cx.set_warning_stream(None)
        self.cx.set_results_stream(None)

    def emit_to(self, path):
        self.cx.write(path, 'lp')

    def cplex_solve(self):
        start = self.cx.get_dettime()
        self.cx.solve()
        end = self.cx.get_dettime()
        return self.cx.solution, end - start

    @abstractmethod
    def clique_cuts(self):
        pass

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def all_vars(self):
        pass
