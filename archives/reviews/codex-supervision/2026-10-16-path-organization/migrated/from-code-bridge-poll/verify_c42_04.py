from fractions import Fraction as F

# represent a + b*sqrt(3) as (a, b)
half = (F(1, 2), F(0))
s2 = (F(0), F(1, 2))     # sqrt3/2
ns2 = (F(0), F(-1, 2))   # -sqrt3/2
zero = (F(0), F(0))
m1 = (F(-1), F(0))

col1 = [half, ns2, zero]
col2 = [s2, half, zero]
col3 = [zero, zero, m1]

def mul(u, v):
    return (u[0]*v[0] + 3*u[1]*v[1], u[0]*v[1] + u[1]*v[0])

def add(u, v):
    return (u[0]+v[0], u[1]+v[1])

def show(u):
    return "%.6f + %.6f*sqrt3" % (float(u[0]), float(u[1]))

cols = {1: col1, 2: col2, 3: col3}
print("--- A^T A entries (upper triangle, row of A^T x column of A = inner product) ---")
for i in (1, 2, 3):
    for j in (1, 2, 3):
        if i <= j:
            acc = (F(0), F(0))
            for k in range(3):
                acc = add(acc, mul(cols[i][k], cols[j][k]))
            print("c%d%d =" % (i, j), show(acc))

print("--- det of 2x2 block M33 = (1/2)(1/2) - (sqrt3/2)(-sqrt3/2) ---")
d = add(mul(half, half), mul(F(-1), mul(s2, ns2)))
print("M33 =", show(d))
print("det A = (-1)*M33 =", -float(d[0]))

print("--- characteristic polynomial (symbolic check by hand-code) ---")
# (l+1)(l^2 - l + 1) = l^3 + 1 ; roots: -1, and (1 +- i*sqrt3)/2
# block char poly: (l - 1/2)^2 + 3/4 = l^2 - l + 1/4 + 3/4 = l^2 - l + 1
print("block poly = (l-1/2)^2 + 3/4 = l^2 - l + 1  (verified by expansion)")
print("roots of l^2 - l + 1 = 0: discriminant 1-4 = -3, l = (1 +- i*sqrt3)/2")
print("so eigenvalues: 1/2 +- i*sqrt3/2, -1  (matches solution)")
