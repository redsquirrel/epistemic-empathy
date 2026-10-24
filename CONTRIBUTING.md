# Contributing

Start with an issue describing a specific research question, measurement concern,
or reproducible failure. Keep changes small enough to review. Every data change
needs a provenance statement and evidence-based label rationale. Never submit
actual client material, real relationship posts, private messages, or composites
derived from real cases, even anonymized. Read [ETHICS.md](docs/ETHICS.md).

Use Python 3.11+ and the standard library for the core harness. Run:

```sh
python3 -m unittest discover -s tests -v
python3 experiments/reproduce.py
```

Tests should protect measurement validity, evidence isolation, metric arithmetic,
and complete accounting of outputs. Do not add a test that simply blesses a new
gold label without independent rationale. Record prompt/data changes as versioned
changes, and never overwrite prior empirical results to hide regressions.

PRs should state the question, change, verification, limitations, and provenance. Label claims as hypothesis, engineering observation,
empirical result, or interpretation. Do not imply a reviewer or maintainer has
endorsed generated material until they actually have.

For a real experiment, freeze a protocol before collection. Publish failures and
negative results alongside successes, after privacy and provenance review.
Disagreements about ratings are welcome; discuss the material, not the reviewer.
Contributors agree to license their original contributions under the repository's
MIT license. Third-party material requires an explicit compatible license and
source attribution.
