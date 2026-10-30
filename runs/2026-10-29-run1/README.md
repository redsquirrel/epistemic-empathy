# Run 1 (2026-10-29)

The first paid evaluation of the pilot: three provider models, three repetitions each, on the 32
exported requests of protocol commit `c6f477d`. This directory is a record of what was sent,
what came back, and how it scored. It is not a finding. The labels it is scored against are
provisional, and model prose has not been rated by people.

## What was run

| | |
| --- | --- |
| Protocol commit | `c6f477d950d5e646d0d6d38ec42bf8fc138e55ea` |
| Dataset | `data/pilot.jsonl`, sha256 `12fef036c827cab88cf535ac45fe46845d70d279aa7955b56829f3dcdbca7f43` |
| Requests | `requests.jsonl` (32), sha256 `d37cf9bf959e9dd224066957d0a28623c165bd503482461961b0fa8e64fe72e0` |
| Models | `claude-opus-5-5` (Anthropic Messages API), `gpt-6.1-sol` (OpenAI Responses API), `grok-4.7` (xAI Chat Completions) |
| Repetitions | 3 per model, each scored on its own; request order shuffled with seed 1733 + repetition |
| Settings | Provider defaults. Only each request's `messages` were sent. Anthropic requires `max_tokens` (16000); OpenAI was sent `store: false`, which only stops server-side retention. Temperature, top_p, seed, reasoning and effort were not sent. |
| Failure rule | A refusal, truncation or format failure is a failed attempt, retried up to 3 times. Probabilities are never filled in. |
| Budget | $25 cap; $3.63 spent, estimated from returned usage at list prices (not an invoice) |

Every repetition completed 32 of 32 requests. Two Claude attempts in repetition 2
(`blocked_exit:AB`, `quiet_evening:AB`) failed the format check (top level was not exactly
`{claims, response}`) and passed on retry. One Claude response in that repetition was wrapped in a
single ```` ```json ```` fence, which the parser accepts and records. The first GPT smoke test
failed with HTTP 429 because the account had no credits; it cost nothing, and the smoke test was
repeated as `smoke-gpt-6.1-sol-2`.

## Automatic scores

Means of the three repetitions; per-repetition files are in `scores/`. Brier is lower-better
(0–2). Unsupported attribution is the mean probability of "supported" given to the 42 claim judgments (of 192)
that attribute a motive, feeling or trait and that the provisional key marks undetermined.

| Model | Brier | Unique-argmax accuracy | Unsupported attribution | New-evidence gain | AB/BA total variation |
| --- | --- | --- | --- | --- | --- |
| claude-opus-5-5 | 0.087 | 0.944 | 0.050 | 0.790 | 0.018 |
| gpt-6.1-sol | 0.140 | 0.927 | 0.018 | 0.824 | 0.017 |
| grok-4.7 | 0.144 | 0.905 | 0.070 | 0.764 | 0.026 |

`human_response_quality` is unscored in every file: the prose responses need blinded human
annotation.

## Limitations

- The gold labels are provisional and partly disputed; agreement with them is not correctness.
- Eight scenes, one prompt, three repetitions. Differences of this size between models are not
  established as stable.
- Provider defaults differ between providers and can change behind the same model string. Only
  the returned model string is recorded.
- Costs are estimates from token usage and public prices checked on 2026-10-29.

## Files

- `adapter/collect.py`: the collection adapter as it stands (sha256 `9e62d465…`), used for the
  GPT runs and smoke test.
- `adapter/collect-e006c9ca.py`: the earlier version (sha256 `e006c9ca…`), used for the Claude and
  Grok runs and the first smoke tests. It differs by one line: it computed `actual_cost_usd` as the
  change in total spend, which counted the other model's concurrent run. Those manifests were
  corrected from `ledger.jsonl` and say so under `deviations`.
- `adapter/keys.py`: reads API keys from a private file outside the repository.
- The adapter ran from a directory beside the repository checkout (`REPO = HERE.parent /
  "epistemic-empathy"`), so the manifests' `raw_output_path` values are local paths.
- `manifests/`: one per repetition and smoke test, following `experiments/run-manifest.template.json`
  plus `settings_sent`, `attempts_log`, `fenced_json_count` and `adapter_sha256`.
- `responses/`: the scoring files given to `python -m epistemic_empathy score`.
- `scores/`: that command's output.
- `raw/`: every provider response body, one file per attempt, without transport headers.
- `ledger.jsonl`: one line per attempt with its estimated cost.

To re-score a repetition from the repository root:

```sh
python3 -m epistemic_empathy score --requests runs/2026-10-29-run1/requests.jsonl \
  --responses runs/2026-10-29-run1/responses/grok-4.7-rep2.jsonl --output /tmp/score.json
```
