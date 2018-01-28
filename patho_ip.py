from __future__ import division
from pyomo.environ import *

model = ConcreteModel()
model.indexes = RangeSet(1, 5)
model.x = Var(model.indexes, within=NonNegativeReals, bounds=(0, 1))
model.z = Objective(expr = model.x[1])
model.constraint = Constraint(expr = 2*model.x[1] + 2*model.x[2] + 2*model.x[3] + 2*model.x[4] + 2*model.x[5] == 5)

