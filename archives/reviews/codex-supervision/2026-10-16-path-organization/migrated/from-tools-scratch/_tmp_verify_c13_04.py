# -*- coding: utf-8 -*-
"""独立复算 draft-c13-04 场景中出现的每个计算结果。"""
import math

out = []
def chk(name, got, want, tol=1e-9):
    ok = abs(got - want) < tol
    out.append(f"{'PASS' if ok else 'FAIL'} {name}: got={got!r} want={want!r}")
    return ok

N = 5
d = lambda n: math.sqrt(n + 1) - math.sqrt(n)

# 1. 有理化 d_n = 1/(sqrt(n+1)+sqrt n)
for n in (1, 2, 5, 100):
    chk(f"rationalize d_{n}", d(n), 1.0 / (math.sqrt(n + 1) + math.sqrt(n)))

# 2. 通项二阶差分 = d_{n+1}-d_n
for n in (1, 2, 5):
    t = math.sqrt(n + 2) - 2 * math.sqrt(n + 1) + math.sqrt(n)
    chk(f"second diff n={n}", t, d(n + 1) - d(n))

# 3. 递减 d_{n+1}<d_n; 放缩 0<d_n<1/(2 sqrt n)
for n in (1, 2, 5):
    chk(f"decreasing n={n}", d(n + 1) < d(n), True)
    chk(f"bound n={n}", (0 < d(n) < 1.0 / (2 * math.sqrt(n))), True)

# 4. 有限和 S_N = d_{N+1}-d_1 = 1-sqrt2 + 1/(sqrt(N+2)+sqrt(N+1))
SN = sum(d(n + 1) - d(n) for n in range(1, N + 1))
chk("S_5 = d_6-d_1", SN, d(N + 1) - d(1))
chk("S_5 formula", SN, 1 - math.sqrt(2) + 1.0 / (math.sqrt(N + 2) + math.sqrt(N + 1)))
chk("d_{N+1} rationalized", d(N + 1), 1.0 / (math.sqrt(N + 2) + math.sqrt(N + 1)))

# 5. S = 1 - sqrt2
chk("S = 1-sqrt2", 1 - math.sqrt(2), -0.41421356237309515)

# 6. 绝对收敛: sum |t| = d_1 - d_{N+1} -> d_1 = sqrt2-1
A = sum(d(n) - d(n + 1) for n in range(1, N + 1))  # d_n - d_{n+1} > 0
chk("abs partial = d_1-d_{N+1}", A, d(1) - d(N + 1))
chk("abs total = d_1 = sqrt2-1", d(1), math.sqrt(2) - 1)

# 7. 尾项 R_N = S - S_N = -1/(sqrt(N+2)+sqrt(N+1)); |R_N| = d_{N+1}
S = 1 - math.sqrt(2)
R = S - SN
chk("R_5", R, -1.0 / (math.sqrt(N + 2) + math.sqrt(N + 1)))
chk("|R_5| = d_6", abs(R), d(N + 1))

# 8. 对照: S = 1-sqrt2 = -(sqrt2-1)
chk("S = -(abs sum)", S, -(math.sqrt(2) - 1))

print("\n".join(out))
print("ALL PASS" if all(o.startswith("PASS") for o in out) else "SOME FAIL")
