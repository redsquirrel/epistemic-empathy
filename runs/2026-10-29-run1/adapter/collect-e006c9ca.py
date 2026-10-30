"""Collect run 1 model responses for the epistemic-empathy benchmark (local only; not for the repo).

    python3 -I collect.py export                  # exported requests from the pinned protocol
    python3 -I collect.py smoke                   # one request per model, cost projection
    python3 -I collect.py run MODEL REP           # one repetition: 32 requests
    python3 -I collect.py score MODEL REP         # score a complete repetition with the repo scorer

Only each request's `messages` are sent. Provider default sampling: nothing but the model, the
messages and (Anthropic only, where it is required) max_tokens is set. A refusal, truncation or
format failure is a failed attempt; probabilities are never filled in. Keys come from keys.py and
are never printed or stored; raw provider bodies are stored without transport headers.
"""

import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import random
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / "epistemic-empathy"
PROTOCOL = "c6f477d950d5e646d0d6d38ec42bf8fc138e55ea"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from epistemic_empathy.benchmark import probabilities, read_jsonl, write_jsonl  # noqa: E402
import keys  # noqa: E402

REQUESTS = HERE / "requests.jsonl"
LEDGER = HERE / "ledger.jsonl"
BUDGET_CAP_USD = 25.0
MAX_ATTEMPTS = 3
WORKERS = 4
ANTHROPIC_MAX_TOKENS = 16000
ADAPTER_VERSION = "run1-collect-1"

# USD per million tokens, from the providers' public pricing pages (checked 2026-10-29).
MODELS = {
    "claude-opus-5-5": {"provider": "anthropic", "input": 4.00, "cached": 0.20, "output": 20.00},
    "gpt-6.1-sol": {"provider": "openai", "input": 2.00, "cached": 0.10, "output": 10.00},
    "grok-4.7": {"provider": "xai", "input": 2.00, "cached": 0.50, "output": 6.00},
}

_lock = threading.Lock()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def spent():
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(line)["cost_usd"] for line in LEDGER.read_text().splitlines() if line)


def post(url, headers, body, timeout=900):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"content-type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"error_text": raw[:2000]}


def call(model, messages, secret):
    """Return (status, body, settings). Settings record exactly what was sent besides messages."""
    provider = MODELS[model]["provider"]
    if provider == "anthropic":
        system = [m["content"] for m in messages if m["role"] == "system"]
        settings = {"max_tokens": ANTHROPIC_MAX_TOKENS}
        body = {"model": model, "max_tokens": ANTHROPIC_MAX_TOKENS, "system": system[0],
                "messages": [m for m in messages if m["role"] != "system"]}
        status, data = post("https://api.anthropic.com/v1/messages",
                            {"x-api-key": secret, "anthropic-version": "2023-06-01"}, body)
    elif provider == "openai":
        settings = {"store": False}
        body = {"model": model, "input": messages, "store": False}
        status, data = post("https://api.openai.com/v1/responses",
                            {"authorization": "Bearer " + secret}, body)
    else:
        settings = {}
        body = {"model": model, "messages": messages}
        status, data = post("https://api.x.ai/v1/chat/completions",
                            {"authorization": "Bearer " + secret}, body)
    return status, data, settings


def extract(model, data):
    """Return (text, failure, returned_model). failure is None or a short reason."""
    provider = MODELS[model]["provider"]
    if provider == "anthropic":
        stop = data.get("stop_reason")
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        failure = {"refusal": "refusal", "max_tokens": "truncated"}.get(stop)
        return text, failure, data.get("model")
    if provider == "openai":
        text, failure = "", None
        for item in data.get("output", []):
            if item.get("type") != "message":
                continue
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    text += part.get("text", "")
                elif part.get("type") == "refusal":
                    failure = "refusal"
        if data.get("status") == "incomplete":
            failure = failure or "truncated"
        return text, failure, data.get("model")
    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    failure = "refusal" if message.get("refusal") else None
    if choice.get("finish_reason") == "length":
        failure = failure or "truncated"
    return message.get("content") or "", failure, data.get("model")


def cost(model, data):
    price = MODELS[model]
    usage = data.get("usage") or {}
    provider = price["provider"]
    if provider == "anthropic":
        cached = usage.get("cache_read_input_tokens") or 0
        written = usage.get("cache_creation_input_tokens") or 0
        fresh, out = usage.get("input_tokens") or 0, usage.get("output_tokens") or 0
        return (fresh * price["input"] + written * price["input"] * 1.25 + cached * price["cached"]
                + out * price["output"]) / 1e6
    if provider == "openai":
        total = usage.get("input_tokens") or 0
        cached = (usage.get("input_tokens_details") or {}).get("cached_tokens") or 0
        out = usage.get("output_tokens") or 0
        return ((total - cached) * price["input"] + cached * price["cached"] + out * price["output"]) / 1e6
    if usage.get("cost_in_usd_ticks") is not None:
        return usage["cost_in_usd_ticks"] / 1e10
    total = usage.get("prompt_tokens") or 0
    cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
    out = usage.get("completion_tokens") or 0
    # Conservative: count reasoning tokens on top in case they are not inside completion_tokens.
    out += (usage.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
    return ((total - cached) * price["input"] + cached * price["cached"] + out * price["output"]) / 1e6


def parse(text, claim_ids):
    """Strict parse of the model's JSON. Returns (record_fields, fenced) or raises ValueError."""
    body, fenced = text.strip(), False
    if body.startswith("```") and body.endswith("```") and body.count("```") == 2:
        body, fenced = body[3:-3].strip(), True
        if body.startswith("json"):
            body = body[4:]
    value = json.loads(body)
    if not isinstance(value, dict) or set(value) != {"claims", "response"}:
        raise ValueError("top level must be exactly {claims, response}")
    if not isinstance(value["response"], str) or not value["response"].strip():
        raise ValueError("empty response text")
    claims = value["claims"]
    if not isinstance(claims, list) or sorted(c.get("id") for c in claims if isinstance(c, dict)) \
            != sorted(claim_ids) or len(claims) != len(claim_ids):
        raise ValueError("claims must cover each claim ID exactly once")
    out = [{"id": c["id"], "probabilities": probabilities(c["probabilities"])} for c in claims]
    return {"claims": out, "response": value["response"]}, fenced


def attempt_request(model, rep, request, secret, raw_dir):
    claim_ids = [c["id"] for c in request["claims"]]
    log = []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        with _lock:
            if spent() >= BUDGET_CAP_USD:
                raise RuntimeError("budget cap reached")
        started = now()
        try:
            status, data, settings = call(model, request["messages"], secret)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            status, data, settings = None, {"transport_error": repr(exc)}, {}
        c = cost(model, data) if status == 200 else 0.0
        name = f"{request['request_id'].replace(':', '__')}.attempt{attempt}.json"
        (raw_dir / name).write_text(json.dumps({"status": status, "started_at_utc": started,
                                                "finished_at_utc": now(), "body": data}, indent=1))
        with _lock:
            with LEDGER.open("a") as f:
                f.write(json.dumps({"model": model, "rep": rep, "request_id": request["request_id"],
                                    "attempt": attempt, "status": status, "cost_usd": c}) + "\n")
        entry = {"attempt": attempt, "status": status, "cost_usd": round(c, 6), "raw": name}
        if status != 200:
            entry["failure"] = f"http_{status}"
            log.append(entry)
            if status in (400, 401, 403, 404):
                raise RuntimeError(f"{model}: HTTP {status}; see {raw_dir / name}")
            time.sleep(5 * attempt)
            continue
        text, failure, returned = extract(model, data)
        entry["model_returned"] = returned
        if not failure:
            try:
                record, fenced = parse(text, claim_ids)
                entry["fenced"] = fenced
                log.append(entry)
                return {"request_id": request["request_id"], **record}, log
            except (ValueError, TypeError, KeyError, AttributeError) as exc:
                failure = f"format: {exc}"[:200]
        entry["failure"] = failure
        log.append(entry)
    return None, log


def git_head():
    return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def export():
    if git_head() != PROTOCOL:
        sys.exit(f"Repo HEAD is not protocol {PROTOCOL}")
    subprocess.run([sys.executable, "-m", "epistemic_empathy", "build", "--output", str(REQUESTS)],
                   cwd=REPO, check=True)
    print(f"Exported {len(read_jsonl(REQUESTS))} requests, sha256 {sha256(REQUESTS)}")


def run(model, rep, request_ids=None, label=None):
    secret = keys.load()[{"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY",
                          "xai": "XAI_API_KEY"}[MODELS[model]["provider"]]]
    requests = read_jsonl(REQUESTS)
    if request_ids:
        requests = [r for r in requests if r["request_id"] in request_ids]
    seed = 1733 + int(rep)
    random.Random(seed).shuffle(requests)
    label = label or f"{model}-rep{rep}"
    raw_dir = HERE / "raw" / label
    raw_dir.mkdir(parents=True, exist_ok=False)
    started, before = now(), spent()
    results, logs = {}, {}
    with cf.ThreadPoolExecutor(WORKERS) as pool:
        futures = {pool.submit(attempt_request, model, rep, r, secret, raw_dir): r["request_id"]
                   for r in requests}
        for fut in cf.as_completed(futures):
            rid = futures[fut]
            record, log = fut.result()
            logs[rid] = log
            if record:
                results[rid] = record
    order = [r["request_id"] for r in read_jsonl(REQUESTS) if r["request_id"] in results]
    responses_path = HERE / "responses" / f"{label}.jsonl"
    responses_path.parent.mkdir(exist_ok=True)
    write_jsonl(responses_path, [results[rid] for rid in order])
    returned = sorted({e.get("model_returned") for log in logs.values() for e in log
                       if e.get("model_returned")})
    failed = sorted(rid for rid in logs if rid not in results)
    attempts = sum(len(log) for log in logs.values())
    manifest = {
        "status": "COMPLETE" if not failed else "INCOMPLETE: failed requests listed in deviations",
        "run_id": label, "protocol_commit": PROTOCOL,
        "dataset_sha256": sha256(REPO / "data/pilot.jsonl"),
        "requests_sha256": sha256(REQUESTS), "responses_sha256": sha256(responses_path),
        "provider": MODELS[model]["provider"], "model_requested": model,
        "model_version_returned": returned,
        "provider_version_limitations": "Provider-reported model string only; the provider may "
                                        "change weights or serving behind it.",
        "repetition": int(rep),
        "temperature": None, "top_p": None,
        "max_output_tokens": ANTHROPIC_MAX_TOKENS if MODELS[model]["provider"] == "anthropic" else None,
        "provider_seed": None,
        "unsupported_settings": [],
        "settings_sent": {"anthropic": {"max_tokens": ANTHROPIC_MAX_TOKENS},
                          "openai": {"store": False}, "xai": {}}[MODELS[model]["provider"]],
        "settings_note": "Provider defaults: temperature, top_p, seed, reasoning/thinking and effort "
                         "were not sent. Anthropic requires max_tokens. OpenAI store=false only "
                         "stops server-side retention. Nulls mean provider default, not zero.",
        "request_order_seed": seed,
        "started_at_utc": started, "finished_at_utc": now(),
        "python_version": sys.version.split()[0], "adapter_version": ADAPTER_VERSION,
        "adapter_sha256": sha256(__file__),
        "budget_cap_usd": BUDGET_CAP_USD,
        "actual_cost_usd": round(spent() - before, 4),
        "cost_note": "Estimated from returned token usage and public list prices; not an invoice.",
        "attempts_log": logs, "attempt_count": attempts, "failure_count": len(failed),
        "failed_attempt_count": sum(1 for log in logs.values() for e in log if e.get("failure")),
        "fenced_json_count": sum(1 for log in logs.values() for e in log if e.get("fenced")),
        "raw_output_path": str(raw_dir),
        "contributors": ["Dave Hoover (approval, keys)", "Fellow research (protocol, analysis plan)"],
        "deviations": [f"{rid}: no valid response after {MAX_ATTEMPTS} attempts" for rid in failed],
        "publication_review": None,
    }
    manifest_path = HERE / "manifests" / f"{label}.json"
    manifest_path.parent.mkdir(exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"run": label, "ok": len(results), "failed": failed, "attempts": attempts,
                      "cost_usd": manifest["actual_cost_usd"], "spent_total_usd": round(spent(), 4),
                      "model_returned": returned}))


def score(label):
    out = HERE / "scores" / f"{label}.json"
    subprocess.run([sys.executable, "-m", "epistemic_empathy", "score", "--requests", str(REQUESTS),
                    "--responses", str(HERE / "responses" / f"{label}.jsonl"), "--output", str(out)],
                   cwd=REPO, check=True)
    print(f"Scored {label} -> {out}")


def smoke():
    requests = read_jsonl(REQUESTS)
    longest = max(requests, key=lambda r: len(r["messages"][1]["content"]))
    mean_len = sum(len(r["messages"][1]["content"]) for r in requests) / len(requests)
    projection = {}
    for model in MODELS:
        before = spent()
        run(model, 0, {longest["request_id"]}, label=f"smoke-{model}")
        projection[model] = round((spent() - before) * 96, 2)
    print(json.dumps({"smoke_request": longest["request_id"],
                      "longest_vs_mean_input_chars": round(len(longest["messages"][1]["content"]) / mean_len, 2),
                      "projected_full_run_usd_by_model": projection,
                      "projected_total_usd": round(sum(projection.values()), 2),
                      "spent_so_far_usd": round(spent(), 4)}, indent=1))


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "export":
        export()
    elif command == "smoke":
        smoke()
    elif command == "run":
        run(sys.argv[2], sys.argv[3])
    elif command == "score":
        score(f"{sys.argv[2]}-rep{sys.argv[3]}")
