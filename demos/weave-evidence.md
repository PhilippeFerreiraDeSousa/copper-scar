# Hosted Weave evidence checkpoint

Checked September 12, 2026, for source base `27846f9`.

Project: https://wandb.ai/philippe-fdesousa/copper-scar/weave

## Current evidence

| Item | Status |
|---|---|
| Existing hosted traces | Not verified: project URL shows logged-out 404 |
| Existing hosted evaluation | Not verified: same access blocker |
| Attached online scorer results | Not verified: same access blocker |
| UI Monitor / Signal configuration | Not verified; code and README are not evidence of an enabled Monitor |
| Local instrumentation | Source present; injected fake-client tests pass |
| Local dataset run | 8/8 authored fixture expectations pass offline |

The page says login or owner privacy permissions may be required. Only the Codex
in-app browser was available, without an authenticated W&B session. Neither
`WANDB_API_KEY` nor `WEAVE_API_KEY` was set, and no api.wandb.ai netrc credential
was configured. No secrets were read out, no traces were created, and no paid
inference was invoked. A logged-out 404 does not establish that the project or
records are absent.

Smallest next action: sign in to W&B in the Codex in-app browser, then open the
project URL with the account that has access. Do not paste an API key into chat.
Do not change project visibility just to make the demo work.

## Views to verify after login, before using the live script

These are source-derived record names to locate, not confirmed UI records or
bookmarked URLs. UI navigation labels may differ. Record actual record URLs and
timestamps here after inspection; avoid using a failed historical attempt.

1. Traces: locate a completed `copper_scar.agent_pass` / `loop.pass.2` call.
   Inspect `act.apply_scar` for the keepout credit, then `evaluate.drc`,
   `evaluate.gates`, and `evaluate.score`. Confirm output score 21797.2,
   `drc_count=0`, `gates_ok=true`, `scar_id=scar_001` and policy
   `copper-scar-sim-v1`. Inspect pass 1's `improve.scar.write` as the causal input.
   Values may be in outputs or summaries rather than persisted attributes.
2. Evaluations: locate completed `copper-scar-loop-eval` on
   `copper-scar-boards`, inspect its eight fixture rows and actual scorer values.
   A successful local fallback table does not prove hosted evaluation success.
3. On the selected pass call, inspect actual attached scores for
   `score_improves_vs_baseline`, `gates_ok_when_scar_applied`, and
   `drc_cleared_after_scar`. Distinguish server-attached scoring results from an
   ordinary `signals` dictionary embedded in output or summary.
4. Separately inspect Monitors / Signals if available. Record whether any Monitor
   exists, its enabled state and the operations it targets. Programmatic
   `apply_scorer` results do not prove an enabled UI Monitor.

Until these steps are complete, use the local fallback segment in the runbook.
If access succeeds but there are no relevant records, report that exact finding
before deciding whether a new live run is needed. Merely printing “Weave UI” is
insufficient: the wrapper deliberately continues when tracing/evaluation fails.
