"""Exact quota/count tests; synthetic integer matrices are not question data."""
import copy, itertools, json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sampling_quota_check import dimensions, solve_counts
HERE = Path(__file__).resolve().parent

class QuotaTests(unittest.TestCase):
    def design(self):
        return json.loads((HERE/"numina_cot.sampling-design-supplement.json").read_text(encoding="utf-8"))

    def test_current_quota_and_caps_sum_exactly_300(self):
        quota, caps = dimensions(self.design(),json.loads((HERE/"numina_cot.sampling-plan.json").read_text(encoding="utf-8")))
        self.assertEqual(sum(quota.values()),300)
        self.assertEqual(sum(caps.values()),300)
        self.assertEqual(len(quota),21)

    def test_original_ten_unit_deficit_rejected(self):
        v=self.design();v["subject_difficulty_quotas"]["proposed_table"][0]["basic"]-=10
        with self.assertRaises(ValueError):dimensions(v)

    def test_noninteger_and_negative_quotas_rejected(self):
        for n in (True,1.0,-1):
            with self.subTest(n=n):
                v=self.design();v["subject_difficulty_quotas"]["proposed_table"][0]["basic"]=n
                with self.assertRaises(ValueError):dimensions(v)

    def test_repeated_subject_rejected(self):
        v=self.design();v["subject_difficulty_quotas"]["proposed_table"][1]=copy.deepcopy(v["subject_difficulty_quotas"]["proposed_table"][0])
        with self.assertRaises(ValueError):dimensions(v)

    def test_missing_difficulty_rejected(self):
        v=self.design();v["subject_difficulty_quotas"]["proposed_table"][0].pop("basic")
        with self.assertRaises(ValueError):dimensions(v)

    def test_parent_source_cap_mismatch_rejected(self):
        v=self.design();p=json.loads((HERE/"numina_cot.sampling-plan.json").read_text(encoding="utf-8"));p["strata"][0]["first_batch_quota"]-=1
        with self.assertRaises(ValueError):dimensions(v,p)

    def test_parent_revision_mismatch_rejected(self):
        v=self.design();p=json.loads((HERE/"numina_cot.sampling-plan.json").read_text(encoding="utf-8"));p["revision"]="wrong"
        with self.assertRaises(ValueError):dimensions(v,p)

    def test_duplicate_source_rejected(self):
        v=self.design();v["joint_constraints"]["source_caps"].append(v["joint_constraints"]["source_caps"][0])
        with self.assertRaises(ValueError):dimensions(v)

    def matrix(self, values):
        return dict(zip([("a","x","d"),("a","y","d"),("b","x","d"),("b","y","d")],values))

    def test_marginal_supply_is_not_joint_feasibility(self):
        result=solve_counts({("x","d"):1,("y","d"):1},{"a":1,"b":1},self.matrix([1,1,0,0]))
        self.assertFalse(result["feasible"]);self.assertEqual(result["max_assigned"],1)

    def test_augmenting_path_reroutes_initial_choice(self):
        result=solve_counts({("x","d"):1,("y","d"):1},{"a":1,"b":1},self.matrix([1,1,1,0]))
        self.assertTrue(result["feasible"]);self.assertEqual(result["max_assigned"],2)

    def test_full_target_uses_each_source_cap_when_sum_matches(self):
        result=solve_counts({("x","d"):1,("y","d"):1},{"a":1,"b":1},self.matrix([2,2,2,2]))
        self.assertEqual(result["source_used"],{"a":1,"b":1})

    def test_unknown_capacity_is_not_zero(self):
        m=self.matrix([1,1,1,1]);m.pop(("a","x","d"))
        with self.assertRaises(ValueError):solve_counts({("x","d"):1,("y","d"):1},{"a":1,"b":1},m)

    def test_invalid_capacity_types_rejected(self):
        for n in (False,1.0,-1):
            with self.subTest(n=n):
                m=self.matrix([1,1,1,1]);m[("a","x","d")]=n
                with self.assertRaises(ValueError):solve_counts({("x","d"):1,("y","d"):1},{"a":1,"b":1},m)

    def test_zero_quota_cell(self):
        result=solve_counts({("x","d"):0,("y","d"):2},{"a":1,"b":1},self.matrix([2,1,2,1]))
        self.assertTrue(result["feasible"])
        self.assertTrue(all(x["subject"]=="y" for x in result["allocation"]))

    def test_shortage_count_exact(self):
        result=solve_counts({("x","d"):2,("y","d"):2},{"a":1,"b":1},self.matrix([5,5,5,5]))
        self.assertEqual(result["max_assigned"],2)
        self.assertEqual(sum(x["count"] for x in result["unfilled"]),2)

    def test_huge_counts_do_not_round_to_float(self):
        n=10**30+1
        result=solve_counts({("x","d"):n},{"a":n},{("a","x","d"):n})
        self.assertEqual(result["max_assigned"],n)
        self.assertEqual(result["allocation"][0]["count"],n)

    def test_exhaustive_binary_capacity_matrices_against_brute_force(self):
        cells={("x","d"):1,("y","d"):1};caps={"a":1,"b":1}
        for limits in itertools.product((0,1),repeat=4):
            with self.subTest(limits=limits):
                feasible=False
                for allocation in itertools.product((0,1),repeat=4):
                    a,b,c,d=allocation
                    if all(x<=n for x,n in zip(allocation,limits)) and a+b<=1 and c+d<=1 and a+c==1 and b+d==1:
                        feasible=True
                self.assertEqual(solve_counts(cells,caps,self.matrix(limits))["feasible"],feasible)

if __name__=="__main__":unittest.main(verbosity=2)
