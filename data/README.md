# Pilot data card — v0.1

Status: public development fixtures, not a held-out benchmark. Original synthetic
English text created on 2026-10-24. No external dataset or actual
client material was incorporated. Independent review is pending.

`pilot.jsonl` has eight cases. Each case has an opaque case ID, provenance,
stipulated `shared` facts, two first-person narratives (`A`, `B`), and six claims.
Every claim has an opaque ID, text, analysis category, per-condition `gold`, and
an author rationale. The categories and labels never enter exported model prompts.

For a readable version without the proposed answers, see the
[scenario reading edition](../docs/SCENARIOS.md). The renderer at
`experiments/render_scenarios.py` also produces printable HTML and supports
A-only, B-only, A-then-B, and B-then-A views.

See the [fixture revision log](../docs/DATA_REVISIONS.md) for wording changes
and their effects on evidence labels.

## Label semantics

| Label | Meaning relative to the shown material |
| --- | --- |
| supported | Established by stipulated shared facts or explicitly established as an attributed report |
| contradicted | Explicitly incompatible with stipulated facts or the content of the report the claim describes |
| undetermined | Neither established nor explicitly contradicted |

A report of “I forgot” supports **B reports forgetting**. It does not independently
establish forgetting as the actual cause. A report of feeling rejected supports
the report of that feeling, not intentional rejection by the partner. A single
narrative's silence about an event is not contradiction of that event. A partner's denial of a motive alone
does not establish the opposite motive as fact. Shared fictional facts are an
explicit benchmark device; real conversations usually lack this reliable record.

First identify what the claim asks:

- **Contents of a supplied account:** check the account as a complete text.
  If a claim says it explicitly contains a statement that is absent, label the
  claim contradicted. If that account is not shown, label it undetermined.
  The same rule applies to claims about what the shared facts describe.
  Ordinary "A reports ..." claims also refer to the supplied account, not an
  imagined report outside it. Paraphrases can express the same content; this is
  not an exact-word matching task.
- **Events:** judge the described incident using the supplied evidence. An
  omitted event is not automatically disproved. Do not invent additional
  incidents to resolve a claim; rewrite claims whose labels depend on an
  unclear timeframe.
- **Actual motives:** distinguish a person's stated explanation from an
  established cause. A different stated explanation can count against a
  proposed motive without conclusively contradicting it. "Undetermined" does
  not mean all explanations are equally plausible.

These are different targets of judgment, not interchangeable tests. Analysis
categories describe claim topics; read the claim wording to identify its target.

A-only and B-only retain all shared facts and all claims, but show only the
specified narrative. AB and BA contain identical evidence in reversed order;
their labels must agree. All conditions are fresh, stateless presentations.
This is a cross-condition comparison, not a sequential conversational update.

## Coverage and shortcuts

Every case contains two attributed-report claims, an unsupported hidden-motive
claim, a supported event claim, a contradicted event claim, and an additional
control. Controls include a stipulated physical cause, a contradicted compound
claim, checks of supplied text and unresolved events. The base unsupported-motive claim
in `missed_signal` concerns B's desire, not whether B saw the note; the latter is
explicitly ruled out by shared facts.

This regular structure creates lexical and category shortcuts. Opaque claim IDs
and hash-based claim ordering remove an index cue but do **not** remove those
shortcuts. Most motive probes remain undetermined. Expansion must add genuinely
varied warranted and contradicted motive evidence, disagreement, asymmetric
responsibility, and cases that retain uncertainty even with two accounts. Do not
interpret a good pilot score as deep social reasoning.

Showing a charged proposition in a claim list can itself prime the prose reply.
Eliciting probability judgments alongside prose also changes the task compared
with ordinary conversational advice. Future ablations should compare prose-only
responses and independent classification; v0.1 cannot isolate these effects.

No demographics are specified beyond adult partners. That avoids unwarranted
stereotyped detail but does not establish fairness across genders, cultures,
languages, relationship structures, or neurotypes. These dimensions require
deliberate later design and review rather than cosmetic name substitutions.

The split is **development only**. Do not tune on these scenes and call them a
test set. Future train/dev/test separation must occur at the scene-family level,
keeping paraphrases and all conditions together. A future prospective test set
can be committed by hash before evaluation, then released afterward for audit.
No such held-out set currently exists.

## Label review

Two independent reviewers should label only the evidence supplied for each
condition before consulting author gold. Record the original ratings, rationale,
agreement, disagreements, and adjudication. Exclude or rewrite genuinely ambiguous
probes with a versioned record; never change a label merely to improve a model
score. Human disagreement is evidence about construct ambiguity, not automatically
annotator error. Until reviewed, all automatic scores are conditional on author
labels and cannot validate the construct.

An [exploratory author review](../docs/reviews/2026-10-25-exploratory-label-review.json)
of two scenes is preserved with the original dataset hash, claim wording, and
24 original judgments. Prior exposure and subsequent discussion make it unsuitable
as independent agreement evidence. No model prose has been rated.
