"""Exact finite-pair population bounds. No dataset reads, labels or sampling side effects."""
from fractions import Fraction
from math import comb
CATEGORIES = ("FP", "TN", "TP", "FN")
CONFIDENCE = Fraction(19, 20)

def integer(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(name + " must be a nonnegative integer")
    return value

def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0

def probability(N, m, K, j):
    return Fraction(choose(K, j) * choose(N - K, m - j), comb(N, m))

def interval(N, m, x, alpha):
    for name, value in (("N", N), ("m", m), ("x", x)):
        integer(value, name)
    if not 0 <= x <= m <= N:
        raise ValueError("require 0 <= x <= m <= N")
    if not isinstance(alpha, Fraction) or not 0 < alpha < 1:
        raise ValueError("alpha must be an exact Fraction in (0,1)")
    feasible = range(x, N - m + x + 1)
    lows = [K for K in feasible if sum(
        (probability(N, m, K, j) for j in range(x, m + 1)), Fraction()) >= alpha]
    highs = [K for K in feasible if sum(
        (probability(N, m, K, j) for j in range(x + 1)), Fraction()) >= alpha]
    return (min(lows), max(highs))

def unrank(N, m, rank):
    for name, value in (("N", N), ("m", m), ("rank", rank)):
        integer(value, name)
    if m > N or rank >= comb(N, m):
        raise ValueError("invalid combination rank")
    result = []
    start = 0
    for slot in range(m):
        for item in range(start, N - (m - slot) + 1):
            block = comb(N - item - 1, m - slot - 1)
            if rank < block:
                result.append(item)
                start = item + 1
                break
            rank -= block
    return tuple(result)

def allocate(capacities, budget):
    integer(budget, "budget")
    if not capacities or any(type(x) is not int or x <= 0 for x in capacities):
        raise ValueError("capacities must be positive integers in canonical layer order")
    count = min(budget, sum(capacities))
    if count < len(capacities):
        return tuple(1 if i < count else 0 for i in range(len(capacities)))
    base = [1] * len(capacities)
    remaining = count - len(capacities)
    residual = [n - 1 for n in capacities]
    denominator = sum(residual)
    if denominator == 0:
        return tuple(base)
    shares = [Fraction(remaining * n, denominator) for n in residual]
    extras = [s.numerator // s.denominator for s in shares]
    order = sorted(range(len(capacities)), key=lambda i: (-(shares[i] - extras[i]), i))
    for i in order[:remaining - sum(extras)]:
        extras[i] += 1
    return tuple(a + b for a, b in zip(base, extras))

def final_bounds(frames):
    """One pre-registered final rule; all nonempty strata of both frames required.
    frames: mapping frame_name -> [{"N": int, "m": int,
      "counts": {"FP": int, "TN": int, "TP": int, "FN": int, "U": int}}, ...].
    Conditional on fixed, correctly adjudicated labels. Does not establish
    exposure, randomization, blindness or gate readiness.
    """
    if set(frames) != {"P1", "P2"} or any(not rows for rows in frames.values()):
        raise ValueError("each registered frame must be nonempty")
    H = sum(len(rows) for rows in frames.values())
    alpha = Fraction(1, 160 * H)
    output = {"confidence": CONFIDENCE, "alpha_per_tail": alpha, "H": H, "frames": {}}
    for name, rows in frames.items():
        totals = {c: [0, 0] for c in CATEGORIES}
        estimates = {c: Fraction() for c in CATEGORIES}
        all_sampled = True
        details = []
        for row in rows:
            N, m = row["N"], row["m"]
            integer(N, "N"); integer(m, "m")
            if N == 0 or m > N:
                raise ValueError("stratum must be nonempty with m <= N")
            if set(row["counts"]) != set(CATEGORIES) | {"U"}:
                raise ValueError("require exactly FP,TN,TP,FN,U")
            counts = row["counts"]
            for c, x in counts.items():
                integer(x, c)
            if sum(counts.values()) != m:
                raise ValueError("all sample outcomes including U must sum to m")
            bounds = {}
            for c in CATEGORIES:
                lo, hi = interval(N, m, counts[c], alpha)
                totals[c][0] += lo
                totals[c][1] += hi
                bounds[c] = (lo, hi)
                if m:
                    estimates[c] += Fraction(N * counts[c], m)
            all_sampled &= m > 0
            details.append({"N": N, "m": m, "bounds": bounds})
        L = {c: totals[c][0] for c in CATEGORIES}
        U = {c: totals[c][1] for c in CATEGORIES}
        negative_known = L["FP"] + L["TN"] > 0
        positive_known = L["TP"] + L["FN"] > 0
        fden = U["FP"] + L["TN"]
        rden = L["TP"] + U["FN"]
        fpr = Fraction(U["FP"], fden) if negative_known and fden else None
        recall = Fraction(L["TP"], rden) if positive_known and rden else None
        ratios = None
        if all_sampled:
            nd = estimates["FP"] + estimates["TN"]
            pd = estimates["TP"] + estimates["FN"]
            ratios = {
                "FPR_HT_ratio": estimates["FP"] / nd if nd else None,
                "Recall_HT_ratio": estimates["TP"] / pd if pd else None,
            }
        output["frames"][name] = {
            "category_total_intervals": totals, "strata": details,
            "FPR_upper": fpr, "Recall_lower": recall,
            "HT_point_estimates": ratios,
            "statistical_criteria_met": fpr is not None and recall is not None
                and fpr <= Fraction(1, 100) and recall >= Fraction(19, 20),
            "scope": "fixed finite adjudicable pair population; prerequisites NOT established",
        }
    output["all_statistical_criteria_met"] = all(
        row["statistical_criteria_met"] for row in output["frames"].values())
    output["gate_accepted"] = False
    return output
