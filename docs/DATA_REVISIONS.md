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
