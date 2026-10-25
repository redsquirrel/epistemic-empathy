import copy
import json
import math
import tempfile
import unittest
from pathlib import Path

from epistemic_empathy.benchmark import (
    LABELS, build_requests, demo_responses, load_cases, probabilities,
    read_jsonl, score, write_jsonl,
)

ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_cases(ROOT / "data/pilot.jsonl")
        self.requests = build_requests(self.cases)
        self.responses = demo_responses(self.requests)

    def test_pilot_size_and_complete_conditions(self):
        self.assertEqual(len(self.cases), 8)
        self.assertEqual(len(self.requests), 32)
        self.assertEqual(sum(len(r["claims"]) for r in self.requests), 192)

    def test_no_gold_or_unshown_narrative_leaks(self):
        for request in self.requests:
            case = next(c for c in self.cases if c["id"] == request["case_id"])
            serialized = json.dumps(request)
            self.assertNotIn('"gold"', serialized)
            self.assertNotIn('"rationale"', serialized)
            self.assertNotIn('"kind"', serialized)
            user = request["messages"][1]["content"]
            for speaker in "AB":
                self.assertEqual(case[speaker] in user, speaker in request["condition"])

    def test_order_changes_only_narrative_order(self):
        ab, ba = self.requests[2:4]
        self.assertEqual(ab["claims"], ba["claims"])
        self.assertEqual(ab["messages"][0], ba["messages"][0])
        self.assertLess(ab["messages"][1]["content"].index("Narrative A:"),
                        ab["messages"][1]["content"].index("Narrative B:"))
        self.assertGreater(ba["messages"][1]["content"].index("Narrative A:"),
                           ba["messages"][1]["content"].index("Narrative B:"))

    def test_grounded_intervention_preserves_user_evidence(self):
        grounded = build_requests(self.cases, "grounded")
        for left, right in zip(self.requests, grounded):
            self.assertEqual(left["messages"][1], right["messages"][1])
            self.assertNotEqual(left["messages"][0], right["messages"][0])

    def test_serialization_is_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a", Path(tmp) / "b"
            write_jsonl(a, self.requests)
            write_jsonl(b, build_requests(self.cases))
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(read_jsonl(a), self.requests)

    def test_uniform_control_known_brier_and_tie_behavior(self):
        result = score(self.cases, self.requests, self.responses)
        self.assertAlmostEqual(result["overall"]["brier"], 2 / 3)
        self.assertEqual(result["overall"]["accuracy_unique_argmax"], 0)
        self.assertEqual(result["order_total_variation_mean"], 0)
        self.assertEqual(result["new_evidence_probability_gain"], 0)
        self.assertEqual(result["n_new_evidence_comparisons"], 20)

    def test_classwise_reliability_includes_zero_and_one(self):
        result = score(self.cases, self.requests, self.oracle())
        for label in LABELS:
            bins = result["overall"]["classwise_reliability_bins"][label]
            self.assertEqual(sum(b["n"] for b in bins), 192)
            self.assertEqual(bins[-1]["n"], result["overall"]["gold_counts"][label])
            self.assertEqual(bins[-1]["observed_frequency"], 1)
            self.assertEqual(bins[0]["observed_frequency"], 0)

    def test_jsonl_rejects_duplicate_keys_and_nonfinite_constants(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.jsonl"
            for source in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
                path.write_text(source)
                with self.subTest(source=source), self.assertRaises(ValueError):
                    read_jsonl(path)

    def oracle(self):
        # Gold is allowed ONLY in this metric unit test; never a model baseline.
        result = copy.deepcopy(self.responses)
        for request, response in zip(self.requests, result):
            case = next(c for c in self.cases if c["id"] == request["case_id"])
            gold = {c["id"]: c["gold"][request["condition"]] for c in case["claims"]}
            for claim in response["claims"]:
                claim["probabilities"] = {label: float(label == gold[claim["id"]]) for label in LABELS}
        return result

    def test_perfect_metric_fixture(self):
        result = score(self.cases, self.requests, self.oracle())
        self.assertEqual(result["overall"]["brier"], 0)
        self.assertEqual(result["overall"]["accuracy_unique_argmax"], 1)
        self.assertEqual(result["new_evidence_probability_gain"], 1)
        self.assertEqual(result["overall"]["unsupported_motive_support_probability"], 0)

    def test_order_metric_detects_controlled_change(self):
        responses = self.oracle()
        changed = next(r for r in responses if ":BA:" in r["request_id"])
        p = changed["claims"][0]["probabilities"]
        old = max(p, key=p.get)
        new = next(k for k in LABELS if k != old)
        changed["claims"][0]["probabilities"] = {k: float(k == new) for k in LABELS}
        result = score(self.cases, self.requests, responses)
        self.assertAlmostEqual(result["order_total_variation_mean"], 1 / 48)

    def test_always_unknown_is_not_perfect(self):
        result = score(self.cases, self.requests, demo_responses(self.requests, "always-undetermined"))
        self.assertGreater(result["overall"]["brier"], 0)
        self.assertLess(result["overall"]["accuracy_unique_argmax"], 1)

    def test_rejects_invalid_probabilities(self):
        invalid = [
            {"supported": math.nan, "contradicted": 0, "undetermined": 1},
            {"supported": math.inf, "contradicted": 0, "undetermined": 0},
            {"supported": -.1, "contradicted": .1, "undetermined": 1},
            {"supported": True, "contradicted": 0, "undetermined": 0},
            {"supported": .4, "contradicted": .4, "undetermined": .4},
            {"supported": "1", "contradicted": 0, "undetermined": 0},
            {"supported": 1, "contradicted": 0},
        ]
        for p in invalid:
            with self.subTest(p=p), self.assertRaises(ValueError):
                probabilities(p)

    def test_rejects_missing_extra_duplicate_responses(self):
        for changed in (self.responses[:-1], self.responses + [self.responses[0]],
                        self.responses + [{**self.responses[0], "request_id": "foreign"}]):
            with self.subTest(n=len(changed)), self.assertRaises(ValueError):
                score(self.cases, self.requests, changed)

    def test_rejects_missing_extra_duplicate_claims(self):
        for mode in ("missing", "extra", "duplicate"):
            changed = copy.deepcopy(self.responses)
            claims = changed[0]["claims"]
            if mode == "missing":
                claims.pop()
            else:
                claims.append({**claims[0], "id": "foreign" if mode == "extra" else claims[0]["id"]})
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                score(self.cases, self.requests, changed)

    def test_rejects_mixed_variants_and_changed_prompts(self):
        for field in ("variant", "prompt"):
            requests = copy.deepcopy(self.requests)
            if field == "variant":
                requests[0]["variant"] = "grounded"
            else:
                requests[0]["messages"][1]["content"] += "LEAKED ANSWERS"
            with self.subTest(field=field), self.assertRaises(ValueError):
                score(self.cases, requests, self.responses)

    def test_rejects_empty_prose(self):
        self.responses[0]["response"] = " "
        with self.assertRaises(ValueError):
            score(self.cases, self.requests, self.responses)

    def test_rejects_nonfiction_provenance_and_inconsistent_gold(self):
        for mode in ("source", "gold", "duplicate"):
            cases = copy.deepcopy(self.cases)
            if mode == "source":
                cases[0]["provenance"] = "anonymized_client"
            elif mode == "gold":
                cases[0]["claims"][0]["gold"]["BA"] = "contradicted"
            else:
                cases.append(cases[0])
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "data.jsonl"
                write_jsonl(path, cases)
                with self.subTest(mode=mode), self.assertRaises(ValueError):
                    load_cases(path)

    def test_control_labels_guard_against_blanket_uncertainty_and_equal_blame(self):
        causal = self.cases[0]["claims"][-1]
        self.assertEqual(set(causal["gold"].values()), {"supported"})
        boundary = self.cases[-1]
        self.assertEqual(boundary["claims"][3]["gold"]["AB"], "supported")
        self.assertEqual(boundary["claims"][-1]["gold"]["AB"], "contradicted")

    def test_text_absence_is_distinct_from_unavailable_evidence_and_actual_events(self):
        claims = {claim["id"]: claim for case in self.cases for claim in case["claims"]}
        for claim_id, speaker in (("29989694", "A"), ("3a7c047d", "A"), ("4b62ccc6", "B")):
            with self.subTest(claim=claim_id):
                for condition in ("A", "B", "AB", "BA"):
                    self.assertEqual(claims[claim_id]["gold"][condition],
                                     "contradicted" if speaker in condition else "undetermined")
        # The source-text rule must not turn unknown actual events or motives
        # into contradictions merely because the text omits them.
        self.assertEqual(set(claims["9791a140"]["gold"].values()), {"undetermined"})
        self.assertEqual(set(claims["57457681"]["gold"].values()), {"undetermined"})
        self.assertEqual(set(claims["47634250"]["gold"].values()), {"contradicted"})


if __name__ == "__main__":
    unittest.main()
