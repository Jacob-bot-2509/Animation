# -*- coding: utf-8 -*-
"""临时校验脚本:draft-c30-01 重写 scene_spec 的数学一致性(独立复算)。"""
from fractions import Fraction as F

errors = []

def check(name, got, want):
    ok = (got == want)
    print(f"{'OK ' if ok else 'BAD'} {name}: got={got} want={want}")
    if not ok:
        errors.append(name)

# 第三步:代入 x=0
check("(0-1)^3", (0 - 1) ** 3, -1)
check("(0-2)^2", (0 - 2) ** 2, 4)
check("c*(-1)*4 = -4c", F(-1) * 4, -4)
# -4c = 1 -> c = -1/4
check("-4 * (-1/4)", -4 * F(-1, 4), 1)

# 第四步:u=x-1, x-2=u-1
# (u-1)^2 = u^2 - 2u + 1 : 系数 [u^2, u, 1]
def expand_uv(cs):
    # cs = [c0, c1, c2] for u^2, u, const
    return (cs[0], cs[1], cs[2])

check("(u-1)^2 coeffs", expand_uv((1, -2, 1)), (1, -2, 1))
# u^3 * (u^2-2u+1) = u^5 - 2u^4 + u^3
# - (u^5-2u^4+u^3)/4 = -u^5/4 + u^4/2 - u^3/4
def expand_u3():
    # 手动卷积:[u^3] * [u^2, -2u, 1]
    out = {}
    a = {3: 1}
    b = {2: 1, 1: -2, 0: 1}
    for ka, va in a.items():
        for kb, vb in b.items():
            out[ka + kb] = out.get(ka + kb, 0) + va * vb
    return out

conv = expand_u3()
check("u^3*(u^2-2u+1) has u^5 coeff 1", conv.get(5), 1)
check("u^3*(u^2-2u+1) has u^4 coeff -2", conv.get(4), -2)
check("u^3*(u^2-2u+1) has u^3 coeff 1", conv.get(3), 1)
check("u^3*(u^2-2u+1) no other terms", sorted(conv.keys()), [3, 4, 5])

# 逐项除以 -4: -u^5/4 + u^4/2 - u^3/4
check("-u^5/4 coeff", F(-1, 4), F(-1, 4))
check("+u^4/2 coeff", F(2, 4), F(1, 2))  # -(-2u^4)/4 = +2u^4/4 = +u^4/2
check("-u^3/4 coeff", F(-1, 4), F(-1, 4))

# 第五步:验证精确重数
# f = c*(x-1)^3*(x-2)^2, c=-1/4
check("(x-2)^2 at x=1", (1 - 2) ** 2, 1)
check("(x-1)^3 at x=2", (2 - 1) ** 3, 1)
check("c != 0", F(-1, 4) != 0, True)

# 最终形式一致性: -1/4*(x-1)^3*(x-2)^2 与 -1/4*(x-1)^5 + 1/2*(x-1)^4 - 1/4*(x-1)^3
# 用 x 的多项式系数独立验证(手工展开):
# (x-1)^3 = x^3 - 3x^2 + 3x - 1
# (x-2)^2 = x^2 - 4x + 4
# 乘积 = x^5 -7x^4 +19x^3 -25x^2 +16x -4   (逐项乘)
def poly_mul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            out[ka + kb] = out.get(ka + kb, 0) + va * vb
    return out

x3 = {3: 1, 2: -3, 1: 3, 0: -1}
x2 = {2: 1, 1: -4, 0: 4}
prod = poly_mul(x3, x2)
print("(x-1)^3*(x-2)^2 =", {k: prod[k] for k in sorted(prod, reverse=True)})
# f1 = -1/4 * prod
f1 = {k: F(-1, 4) * v for k, v in prod.items()}
# f2 = -1/4*(x-1)^5 + 1/2*(x-1)^4 - 1/4*(x-1)^3
# (x-1)^5 = x^5-5x^4+10x^3-10x^2+5x-1
# (x-1)^4 = x^4-4x^3+6x^2-4x+1
pow5 = {5: 1, 4: -5, 3: 10, 2: -10, 1: 5, 0: -1}
pow4 = {4: 1, 3: -4, 2: 6, 1: -4, 0: 1}
pow3 = {3: 1, 2: -3, 1: 3, 0: -1}
f2 = {}
for k, v in pow5.items():
    f2[k] = f2.get(k, 0) + F(-1, 4) * v
for k, v in pow4.items():
    f2[k] = f2.get(k, 0) + F(1, 2) * v
for k, v in pow3.items():
    f2[k] = f2.get(k, 0) + F(-1, 4) * v
allkeys = set(f1) | set(f2)
same = all(f1.get(k, 0) == f2.get(k, 0) for k in allkeys)
check("两形式系数全等", same, True)
print("f1 coeffs =", {k: f1[k] for k in sorted(f1, reverse=True)})
print("f2 coeffs =", {k: f2[k] for k in sorted(f2, reverse=True)})

# f(0) 应等于 1
f0 = f1.get(0, 0)
check("f(0) = -4c = 1 (c=-1/4)", f0, 1)

# 重数验证:f 中 (x-1) 的重数恰为 3
# f = -1/4*(x-1)^3*(x-2)^2;在 x=1,(x-2)^2=1≠0 → (x-1)^4 ∤ f
# 同理 x=2 处重数恰为 2
print()
print("ALL CHECKS PASSED" if not errors else f"ERRORS: {errors}")
