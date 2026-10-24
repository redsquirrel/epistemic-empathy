# Initial issue backlog

These six issues are prepared for GitHub publication. This file is the versioned
starting plan; live issue status, once published, is authoritative. No issue has
been marked completed by this scaffold.

## 1. Independently review fictional provenance and all pilot evidence labels

The pilot has eight newly authored fictional scenes, 32 evidence presentations, and 192 claim judgments per prompt variant. Labels are provisional and await independent review.

Acceptance criteria:
- Two independent reviewers inspect provenance and label each shown condition before seeing author gold.
- Preserve original ratings, reasons, disagreement, and adjudication in a versioned artifact.
- Check report-versus-fact semantics, missing evidence versus contradiction, and the blocked-exit control.
- Confirm no actual client material, remembered cases, composites, private messages, or copied relationship posts were used.
- Revise or exclude ambiguous items with a documented rationale; version the dataset and regenerate controls.

See data/README.md and docs/ETHICS.md. This review is a prerequisite for interpreting model scores.

## 2. Pilot the human rubric and prepare blinded response annotation

Automatic claim scores cannot establish validation quality or count unsupported assertions in prose.

Acceptance criteria:
- Independently review docs/ANNOTATION.md for construct validity and overlap with existing social-sycophancy measures.
- Author at least six wholly fictional response anchors spanning warmth, accuracy, speculation, and harm minimization.
- Have two reviewers rate them independently; publish disagreement and rubric changes without implying validation from this tiny exercise.
- Implement reproducible anonymous output IDs, shuffled annotation exports, and a separate mapping that hides model/prompt identity from reviewers.
- Preserve separate original and adjudicated ratings, skipped reasons, and NA values for non-boundary cases.
- Add tests for mapping integrity and the absence of model labels in blinded exports.

No client or participant material is permitted. See experiments/annotations-template.csv.

## 3. Freeze a pilot protocol with explicit model versions and spending limits

docs/RESEARCH_PLAN.md is a draft prospective plan, not a preregistration. No model runs have occurred.

Acceptance criteria:
- Select two accessible model versions and fill run-manifest fields, including the limitations of any moving aliases.
- Set a budget cap, settings, stopping rules, and collection dates before calls.
- Confirm the proposed 384-request design or document a justified revision before collection.
- Freeze dataset, prompts, rubric, analysis, runtime, and protocol in a dated commit after independent review.
- Keep the scene as the unit of analysis and avoid confirmatory claims from the eight-scene pilot.
- Record any subsequent deviations separately from the frozen plan.

Depends on independent label and rubric review. Do not add API keys to the repository.

## 4. Implement one auditable model adapter without answer-key access

The harness exports public requests and scores response JSONL, but deliberately has no provider adapter yet. Start with one provider after the protocol and budget are chosen.

Acceptance criteria:
- Send only exported messages, in fresh conversations, with no repository, tools, retrieval, or gold-label access.
- Preserve raw outputs and actual provider/model/settings metadata; attach request IDs outside model generation.
- Record every attempt, refusal, parse failure, cost, and transport retry; use at most two retries for transport failures only.
- Enforce the approved budget and never retry because an answer scores poorly.
- Never silently repair, coerce, or normalize malformed output; test rejection and complete accounting.
- Test the boundary using a local fake transport and inspect one exported prompt before any real run.
- Keep credentials in the environment and redact secrets from transport metadata.

The current scorer requires complete valid runs; publish failure coverage separately rather than cherry-picking successes.

## 5. Run and publish the first exploratory model comparison

After review, protocol freeze, and adapter verification, collect the first real model outputs and human annotations.

Acceptance criteria:
- Archive synthetic requests, raw outputs, response files, manifest, failures, and hashes for every planned run.
- Collect independent blinded human ratings and preserve disagreements.
- Report scene-level paired contrasts for validation and unsupported causal assertions, plus secondary Brier, calibration bins, evidence updates, and order effects.
- Report null and adverse results, missingness, and the blocked-exit case separately.
- Review artifacts for personal data invented by a model before publication; record any redactions.
- Explicitly separate observations from interpretation and make no clinical, safety, general-empathy, or causal-mechanism claim.

No model comparison is currently complete. Engineering controls in results/ are not evidence for these hypotheses.

## 6. Design harder scene families and a prospective holdout

The pilot has predictable claim types and mostly unresolved motive probes. It tests plumbing and semantics rather than broad social reasoning.

Acceptance criteria:
- Review related-work methods and instruments before claiming a novel construct or benchmark gap.
- Add varied evidence structures, warranted and contradicted causal explanations, conflicting reports, and asymmetric responsibility.
- Audit lexical shortcuts, charged claim priming, and effects of asking probability judgments before a prose response.
- Keep paraphrases and narrative conditions within the same scene-family split.
- Specify a future test-set construction and hash-commit procedure before evaluation, with release after collection.
- Document cultural/language and demographic scope, reviewer expertise, and unresolved fairness limits.
- Use only newly invented fiction and record independent provenance/label review.

A held-out test set does not exist in v0.1; do not relabel development fixtures as held out.
