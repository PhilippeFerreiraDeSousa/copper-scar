# Native acceptance and evidence corrections

The nine-ground-terminal attempt `stage1-20260913-043321-c091d4` finished at 54 missing pairs, zero error-severity findings and 18 warnings. It produced no native pad-partition improvement. Its final airwire proxy 1026.044 was below the stale incumbent cache 1026.721 but above the same run's fresh measurement of that incumbent, 1023.898. The original controller therefore incorrectly promoted a freshly measured regression.

The original attempt remains immutable. `retention-correction.json` beside it records both comparisons and restores candidate `stage1-20260913-042140-425473`, board SHA `785d2ebc0d4d98e781b07c3d04849f7e2469f037c47ebecd4a561f05129901ce`. Dashboard and replay readers apply this explicit correction without rewriting historical attempt bytes. W&B retains its historical upload and publishes a separate correction summary and Weave event; the verification receipt marks effective retention false. The nine-ground trial remains visible as a completed negative result.

Promotion now requires improvement against the freshly measured input as well as the incumbent. When the input and incumbent design hashes match, the fresh measurement replaces the cached tie-break in either direction. A different exploratory parent still compares against the separate incumbent. Airwire changes remain diagnostic and never imply manufacturing or electrical qualification.

Two additional acceptance boundaries were hardened through bounded fault injection:

- A nonzero backend exit or external process timeout cannot be hidden by a successful wrapper exit, even if a partial SES exists. Both the wrapper and stage controller reject it while preserving evidence. Normal backend exit zero at its internal routing effort limit still proceeds to independent native evaluation.
- A publication/viewer/deadline failure after native evaluation and retention is complete records a postprocessing error. It does not relabel the native result as failed, duplicate its feedback, or leave a supposedly failed candidate retained.

The retained54 board has an overlapping CAN2_L drill pair: native `hole_to_hole`, required0.25mm, actual0mm. Its warning severity does not make it acceptable for manufacturing. Native evaluations now report severity-independent manufacturing findings separately from the unchanged historical v1 search metrics. Project rule severities and dimensions are preserved. The final validity gate remains false and Stage2 remains disabled; zero error-severity findings is not a manufacturability claim.

Validation: 57 tests passed, one skipped. Independent read-only review reproduced the original failure boundaries and verified their corrected behavior without routing or changing CAD. No failed-backend promotion or postprocessing inconsistency was found in the bounded completed v9 history; the nine-ground stale-cache retention is the concrete historical correction.
