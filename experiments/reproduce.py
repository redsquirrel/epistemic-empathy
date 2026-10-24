"""Reproduce offline controls. No network, credentials, or external dependencies."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from epistemic_empathy.benchmark import (  # noqa: E402
    build_requests, demo_responses, load_cases, provenance, score, write_jsonl,
)


def main():
    cases = load_cases(ROOT / "data/pilot.jsonl")
    report = {"status": "ENGINEERING CONTROLS ONLY; NO LLM EVALUATED",
              "runs": []}
    for variant in ("baseline", "grounded"):
        requests = build_requests(cases, variant)
        folder = ROOT / "work/demo" / variant
        request_path = folder / "requests.jsonl"
        write_jsonl(request_path, requests)
        for strategy in ("uniform", "always-undetermined"):
            responses = demo_responses(requests, strategy)
            response_path = folder / (strategy + ".jsonl")
            write_jsonl(response_path, responses)
            result = score(cases, requests, responses)
            result["strategy"] = strategy
            result["provenance"] = provenance({"data": ROOT / "data/pilot.jsonl",
                                                "requests": request_path,
                                                "responses": response_path})
            report["runs"].append(result)
    target = ROOT / "results/demo-summary.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print("Reproduced 4 offline controls; raw artifacts in work/demo; summary in results/.")


if __name__ == "__main__":
    main()
