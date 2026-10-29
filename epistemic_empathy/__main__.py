"""Run from the repository root: python -m epistemic_empathy --help."""

import argparse
import json
from pathlib import Path

from .benchmark import (build_requests, demo_responses, load_cases, provenance,
                        read_jsonl, score, write_jsonl)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="Export model-facing prompts without gold labels")
    build.add_argument("--data", default="data/pilot.jsonl")
    build.add_argument("--output", required=True)
    demo = sub.add_parser("demo", help="Generate an offline plumbing control, not an LLM result")
    demo.add_argument("--requests", required=True)
    demo.add_argument("--strategy", choices=("uniform", "always-undetermined"), default="uniform")
    demo.add_argument("--output", required=True)
    evaluate = sub.add_parser("score", help="Score a complete response set")
    evaluate.add_argument("--data", default="data/pilot.jsonl")
    evaluate.add_argument("--requests", required=True)
    evaluate.add_argument("--responses", required=True)
    evaluate.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.command == "build":
            write_jsonl(args.output, build_requests(load_cases(args.data)))
        elif args.command == "demo":
            write_jsonl(args.output, demo_responses(read_jsonl(args.requests), args.strategy))
        else:
            result = score(load_cases(args.data), read_jsonl(args.requests), read_jsonl(args.responses))
            result["provenance"] = provenance({"data": args.data, "requests": args.requests,
                                               "responses": args.responses})
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
                              encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Invalid benchmark input: {exc}\n")


if __name__ == "__main__":
    main()
