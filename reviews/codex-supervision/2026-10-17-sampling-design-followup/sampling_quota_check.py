"""Integer quota validation/feasibility only. No data acquisition or selection."""
from collections import deque
from pathlib import Path
import argparse, hashlib, json

def integer(n):
    if type(n) is not int or n < 0:
        raise ValueError("Nonnegative integer required; bool/float refused")
    return n

def dimensions(design, parent=None):
    levels = design["difficulty_taxonomy"]["proposed_levels"]
    subjects = design["subject_taxonomy"]["proposed_subjects"]
    if not levels or len(set(levels)) != len(levels) or not subjects or len(set(subjects)) != len(subjects):
        raise ValueError("Missing or repeated categories")
    rows = design["subject_difficulty_quotas"]["proposed_table"]
    if len(rows) != len(subjects) or {x["subject"] for x in rows} != set(subjects):
        raise ValueError("Subject coverage mismatch")
    if len({x["subject"] for x in rows}) != len(rows):
        raise ValueError("Repeated subject row")
    quota = {}
    for row in rows:
        if set(row) != {"subject", *levels}:
            raise ValueError("Difficulty coverage mismatch")
        for level in levels:
            quota[(row["subject"], level)] = integer(row[level])
    target = integer(design["subject_difficulty_quotas"]["target_total"])
    if target == 0 or sum(quota.values()) != target:
        raise ValueError("Quota sum differs from target")
    caps = {}
    for row in design["joint_constraints"]["source_caps"]:
        key = row["source"]
        if not isinstance(key, str) or not key or key in caps:
            raise ValueError("Invalid/repeated source")
        caps[key] = integer(row["cap"])
    if not caps or sum(caps.values()) < target:
        raise ValueError("Source caps cannot supply target")
    if parent is not None:
        expected = {x["source"]: x["first_batch_quota"] for x in parent["strata"]}
        if len(expected) != len(parent["strata"]) or caps != expected or parent["first_batch_total"] != target:
            raise ValueError("Parent plan binding mismatch")
    if design.get("execution_ready") is not False:
        raise ValueError("Design must not enable sampling")
    return quota, caps

def solve_counts(quota, caps, capacities):
    """Max-flow on disjoint, already eligible representative-family counts."""
    cells = list(quota); sources = list(caps)
    for x in quota.values(): integer(x)
    for x in caps.values(): integer(x)
    expected = {(s, *cell) for s in sources for cell in cells}
    if set(capacities) != expected:
        raise ValueError("Complete capacity matrix required; missing is not zero")
    for x in capacities.values(): integer(x)
    first_source = 1; first_cell = 1 + len(sources)
    sink = first_cell + len(cells); graph = [[] for _ in range(sink + 1)]; residual = {}
    def edge(u, v, n):
        graph[u].append(v); graph[v].append(u)
        residual[(u, v)] = n; residual[(v, u)] = 0
    for i, s in enumerate(sources): edge(0, first_source + i, caps[s])
    for j, cell in enumerate(cells): edge(first_cell + j, sink, quota[cell])
    for i, s in enumerate(sources):
        for j, cell in enumerate(cells): edge(first_source+i, first_cell+j, capacities[(s, *cell)])
    flow = 0; target = sum(quota.values())
    while flow < target:
        parent = {0: None}; queue = deque([0])
        while queue and sink not in parent:
            u = queue.popleft()
            for v in graph[u]:
                if v not in parent and residual[(u, v)] > 0:
                    parent[v] = u; queue.append(v)
        if sink not in parent: break
        delta = target - flow; v = sink
        while parent[v] is not None:
            u = parent[v]; delta = min(delta, residual[(u, v)]); v = u
        v = sink
        while parent[v] is not None:
            u = parent[v]; residual[(u, v)] -= delta; residual[(v, u)] += delta; v = u
        flow += delta
    allocated = {(s, *cell): capacities[(s, *cell)]-residual[(first_source+i, first_cell+j)]
                 for i, s in enumerate(sources) for j, cell in enumerate(cells)}
    source_used = {s: sum(allocated[(s, *cell)] for cell in cells) for s in sources}
    missing = {cell: quota[cell] - sum(allocated[(s, *cell)] for s in sources) for cell in cells}
    return {"scope": "COUNTS_FEASIBILITY_ONLY_NO_QUESTION_SELECTION", "target": target,
            "max_assigned": flow, "feasible": flow == target, "source_used": source_used,
            "unfilled": [{"subject": c[0], "difficulty": c[1], "count": n} for c, n in missing.items() if n],
            "allocation": [{"source": s, "subject": c[0], "difficulty": c[1], "count": allocated[(s,*c)]}
                           for s in sources for c in cells if allocated[(s,*c)]]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--design", type=Path, required=True)
    ap.add_argument("--parent-plan", type=Path, required=True)
    ap.add_argument("--capacities", type=Path)
    args = ap.parse_args()
    raw = args.parent_plan.read_bytes()
    design = json.loads(args.design.read_text(encoding="utf-8"))
    if hashlib.sha256(raw).hexdigest() != design["parent_plan_sha256"]:
        raise ValueError("Parent file SHA mismatch")
    quota, caps = dimensions(design, json.loads(raw))
    out = {"scope": "DESIGN_SCHEMA_ONLY", "quota_sum": sum(quota.values()),
           "source_cap_sum": sum(caps.values()), "cells": len(quota), "execution_ready": False,
           "capacity_status": "PENDING_REAL_ELIGIBLE_FAMILY_COUNTS"}
    if args.capacities:
        rows = json.loads(args.capacities.read_text(encoding="utf-8"))
        capacities = {(x["source"],x["subject"],x["difficulty"]): x["eligible_family_count"] for x in rows}
        if len(capacities) != len(rows): raise ValueError("Duplicate capacity cell")
        out["counts_feasibility"] = solve_counts(quota, caps, capacities)
        out["capacity_status"] = "COUNTS_ONLY_NOT_INDEPENDENT_EVIDENCE_ACCEPTANCE"
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
