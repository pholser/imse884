import itertools as it
import numpy as np
import sys

cover = tuple(sorted(map(lambda i: int(i) - 1, sys.argv[1:])))

x = [35, 27, 23, 19, 15, 15, 12, 8, 6, 3]
alpha = [2, 2, 1, 1, 1, 1, 1, 1, 1, 0]

def feasible(point):
    return sum(x[i] for i in point) <= 39

def meets_cover(point):
    return sum(alpha[i] * int(bool(i in cover)) for i in point) == 3

vectors = []
for i in xrange(1, len(x)+1):
    for j in it.combinations(xrange(0, len(x)), i):
        if feasible(j) and meets_cover(j):
            vectors.append([int(bool(k in j)) for k in xrange(0, len(x))] + [1])

vectors.sort()

m = np.array(vectors)
print m
print np.linalg.matrix_rank(m)
