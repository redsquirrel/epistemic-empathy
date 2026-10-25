"""Render the fictional scenarios as readable HTML or Markdown, without answers."""

import argparse
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from epistemic_empathy.benchmark import CONDITIONS, LABEL_GUIDANCE, build_requests, load_cases


INTRO = (
    "Eight wholly fictional situations involving adult partners. No actual client "
    "material is used. Shared facts are stipulated for each situation; the partners' "
    "accounts describe what they report, not independent proof of events or motives."
)
GUIDANCE = (
    "The statements to assess are questions for review, not additional facts. "
    "Decide whether each is supported, contradicted, or undetermined using only "
    "the material shown. Supported means established by that material; contradicted "
    "means explicitly incompatible with it; undetermined means neither. Missing "
    "event evidence is not contradiction. Proposed answers and author rationales are "
    "omitted from this document. " + " ".join(LABEL_GUIDANCE.split())
)
VIEWS = {
    "A": "Partner A only",
    "B": "Partner B only",
    "AB": "Both partners: A, then B",
    "BA": "Both partners: B, then A",
}
CSS = """
:root { color-scheme: light; --ink:#23332d; --muted:#52665d; --line:#cddbd3; }
* { box-sizing:border-box; }
body { margin:0; background:#f4f7f3; color:var(--ink); font:18px/1.65 system-ui,sans-serif; }
main { max-width:860px; margin:0 auto; padding:36px 24px 72px; }
h1,h2,h3 { line-height:1.25; }
h1 { font-size:2.25rem; margin:10px 0 20px; }
h2 { font-size:1.6rem; margin-top:0; }
h3 { font-size:1.05rem; margin-bottom:8px; }
a { color:#255943; text-underline-offset:3px; }
.eyebrow { color:var(--muted); font-size:.85rem; letter-spacing:.08em; text-transform:uppercase; }
.note { border-left:4px solid #8aab98; padding:12px 18px; background:#e9f0e9; }
.contents { margin:24px 0 40px; }
.scenario { background:white; padding:28px; margin:24px 0; border:1px solid var(--line); border-radius:12px; }
.facts { padding:16px 20px; background:#f4f7f3; border-radius:6px; }
.facts p { margin:0; }
blockquote { margin:0; padding:0 0 0 18px; border-left:3px solid var(--line); }
blockquote p { margin:0; white-space:pre-wrap; }
.claims { padding-left:26px; }
.claims li { padding-left:4px; margin-bottom:12px; }
.back { font-size:.85rem; margin-bottom:0; }
@media (max-width:520px) { main { padding:24px 14px; } .scenario { padding:20px 16px; } h1 { font-size:1.85rem; } }
@media print { body { background:white; font-size:11pt; } main { max-width:none; padding:0; }
 .scenario { break-before:page; border:0; padding:0; } .back { display:none; }
 h2,h3 { break-after:avoid; } blockquote,.claims li { break-inside:avoid; } }
"""


def title(case):
    return case["id"].replace("_", " ").capitalize()


def visible_cases(cases, condition):
    """Use benchmark ordering while selecting only the requested evidence."""
    if condition not in CONDITIONS:
        raise ValueError("Unknown condition")
    requests = {r["case_id"]: r for r in build_requests(cases)
                if r["condition"] == condition}
    return [(case, requests[case["id"]]["claims"]) for case in cases]


def render(cases, condition="AB", output_format="html"):
    if output_format not in ("html", "md"):
        raise ValueError("Output format must be html or md")
    intro = INTRO.replace("Eight", str(len(cases)), 1)
    view = VIEWS[condition]
    view_note = ("This reading view shows both accounts. For a single-account review, "
                 "generate the A-only or B-only version before reading the other account."
                 if len(condition) == 2 else "The other partner's account is not included.")
    warning = "Content note: the final scenario describes a partner blocking the other's exit."
    if output_format == "md":
        lines = ["# Fictional couples scenarios", "", intro, "", f"**View: {view}.** {view_note}",
                 "", GUIDANCE, "", warning, "", "## Contents", ""]
        for i, case in enumerate(cases, 1):
            lines.append(f"{i}. {title(case)}")
        for i, (case, claims) in enumerate(visible_cases(cases, condition), 1):
            lines += ["", "---", "", f"## {i}. {title(case)}", "",
                      "### Facts of the fictional situation", "", case["shared"]]
            for speaker in condition:
                lines += ["", f"### Partner {speaker}'s account", "",
                          "\n".join("> " + line for line in case[speaker].splitlines())]
            lines += ["", "### Statements to assess", ""]
            lines += [f"{n}. {c['text']}" for n, c in enumerate(claims, 1)]
        return "\n".join(lines) + "\n"

    parts = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width, initial-scale=1'>",
             "<title>Fictional couples scenarios</title>", f"<style>{CSS}</style></head><body>",
             "<main id='top'><header><div class='eyebrow'>Epistemic empathy · Reading edition</div>",
             "<h1>Fictional couples scenarios</h1>", f"<p>{escape(intro)}</p>",
             f"<p><strong>View: {escape(view)}.</strong> {escape(view_note)}</p>",
             f"<p class='note'>{escape(GUIDANCE)}</p><p>{escape(warning)}</p></header>",
             "<nav class='contents' aria-label='Scenario contents'><h2>Contents</h2><ol>"]
    for i, case in enumerate(cases, 1):
        parts.append(f"<li><a href='#scenario-{i}'>{escape(title(case))}</a></li>")
    parts.append("</ol></nav>")
    for i, (case, claims) in enumerate(visible_cases(cases, condition), 1):
        parts += [f"<section class='scenario' id='scenario-{i}'>",
                  f"<h2>{i}. {escape(title(case))}</h2>",
                  "<h3>Facts of the fictional situation</h3>",
                  f"<div class='facts'><p>{escape(case['shared'])}</p></div>"]
        for speaker in condition:
            parts += [f"<h3>Partner {speaker}'s account</h3>",
                      f"<blockquote><p>{escape(case[speaker])}</p></blockquote>"]
        parts += ["<h3>Statements to assess</h3><ol class='claims'>"]
        parts += [f"<li>{escape(c['text'])}</li>" for c in claims]
        parts += ["</ol><p class='back'><a href='#top'>Back to contents</a></p></section>"]
    parts.append("</main></body></html>")
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data/pilot.jsonl")
    parser.add_argument("--condition", choices=CONDITIONS, default="AB")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/scenarios.html",
                        help="Destination ending in .html or .md")
    args = parser.parse_args()
    if args.output.suffix not in (".html", ".md"):
        parser.error("--output must end in .html or .md")
    content = render(load_cases(args.data), args.condition, args.output.suffix[1:])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
