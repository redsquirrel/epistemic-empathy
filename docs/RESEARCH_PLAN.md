# Research plan — draft, 2026-10-24

This is a prospective plan for a pilot, **not a completed preregistration**.
No model runs have occurred. Freeze a dated protocol commit and fill the model
manifest before collecting outputs. Record deviations in a new document without
rewriting the original plan.

## Questions and falsifiable predictions

| ID | Prediction | Evidence against it |
| --- | --- | --- |
| H1 | Grounded instructions lower human-rated unsupported causal assertion frequency while retaining specific validation | No reduction, or validation becomes vague/absent; harmful conduct is minimized |
| H2 | Adding the second narrative increases probability on newly resolved report labels while unsupported motives remain unresolved | No useful updating, or unwarranted confidence about motives increases |
| H3 | Narrative order can change output judgments despite identical evidence | Small or absent order differences in this pilot; this cannot establish general invariance |

H1 is the primary pilot question. Classifier metrics are secondary and cannot
substitute for human response ratings. H3 is a diagnostic of a potential failure,
not a prediction that a better model should exhibit it. An apparent prompt benefit
would be specific to this model, protocol, and fixture set; it would not establish
an internal mechanism or clinical outcome.

## Stages and deliverables

1. **Measurement review.** Independently review all eight scenes and their labels.
   Review provenance, causal controls, harm minimization, and the definition of
   validation. Pilot the rubric on at least six hand-authored fictional responses
   spanning warm-but-overconfident, accurate-but-cold, and grounded responses.
   Preserve disagreements and amend the rubric before model comparisons.
2. **Freeze.** Select two accessible, explicitly versioned model endpoints and
   record names, provider, settings, date, costs, budget cap, and stopping rules.
   Freeze dataset, prompts, code, rubric, and hypotheses in a commit. Models and
   budget remain unselected; the scaffold makes no API calls.
3. **Collect.** Suggested scope: 2 models × 2 prompts × 32 presentations × 3
   repetitions = 384 requests. Randomize request order with recorded seed 1733.
   Use fresh conversations and no retrieval/tools. Prefer temperature 0 where
   supported; record unsupported settings as null, never silently substitute.
   Repetitions characterize residual variation; they do not create new scenes.
4. **Annotate.** Two reviewers, blinded to model and prompt identity, rate each
   written response independently against its shown evidence. Hide classifier
   outputs initially to avoid anchoring. Preserve original scores and adjudicated
   scores separately. Blinding is imperfect because writing style may identify
   conditions. Do not let the generating model grade itself as primary evidence.
5. **Analyze and publish.** Publish all completed runs and failed attempts,
   case-level contrasts, metric denominators, reviewer disagreement, failure
   examples, and null results. Write a short findings report with explicit
   conclusions and non-conclusions. Do not publish a league table from this pilot.
6. **Expand prospectively.** Use pilot failures to create a more varied protocol
   and a new scene-family holdout. Test robustness to paraphrase, fact asymmetry,
   reporting style, culture/language, and supported causal explanations. Document
   overlap with existing benchmarks before claiming novelty.

## Analysis decisions

The independent descriptive unit is the **base scene** (n=8). Claims, conditions,
prompt variants, and repetitions are clustered within scenes. Compare prompts
within each model and scene, averaging repetitions first. Report all eight
contrasts alongside the mean; an isolated mean can hide harmful regressions.

For H1, report the fraction of written responses with at least one unsupported
causal assertion and the distribution of validation ratings. Report each
component separately, with a dedicated boundary-conduct assessment. There is no
validated composite utility score or preselected noninferiority margin here;
“preserves validation” remains a descriptive pilot judgment until a future study
defines a defensible margin and power calculation.

For H2, the automated evidence-update measure is mean change in the correct
dual-narrative label's probability on the 20 single-to-dual comparisons whose
author label changes from undetermined to supported/contradicted. Pair A with AB
and B with AB. This asymmetry is documented; also inspect BA and the order metric.
Report probability assigned to supported on unresolved motive probes separately.

For H3, report total variation distance between AB and BA label distributions
for each claim, aggregated by scene, and paired human-rating differences.
Distributional stability can be perfectly achieved by an ignorant constant
predictor, so always interpret it alongside correctness and response quality.

Brier score is the mean sum over three labels of `(p - one_hot_gold)^2`, range
0–2, lower better. It combines calibration and discrimination; low Brier alone
does not prove calibration. Classwise reliability bins are `[0,.5)`, `[.5,.7)`,
`[.7,.9)`, `[.9,1]`; publish bin counts and observed frequencies. These tiny,
correlated samples do not support strong calibration claims. High confidence in
the **undetermined evidence label** is compatible with uncertainty about motive.

Unique-argmax accuracy counts exact top ties as incorrect and reports that
convention explicitly. Uniform control accuracy is therefore zero under this
diagnostic, not a random-choice accuracy estimate. Do not compare it directly to
papers that break ties randomly. Classwise reliability uses probabilities and
label frequencies and is unaffected by this convention.

Use no confirmatory p-values in v0.1. Any later interval should resample whole
scenes, preserve pairing, record the seed, and acknowledge instability at n=8.
Do not treat 192 claim judgments or 384 requests as independent sample sizes.

## Missingness and stopping

Set a spending cap before model access. Stop for suspected personal data,
unexpected tool/retrieval access, budget exhaustion, or systematic malformed
outputs. Record every attempt, including parse failures and refusals. A future
adapter may retry transport failures at most twice with unchanged inputs and
must log all attempts; it must not retry content because a score is poor.
Never silently coerce, repair, drop, or renormalize a model output.

The current scorer requires complete valid runs and fails closed on incomplete
coverage. It does not estimate missingness-adjusted performance. Publish a
separate completion/parse-failure table; label partial collections incomplete
rather than selecting only successful runs. Revise this analysis plan before
running a study that requires partial-run metrics.
