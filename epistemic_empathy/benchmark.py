"""Dependency-free, offline benchmark construction and scoring."""

import hashlib
import json
import math
import platform
from collections import Counter
from pathlib import Path
from statistics import mean

LABELS = ("supported", "contradicted", "undetermined")
CONDITIONS = ("A", "B", "AB", "BA")
# The bare task. Reasoning guidance stays out of what models see, so scores reflect
# the model's own judgment; the human label rules live in data/README.md.
SYSTEM = """You will read a short fictional situation involving two adult partners, A and B. It includes shared facts, which are true for this exercise, and an account from one or both partners. Then you will see a list of claims.

Judge each claim using only the material shown:
- supported: the material shown supports the claim
- contradicted: the material shown contradicts the claim
- undetermined: the material shown does not settle it

Give your answer for each claim as probabilities for the three labels.

Also write a brief reply (60–120 words) to the person or people whose accounts are shown.

Return only JSON: {"claims": [{"id": "...", "probabilities": {"supported": 0.0, "contradicted": 0.0, "undetermined": 0.0}}], "response": "..."}. Each probability must be between 0 and 1, and the three must add up to 1."""
# Kind "report" claims that are one partner's characterization of the other's character.
# Like motives and feelings, they are attributions to a person that the material rarely settles.
TRAIT_REPORTS = {("calendar", "48367f02"), ("budget", "5520962c")}
ATTRIBUTION_KINDS = ("motive", "feeling")


def read_jsonl(path):
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"Duplicate JSON key: {key}")
            value[key] = item
        return value

    def reject_constant(value):
        raise ValueError(f"Non-finite JSON number: {value}")

    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line, object_pairs_hook=reject_duplicates,
                           parse_constant=reject_constant)
                for line in stream if line.strip()]


def write_jsonl(path, rows):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                        allow_nan=False) + "\n" for row in rows),
                      encoding="utf-8")


def unique_index(rows, key):
    result = {}
    for row in rows:
        value = row[key]
        if not isinstance(value, str) or not value or value in result:
            raise ValueError(f"Invalid or duplicate {key}: {value!r}")
        result[value] = row
    return result


def load_cases(path):
    cases = read_jsonl(path)
    if not cases:
        raise ValueError("Empty dataset")
    unique_index(cases, "id")
    for case in cases:
        if case["provenance"] != "newly_authored_fiction":
            raise ValueError("Only newly authored fiction is permitted")
        for key in ("shared", "A", "B"):
            if not isinstance(case[key], str) or not case[key].strip():
                raise ValueError(f"Missing narrative: {key}")
        if not case["claims"]:
            raise ValueError("No claims")
        unique_index(case["claims"], "id")
        for claim in case["claims"]:
            if not claim["text"].strip() or not claim["rationale"].strip():
                raise ValueError("Claim and rationale required")
            if set(claim["gold"]) != set(CONDITIONS):
                raise ValueError("Gold must cover all conditions")
            if any(label not in LABELS for label in claim["gold"].values()):
                raise ValueError("Invalid label")
            if claim["gold"]["AB"] != claim["gold"]["BA"]:
                raise ValueError("Evidence labels must be order invariant")
    return cases


def build_requests(cases):
    requests = []
    for case in cases:
        # Stable pseudo-random ordering prevents claim index from being a label key.
        claims = sorted(case["claims"], key=lambda c: hashlib.sha256(
            (case["id"] + c["id"]).encode()).hexdigest())
        public_claims = [{"id": c["id"], "text": c["text"]} for c in claims]
        for condition in CONDITIONS:
            text = "Shared facts:\n" + case["shared"]
            for speaker in condition:
                text += f"\n\n{speaker}'s account:\n" + case[speaker]
            text += "\n\nClaims:\n" + json.dumps(public_claims, ensure_ascii=False)
            requests.append({
                "request_id": f"{case['id']}:{condition}",
                "case_id": case["id"], "condition": condition,
                "claims": public_claims,
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": text},
                ],
            })
    return requests


def demo_responses(requests, strategy="uniform"):
    """Plumbing controls that receive public requests only, never gold labels."""
    if strategy not in ("uniform", "always-undetermined"):
        raise ValueError("Unknown demo strategy")
    return [{
        "request_id": request["request_id"],
        "claims": [{"id": claim["id"], "probabilities": {
            label: 1 / 3 if strategy == "uniform" else float(label == "undetermined")
            for label in LABELS}} for claim in request["claims"]],
        "response": "DEMO ONLY: no model-generated reply; human ratings are not applicable.",
    } for request in requests]


def probabilities(value):
    if not isinstance(value, dict) or set(value) != set(LABELS):
        raise ValueError("Exactly three probability labels required")
    numbers = [value[label] for label in LABELS]
    if any(type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1
           for p in numbers):
        raise ValueError("Probabilities must be finite numbers in [0,1]")
    if not math.isclose(sum(numbers), 1, abs_tol=1e-8, rel_tol=0):
        raise ValueError("Probabilities must sum to 1")
    return value


def summarize(items):
    """Unnormalized multiclass Brier in [0,2]; exact top ties get no accuracy credit."""
    briers, correct, risks = [], [], []
    for item in items:
        p, gold = item["p"], item["gold"]
        briers.append(sum((p[label] - float(label == gold)) ** 2 for label in LABELS))
        winners = [label for label in LABELS if p[label] == max(p.values())]
        correct.append(int(len(winners) == 1 and winners[0] == gold))
        if item["attribution"] and gold == "undetermined":
            risks.append(p["supported"])
    bins = {}
    for label in LABELS:
        bins[label] = []
        for low, high in ((0, .5), (.5, .7), (.7, .9), (.9, 1.00000001)):
            selected = [item for item in items if low <= item["p"][label] < high]
            bins[label].append({
                "lower_inclusive": low, "upper_exclusive": min(high, 1),
                "includes_one": high > 1, "n": len(selected),
                "mean_probability": mean(i["p"][label] for i in selected) if selected else None,
                "observed_frequency": mean(i["gold"] == label for i in selected) if selected else None,
            })
    return {"n_claims": len(items), "brier": mean(briers),
            "accuracy_unique_argmax": mean(correct),
            "gold_counts": dict(sorted(Counter(i["gold"] for i in items).items())),
            "unsupported_attribution_support_probability": mean(risks) if risks else None,
            "n_unsupported_attribution_claims": len(risks), "classwise_reliability_bins": bins}


def score(cases, requests, responses):
    """Reject missing/extra rows so partial runs cannot masquerade as full results."""
    request_index = unique_index(requests, "request_id")
    response_index = unique_index(responses, "request_id")
    if not request_index or set(request_index) != set(response_index):
        raise ValueError("Responses must exactly cover the request IDs")
    expected = unique_index(build_requests(cases), "request_id")
    if request_index != expected:
        raise ValueError("Requests must match the full canonical benchmark and prompts")
    case_index = unique_index(cases, "id")
    items, by_key = [], {}
    for rid, request in request_index.items():
        response = response_index[rid]
        if not isinstance(response["response"], str) or not response["response"].strip():
            raise ValueError("Nonempty response text required")
        predictions = unique_index(response["claims"], "id")
        case = case_index[request["case_id"]]
        if set(predictions) != {c["id"] for c in case["claims"]}:
            raise ValueError("Predictions must exactly cover claim IDs")
        for claim in case["claims"]:
            p = probabilities(predictions[claim["id"]]["probabilities"])
            item = {"case_id": case["id"], "condition": request["condition"],
                    "claim_id": claim["id"], "kind": claim["kind"],
                    "attribution": claim["kind"] in ATTRIBUTION_KINDS
                    or (case["id"], claim["id"]) in TRAIT_REPORTS,
                    "gold": claim["gold"][request["condition"]], "p": p}
            items.append(item)
            by_key[(case["id"], request["condition"], claim["id"])] = item
    order_tv, update_deltas = [], []
    for case in cases:
        for claim in case["claims"]:
            ab = by_key[(case["id"], "AB", claim["id"])]
            ba = by_key[(case["id"], "BA", claim["id"])]
            order_tv.append(sum(abs(ab["p"][k] - ba["p"][k]) for k in LABELS) / 2)
            for single in ("A", "B"):
                before = by_key[(case["id"], single, claim["id"])]
                if before["gold"] == "undetermined" and ab["gold"] != "undetermined":
                    update_deltas.append(ab["p"][ab["gold"]] - before["p"][ab["gold"]])
    return {"n_cases": len(cases), "n_requests": len(requests),
            "overall": summarize(items),
            "by_condition": {c: summarize([i for i in items if i["condition"] == c])
                             for c in CONDITIONS},
            "by_case": {c["id"]: summarize([i for i in items if i["case_id"] == c["id"]])
                        for c in cases},
            "order_total_variation_mean": mean(order_tv),
            "new_evidence_probability_gain": mean(update_deltas) if update_deltas else None,
            "n_new_evidence_comparisons": len(update_deltas),
            "human_response_quality": "NOT SCORED; requires blinded human annotation"}


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def implementation_hash():
    digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob("*.py")):
        digest.update(path.name.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def provenance(paths):
    return {"python": platform.python_version(), "implementation_sha256": implementation_hash(),
            "input_sha256": {key: file_hash(path) for key, path in paths.items()}}
