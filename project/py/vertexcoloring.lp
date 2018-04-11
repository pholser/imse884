Minimize
color_reps: x1,1 + x2,2 + x3,3 + x4,4
Subject To
rep1: x1,1 + x2,1 >= 1
rep2: x2,2 + x1,2 + x3,2 >= 1
rep3: x3,3 + x2,3 >= 1
rep4: x4,4 >= 1
uqrep2_1,3: x2,1 + x2,3 - x2,2 <= 0
Binary
x1,1 x1,2
x2,1 x2,2 x2,3
x3,2 x3,3
x4,4
End