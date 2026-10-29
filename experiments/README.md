# Experiment scaffold

The repository implements prompt export, offline controls, response validation,
automatic metrics, and reproducible summaries. **There is no provider adapter,
paid evaluation, human-rating collection, or empirical model result yet.**
The next issues specify those boundaries rather than concealing them behind
placeholder model names or fabricated ratings.

## Model-facing boundary

`build` exports JSONL records containing IDs, public claims, and `messages`.
Only `messages` should be sent to a model, with no access to repository files.
The harness attaches `request_id` after receiving the response; a model need not
generate that ID. The dataset file contains gold labels and is evaluation-only.
Claims themselves can contain a proposition not present in the narratives; the
task is to determine its evidence status, not assume the question asserts it.

For each request, store one response record of this shape (shown with a dummy ID):

```json
{
  "request_id": "CASE:CONDITION",
  "claims": [
    {
      "id": "CLAIM_ID",
      "probabilities": {
        "supported": 0.1,
        "contradicted": 0.1,
        "undetermined": 0.8
      }
    }
  ],
  "response": "The model's actual prose goes here."
}
```

Include all six claims exactly once and every request exactly once. A run is one
model and one repetition: 32 responses. Do not concatenate repetitions into one
scoring file. Preserve transport records
and raw output separately. Record a refusal/format failure as a failed attempt;
do not invent probabilities to get the scorer to run. The scorer binds requests
to the canonical dataset and prompt and rejects missing/extra IDs,
duplicates, malformed probabilities, empty prose, and altered prompts.

## Run metadata

Copy [run-manifest.template.json](run-manifest.template.json) for each real run.
Fill every applicable field and explain nulls. The manifest is an operational
template; the current scorer does not validate provider metadata. `score` writes
its own file hashes, implementation hash, and actual Python version. Preserve
both files. Also record the protocol commit, model version (not merely an alias),
UTC collection times, exact settings, request-order seed, failures/retries, costs,
and contributors. Never include secrets or transport headers.

Pin the protocol and runtime before collection. Vendor models can change behind
aliases and numerical determinism is not guaranteed even at temperature zero.
Reproducibility here means auditable inputs and rerunnable scoring of archived
outputs, not a promise that a remote model will regenerate identical text.

The first reviewer should inspect an exported prompt to confirm no answer-key or
unshown narrative content crosses the boundary. Tests cover this property, but
an adapter must also preserve it.

## Development workflow

Improve one issue at a time with tests and a reviewable PR.
Keep development examples focused on fictional fixtures. Distinguish hypotheses,
engineering controls, model observations, and interpretations.
Do not run the evaluated model as a repository-aware coding agent: that would
expose the answer key. Review generated examples and prose before publication.

Do not automatically publish raw model output, accept generated labels as expert
consensus, or silently revise the protocol after observing a favorable result.
