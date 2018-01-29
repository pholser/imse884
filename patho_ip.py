from __future__ import division
import heapq as q
from ostruct import OpenStruct
from pyomo.environ import *
from pyomo.opt import SolverFactory

class Node:
    def __init__(self, solution):
        self.z = solution.z()
        self.x = [solution.x[i]() for i in xrange(1, len(solution.x) + 1)]

    def is_integer(self):
        return all([v.is_integer() for v in self.x])

    def branching_var(self):
        return next(i for i, v in enumerate(self.x) if not v.is_integer()) + 1

    def __str__(self):
        return "z = %f, x = %s" % (self.z, self.x)

    def __repr__(self):
        return self.__str__()

nil_node = OpenStruct()
nil_node.z = -float('inf')

class BranchAndBound:
    def __init__(self, problem):
        self.problem = problem
        self.opt = SolverFactory('cplex')

    def solve(self):
        z_star = -float('inf')
        candidates = []
        processed_nodes = []
        best = nil_node 

        root_result = self.opt.solve(self.problem)
        root = Node(self.problem)
        q.heappush(candidates, (-root.z, root))

        while len(candidates) > 0:
            candidate = q.heappop(candidates)[1]
            if candidate.is_integer():
                print candidate, "is integer"
                if candidate.z > best.z:
                    print candidate, "is better than", best
                    best = candidate
                else:
                    print "fathom", candidate
            else:
                print candidate, "is not integer"
                if candidate.z >= best.z:
                    print candidate, "is better than", best
                else:
                    print "fathom", candidate

            processed_nodes.append(candidate)
 
        return processed_nodes

def z(model):
    return model.x[1]

def model_instance():
    model = AbstractModel()
    model.n = 5
    model.x = Var(RangeSet(model.n), within=NonNegativeReals, bounds=(0, 1))
    model.z = Objective(rule=z)
    model.constraints = ConstraintList()
    instance = model.create_instance()
    instance.constraints.add(2*summation(instance.x) == instance.n)
    return instance

branch_and_bound = BranchAndBound(model_instance())
print branch_and_bound.solve()
