import itertools as it

x = [35, 27, 23, 19, 15, 15, 12, 8, 6, 3]

for i in xrange(1, len(x)+1):
    for j in it.combinations(xrange(0, len(x)), i):
        if sum(x[k] for k in j) <= 39 and (3*int(bool(0 in j)) + 2*int(bool(1 in j)) + int(bool(2 in j)) + int(bool(3 in j)) + int(bool(4 in j)) + int(bool(5 in j)) + int(bool(6 in j)) + int(bool(7 in j)) + int(bool(8 in j))) == 3:
            print [k+1 for k in j]

