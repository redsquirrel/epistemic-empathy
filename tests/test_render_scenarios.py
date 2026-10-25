import copy
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import unittest

from epistemic_empathy.benchmark import build_requests, load_cases
from experiments.render_scenarios import render

ROOT = Path(__file__).resolve().parents[1]


class TextReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_cases(ROOT / "data/pilot.jsonl")

    def test_all_evidence_and_claims_preserved_without_answer_rationales(self):
        for fmt in ("html", "md"):
            output = render(self.cases, output_format=fmt)
            if fmt == "html":
                reader = TextReader()
                reader.feed(output)
                output = "\n".join(reader.text)
            for case in self.cases:
                for key in ("shared", "A", "B"):
                    self.assertIn(case[key], output)
                for claim in case["claims"]:
                    self.assertIn(claim["text"], output)
                    self.assertNotIn(claim["rationale"], output)
                    self.assertNotIn(claim["id"], output)

    def test_condition_limits_evidence_and_preserves_benchmark_claim_order(self):
        for condition in ("A", "B", "AB", "BA"):
            output = render(self.cases, condition, "html")
            for case in self.cases:
                for speaker in "AB":
                    self.assertEqual(escape(case[speaker]) in output, speaker in condition)
                if len(condition) == 2:
                    self.assertLess(output.index(escape(case[condition[0]])),
                                    output.index(escape(case[condition[1]])))
            for request in build_requests(self.cases):
                if request["condition"] == condition:
                    positions = [output.index("<li>" + escape(c["text"]) + "</li>")
                                 for c in request["claims"]]
                    self.assertEqual(positions, sorted(positions))

    def test_html_does_not_execute_text_as_markup(self):
        cases = copy.deepcopy(self.cases)
        cases[0]["A"] = '<script>alert("test")</script>'
        output = render(cases)
        self.assertNotIn("<script>", output)
        self.assertIn(escape(cases[0]["A"]), output)


if __name__ == "__main__":
    unittest.main()
