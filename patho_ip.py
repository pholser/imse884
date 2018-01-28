from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory

def z(model):
    return model.x[1]

def cx(model):
    return 2*summation(model.x) == 5

opt = SolverFactory('cplex')

model = ConcreteModel()
model.n = 5
model.indexes = RangeSet(1, model.n)
model.x = Var(model.indexes, within=NonNegativeReals, bounds=(0, 1))
model.z = Objective(rule=z)
model.constraints = ConstraintList()
model.constraints.add(2*summation(model.x) == 5)

results = opt.solve(model)
model.display()

