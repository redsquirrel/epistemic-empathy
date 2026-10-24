# Epistemic Empathy

**Can an AI acknowledge a person's emotional experience while remaining honest
about what it does—and does not—know about another person's perspective?**

An independent, public-facing research project initiated by Dave Hoover. We study
perspective-taking under narrative uncertainty, beginning with paired, wholly
fictional adult couples narratives. The alignment concern is that a warm, convincing
response can turn a speaker's interpretation into an unsupported causal story.

**Status: v0.1 engineering pilot. No AI model has been evaluated. No hypothesis has
been confirmed.** The scenarios, labels, code, and initial prose require
independent review. There is no Anthropic affiliation or endorsement. This is an
evaluation research artifact, not a therapy tool.

## Research charter

We use *epistemic empathy* as a working operational term: representing the
perspectives actually available, acknowledging reported feelings, and maintaining
the boundary between evidence and interpretation. It is not a claim that a model
has subjective empathy or an established psychological construct.

Consider: “I felt rejected when my partner went quiet.” A response can acknowledge
that hurt without concluding, “Your partner went quiet to punish you.” A second
narrative might add, “I felt overwhelmed and needed quiet.” That establishes a
second **reported** perspective; it does not prove a hidden motive or invalidate
the first person's feeling. Explicitly described harmful conduct should still be
acknowledged. Uncertainty must not become an excuse for invented equal blame.

Our goals are to:

- Measure evidence-sensitive perspective representation and uncertainty.
- Distinguish emotional validation from agreement with unsupported explanations.
- Test whether adding a perspective changes judgments appropriately, and whether
  merely reversing presentation order changes them inappropriately.
- Publish protocols, fixtures, disagreements, raw synthetic outputs, negative
  results, and limitations so others can challenge the work.

We will not diagnose people, adjudicate real relationships, test on clients,
collect therapy transcripts, or infer clinical benefit from benchmark scores.
Even anonymized, composite, remembered, or paraphrased client cases are excluded.
See [ethics and provenance](docs/ETHICS.md).

## First benchmark

Eight original fictional situations cover a late train, a quiet evening, dishes,
calendar assumptions, an unanswered message, shared spending, a missed note, and
a blocked exit. Each has A-only, B-only, A-then-B, and B-then-A presentations:
**32 requests and 192 claim judgments per prompt variant**. The blocked-exit
scenario contains non-graphic coercive conduct.

Each request asks for probabilities over `supported`, `contradicted`, and
`undetermined`, plus a short response. Labels describe **support in the shown
material**, not the actual truth of a person's motive. Fictional shared facts are
stipulated; individual narratives remain attributed reports. The full semantics
and provisional labels are in the [data card](data/README.md).

Two prompts hold the evidence and output contract constant. `baseline` gives the
task; `grounded` additionally asks for specific emotional acknowledgment,
source attribution, uncertainty, and a non-leading clarification question.
The baseline already defines evidence grounding, so this is an incremental
instruction comparison, not an unconstrained chatbot comparison.

Automated metrics include multiclass Brier score, classwise reliability bins,
unique-argmax accuracy, unsupported-motive support probability, evidence-update
gain, and A/B order sensitivity. None measures empathy by itself. Written
responses need the separate [human rubric](docs/ANNOTATION.md); no keyword-based
or self-grading “empathy score” is used.

## Reproduce locally

Use Python 3.11 or newer from this repository's root. The project uses only the
standard library; there are no packages to install, API keys, paid calls, or
network access in these commands. Initial local verification used Python 3.14.8.

```sh
python3 -m unittest discover -s tests -v
python3 experiments/reproduce.py
```

This generates uniform and always-undetermined controls for both prompts. Raw
requests and responses go to ignored `work/demo/`; the checked-in
[summary](results/demo-summary.json) records input and implementation hashes.
These controls verify the harness; **they are not LLM results**. See
[results status](results/README.md) for interpretation and reproduction details.

To export a prompt set and score a conforming response file:

```sh
python3 -m epistemic_empathy build --variant grounded --output work/requests.jsonl
python3 -m epistemic_empathy demo --requests work/requests.jsonl --output work/responses.jsonl
python3 -m epistemic_empathy score --requests work/requests.jsonl --responses work/responses.jsonl --output work/score.json
```

The `demo` step is deliberately synthetic. Replace it with a separately reviewed
model adapter for an actual experiment. Such an adapter must send only `messages`
from exported requests, keep fresh conversations for each request, and must not
give the evaluated model repository or answer-key access. Follow the
[experiment contract](experiments/README.md) and complete the run manifest before
making model calls. The scorer refuses incomplete or mismatched runs.

## Hypotheses and next steps

**H1:** The grounded prompt may reduce unsupported causal assertions in the written
reply while preserving specific validation. **H2:** A second narrative may improve
judgments about newly available reports without making unknown motives certain.
**H3:** Presentation order may affect judgments despite unchanged evidence.
These are hypotheses, not findings. The pilot cannot establish their prevalence
or generalization. See the [research plan](docs/RESEARCH_PLAN.md).

First: independently review provenance and labels; test the annotation rubric;
freeze a versioned protocol; then run a small model comparison. The
[initial issue backlog](docs/ISSUES.md) contains ready-to-publish issues and
acceptance criteria.

## Limits and related work

The dataset is tiny, English-only, and deliberately patterned. The scenarios and
rubric were developed together and have not been independently reviewed.
Eight scenes are eight dependent units, not 192 independent observations. Public gold labels invite contamination;
fluency, label accuracy, and calibrated probabilities do not establish real-world
empathy, relationship outcomes, clinical usefulness, or safety.

This builds on work on [sycophancy](https://arxiv.org/abs/2310.13548v4),
[information-asymmetric perspective tasks](https://aclanthology.org/2023.emnlp-main.890/),
and [model uncertainty](https://arxiv.org/abs/2207.05221v4). Existing
[interpersonal sycophancy research](https://arxiv.org/abs/2510.01395v1) and the
[Social Sycophancy Scale](https://arxiv.org/abs/2603.15448v1) make a novelty claim
premature. Our candidate contribution is a small, auditable paired-narrative
protocol connecting evidence updates to validation without unsupported motives.
See the [annotated reading list](docs/RELATED_WORK.md).

## Contributing and reuse

See [CONTRIBUTING.md](CONTRIBUTING.md) before submitting data or examples. Never put
real personal or clinical material in an issue, PR, prompt, or evaluation output.
Use issues to challenge labels and propose falsifiable alternatives. Preserve
original results when correcting analysis. The initial project uses the
[MIT license](LICENSE) for original code, documentation, and fictional fixtures;
external papers retain their own licenses. Research uses should cite the exact
commit and dataset hash, and describe this as an unvalidated pilot.
