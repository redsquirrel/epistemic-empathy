# Fixture review revisions

These revisions precede any model evaluation. Earlier fixtures and engineering
controls remain available in Git history; the current controls are regenerated
from the revised fixtures. The changes reflect wording and evidence review, not
observed model scores.

## 2026-10-25 — Late train

Removed “I say” from B's sentence about trying to send a message. The revised
sentence is: “I tried to send a message, but I do not know whether it arrived.”
The narrative framing already identifies this as B's report. No claim or label
changed.

## 2026-10-25 — Quiet evening

Replaced A's account with:

> I felt rejected when B went to the other room. I thought B was angry with me.

Replaced B's account with:

> I felt overloaded by the noise at work. I wanted a quiet interval so I took a few minutes so I could be more present when I came out.

The revisions remove explicit qualifications about what was not communicated
and use the wording supplied during review. Shared facts and claim texts remain
unchanged. B's stated purpose remains an attributed report.

Claim `29989694`, “A reports that B explicitly said they were angry with A,”
changes from contradicted to undetermined in A, AB, and BA; it remains
undetermined in B. The revised account no longer explicitly rules out such a
statement. Its omission is not contradiction under the existing evidence rules.

This changes the counts per prompt variant from 87 supported, 42 contradicted,
and 63 undetermined to 87 supported, 39 contradicted, and 66 undetermined. The
number of single-to-dual comparisons that resolve an undetermined label changes
from 19 to 18. These are fixture changes, not findings about a model.

## 2026-10-25 — Remaining report prefaces

Removed “I say” from B's accounts in dishes, unanswered message, and blocked
exit. The revised sentences are:

- Dishes: “I forgot them after a long call.”
- Unanswered message: “My phone was in my bag while I was working.”
- Blocked exit: “I wanted to finish talking.”

The narrative framing already identifies these as personal accounts. No claim,
evidence label, or scoring rule changed.

## 2026-10-25 — Calendar wording

Replaced “entered separate events” with “made separate plans” in the shared
facts. Updated A's reference to the other event to “B's plans,” and used the
same plans wording in the two related claims. No evidence labels changed.

## 2026-10-25 — Budget

Replaced A's account with:

> I felt upset when B questioned the chair. I thought it was useful for both of us even though I knew we were supposed to discuss purchases like this first.

Replaced B's account with:

> I felt excluded from the decision. I saw the purchase as disregarding our agreement.

Changed claim `d2d34941` to “A reports feeling upset.” Its evidence labels remain
unchanged. The discussion agreement and shared facts remain unchanged.

Claim `4b62ccc6`, “B reports that A explicitly intended to humiliate B,” changes
from contradicted to undetermined in B, AB, and BA; it remains undetermined in
A. The revised B account no longer explicitly denies having stated what A
intended. Omission alone is not contradiction under the existing evidence rules.

The counts per prompt variant change from 87 supported, 39 contradicted, and
66 undetermined to 87 supported, 36 contradicted, and 69 undetermined. The number
of single-to-dual comparisons that resolve an undetermined label changes from
18 to 17. These changes precede model evaluation.

## 2026-10-25 — Missed signal

Removed “I did not see it blow away.” from A's account. Shared facts, claim
texts, and evidence labels remain unchanged; no claim evaluates whether A saw
the note move.

## 2026-10-25 — Distinguish text checks, events, and motives

After an exploratory author review of quiet evening and blocked exit, clarified
three judgment targets in the data card, model instructions, reading edition,
and review wizard. Original judgments and discussion are preserved in
[the review record](reviews/2026-10-25-exploratory-label-review.json), against
original dataset SHA-256
`d41b944a01e54747b8acff82790f0089e88363bbe8c013d40ad0e696801f31f1`.
They are not relabeled or rescored as if they evaluated the revised claims.

- Quiet evening `29989694` now explicitly checks A's supplied text. A, AB,
  and BA change from undetermined to contradicted; B remains undetermined.
- Blocked exit `47634250` now checks what the shared-facts text describes,
  rather than unspecified reciprocal actions. All four labels change from
  undetermined to contradicted. The incident's facts are unchanged.
- Consistency review found the same report ambiguity in calendar `3a7c047d`
  and budget `4b62ccc6`. Both now explicitly check the relevant supplied account.
  Each changes from undetermined to contradicted in the three conditions that
  show that account; the absent-account condition remains undetermined.
- Quiet evening motive `57457681` retains all undetermined labels, with an
  expanded rationale distinguishing counterevidence from conclusive contradiction.
  The original reviewer's different judgment remains in the review record.

All 48 claims were checked across their conditions. Other labels remain unchanged,
including the unknown read status in unanswered message and the contradicted
compound motive claim in missed signal. Rewritten claims retain their IDs for
traceability; IDs must be paired with dataset hashes when comparing revisions.

Counts per prompt variant change from 87 supported, 36 contradicted, and 69
undetermined to 87 supported, 49 contradicted, and 56 undetermined. Single-to-dual
comparisons resolving an undetermined label increase from 17 to 20. Controls are
regenerated; these are measurement-design changes, not model findings.

## 2026-10-28 — Iteration 1: rewritten stories, claim review, bare model instructions

Dave rewrote the stories by hand and then reviewed all 48 claims against them.
Earlier dataset SHA-256:
`ef3edf3a483b76bacd6e4ca96d239ae33ed812be4c7545b71d30b5e74ce97e65`. Earlier
reviews, the exploratory label review, and any answers collected against that
wording stay tied to it. They are not relabeled or rescored as if they evaluated
the revised stories or claims. Claim IDs are retained, so pair IDs with dataset
hashes when comparing revisions.

**Stories.** 15 of 24 story parts changed. A and B were rewritten in late train,
quiet evening, calendar, and missed signal; B in dishes and blocked exit; shared
facts and B in unanswered message; all three parts in budget. The revised accounts
add partners' readings of each other ("B seemed annoyed at me", "B was angry with
me, as usual", "A is always so sensitive", "A is always so impulsive") and a
stated justification in blocked exit. Unanswered message drops the shared-facts
sentence about the record not establishing whether B saw the message. The full
text is in the fixture file; the earlier text is in Git history.

**New analysis category.** `feeling`: a claim about what someone actually felt,
as distinct from `report`, what they say they felt.

**Claims.** Fourteen claims changed. Labels are listed as A only / B only / both
orders.

| Claim | Change | Labels |
| --- | --- | --- |
| late_train `924299ca` | Rationale only; text unchanged | U/U/U → U/C/C |
| late_train `a7fa5717` | "B arrived before 7 pm." → "B was annoyed upon arrival." (event → feeling) | C/C/C → U/U/U |
| quiet_evening `57457681` | Rationale only; B's account now gives a reason | unchanged |
| quiet_evening `30c8456f` | "They had an explicit agreement about greetings." → "B felt angry." (event → feeling) | C/C/C → U/U/U |
| quiet_evening `29989694` | Rationale only; A's account now says B was angry "as usual" | unchanged |
| dishes `7215791e` | "B reports feeling embarrassed." → "B reports forgetting the dishes." | unchanged |
| dishes `b9e87742` | "B reports having forgotten the dishes after a call." → "B felt annoyed." (report → feeling) | unchanged |
| calendar `48367f02` | "They had agreed to spend that afternoon together." → "A is consistently sensitive." (event → report) | C/C/C → U/U/U |
| unanswered_message `246bf232` | "B reports feeling rushed." → "B reports needing to focus." | unchanged |
| unanswered_message `9791a140` | Rationale only; the old one cited the deleted shared-facts sentence | unchanged |
| budget `5520962c` | "A bought the chair in order to humiliate B." → "A is consistently impulsive." (motive → report) | unchanged |
| budget `4b62ccc6` | Rationale only; B's account now calls A impulsive | unchanged |
| missed_signal `5d297f78` | "chose not to answer" → "avoided answering" | unchanged |
| blocked_exit `47634250` | "The shared facts describe both partners preventing the other from leaving." → "The argument really needed to be resolved." (event → feeling) | unchanged |

Rationales for `924299ca`, `a7fa5717`, `57457681`, `30c8456f`, `29989694`,
`b9e87742`, `48367f02`, `5520962c`, `9791a140`, `4b62ccc6`, and `47634250` use
the text Dave approved; for the three marked "rationale only", the story changed
under an unchanged claim. Every other claim keeps its earlier rationale. Claim
texts end with a period. The two characterization claims (`48367f02`,
`5520962c`) stay `report` by Dave's decision. `47634250` no longer checks the
shared-facts text, so the test that pinned it as a supplied-text control no longer
names it.

Counts change from 87 supported, 49 contradicted, and 56 undetermined to 87
supported, 40 contradicted, and 65 undetermined. Single-to-dual comparisons
resolving an undetermined label change from 20 to 21.

**Model instructions.** The model-facing instructions were reduced to the bare
task, so that scores reflect the model's own judgment rather than our coaching.
The old guidance steered models toward "undetermined" on contextual motive
judgments, such as late train `924299ca` ("B arrived late in order to punish
A"). Removed: the label-target guidance, "Narratives are reports…", "explicitly
incompatible", the reported-feeling line, the line that the labels are not
probabilities of hidden motives, and the `grounded` intervention. The label rules,
plus a new rule on feelings, traits, and justifications, now appear only in the
[data card](../data/README.md#label-semantics). The user message labels each
narrative "A's account:" or "B's account:" (was "Narrative A:"), matching the
instructions' wording. The prior wording remains in Git history.

**Reading edition.** Its reviewer guidance now shows the model instructions
verbatim instead of the label rules, so an independent clinician panel reads the
material under the same instructions as the models and is not coached toward the
authors' labels.

**Unsupported attribution.** `unsupported_motive_support_probability` becomes
`unsupported_attribution_support_probability` (with
`n_unsupported_attribution_claims`). It is the mean probability of "supported"
on undetermined claims that attribute something to a person: motives, actual
feelings, and the two characterization claims (`48367f02`, `5520962c`), which are
kind `report` and are listed in `TRAIT_REPORTS`. Previously it counted motives
only; budget no longer has a motive probe.

**Single prompt.** The `grounded` variant is retired for iteration 1, along with
the `--variant` option and the variant part of request IDs (now `CASE:CONDITION`).
A coached variant may return later as a deliberate comparison. Without it, H1 in
the [research plan](RESEARCH_PLAN.md) is not tested in iteration 1; the plan is
left as written, and this entry records the deviation. Controls are regenerated;
these are measurement-design changes, not model findings.
