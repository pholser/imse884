import time

from decimal import *

start = ''
end = ''
start = time.strftime("%H:%M:%S")

import sys
import cplex
import math
import random

from io import open


################################### Write SIP #########################################

def CreateRandomKnapsackInstance(amatrix, rhs, cost, numbervar, numberrow):

 #create instance
    for i in range (0, numberrow):
        rowcoef=[]
        total=0
        for j in range (0, numbervar):
            aij=random.randint(1,1000)
            rowcoef.append(aij)
            total=total+aij
        rhs.append(int(total/2))
        amatrix.append(rowcoef)

    for j in range (0, numbervar):
        total = 0
        for i in range (0, numberrow):
            total = total + amatrix[i][j]
        cj = int (total)/numberrow +random.randint(1,200)
        cost.append(cj)
    print 'Maximize', cost, '\n Subject to '
    for i in range (0, numberrow):
         print amatrix[i] , ' <= ' , rhs[i]


def WriteKnapsackIP(amatrix, rhs, cost, numbervar,numberrow):
   fp=open(u'mknapsack.lp',u'w')

   a = u'Maximize\n'
   fp.write(a)
   a=''
   cnt=0
   for j in range(0,numbervar):
       a = a + unicode( cost[j]) + u' x'+ unicode(j)+u' + '
       cnt=cnt+1
       if cnt >= 10 and j< numbervar-2 :
          cnt=0
          a=a+u'\n'

   a=a[:len(a)-2]
   a=a+u'\n\n'
   fp.write(a)

#Constraints:
   fp.write(u'\nsubject to\n')
   for i in range (0,numberrow):
       a=''
       cnt=0
       for j in range(0,numbervar):
           a = a + unicode (amatrix[i][j]) +u' x'+ unicode(j)+u' + '
           cnt=cnt+1
           if cnt >= 10 and j< numbervar-2 :
              cnt=0
              a = a+ u'\n'
       a=a[:len(a)-2] + u'<= ' +unicode (rhs[i]) + u'\n'
       fp.write(a)

#Bounds

   fp.write(u'\nBinary\n')
   a=''
   cnt =0
   for i in range(0,numbervar):
       a = a+  u' x'+unicode(i)
       cnt=cnt+1
       if cnt % 10 ==0 and j< numbervar-2:
           a=a+'\n'
           cnt=0
   fp.write(a)

   a=u'\nEnd'
   fp.write(a)
   fp.close()






#MAIN

amatrix = []
rhs = []
cost = []
xsol = []

random.seed(1550)
numbervar=10
numberrow=5
CreateRandomKnapsackInstance(amatrix, rhs, cost, numbervar,numberrow)
WriteKnapsackIP(amatrix, rhs, cost, numbervar,numberrow)


cpx= cplex.Cplex("mKnapsack.lp")
#cpx.parameters.mip.tolerances.absmipgap.set(3.0)
cpx.solve()

z=cpx.solution.get_objective_value()
print 'OBJECTIVE ', z
x= cpx.solution.get_values()
for j in range(0, numbervar):
    print 'x', j , '=', x[j]


#better format,
print 'OBJECTIVE ', z
for j in range(0, numbervar):
    if x[j]<.001:
        xsol.append(0)
    if x[j]>.999:
        xsol.append(1)

a = ''
for j in range(0, numbervar):
    print 'x', j , '=', xsol[j]
print 'OBJECTIVE ', z
for cuts in range (0,5):
    num=0
    indices=[]
    alpha=[]
    beta =[]
    for j in range(0, numbervar):
        if x[j]>.99:
           num+=1
           indices.append(j)
           alpha.append(1.0)
    beta.append(float(num-1))
    print alpha, beta
    cpx.linear_constraints.add(lin_expr=[[indices,alpha]], senses  = ["L"] ,rhs = beta)

    ''' FROM CPLEX DOCUMENTATION WILL ADD MULTIPLE CONSTAINTS AT A TIME
        c = cplex.Cplex()
        c.variables.add(names=["x{0}".format(i+1) for i in range(9)])
        c.linear_constraints.add(lin_expr=[[[0, 1, 2], [1.0, 1.0, 1.0]],
                                           [[3, 4, 5, 6], [1.0, 1.0, 1.0, 1.0]],
                                           [[7, 8], [1.0, 1.0]]],
                                           rhs=[1.0, 1.0, 1.0],
                                           names=["c{0}".format(i+1) for i in range(3)])
    '''

    cpx.solve()
    z=cpx.solution.get_objective_value()
    print 'OBJECTIVE ', z
    x= cpx.solution.get_values()
    a=''
    for j in range(0, numbervar):
        if x[j]>.99:
            a= a+' x'+unicode(j)
    print a
    raw_input()
