# R37 CMD pull-up placement result

Attempt `stage1-20260913-044612-074e42` reduced missing native connection pairs from54 to53 after a single-component placement change followed by the full600-second routing budget. Final native checks report zero error-severity findings,19 warnings and preserved schematic/pad/reference invariants. The backend returned0 with no external timeout. The candidate became the retained partial board.

The exact starting board was `785d2ebc0d4d98e781b07c3d04849f7e2469f037c47ebecd4a561f05129901ce`. Native diagnostics showed R37.2 isolated on Net-(J2-CMD), while J2.3 and R42.2 were already connected. Its representative approach to that branch was25.089mm. R37.1 belonged to the main+3V3 island, so relocation also had to restore that attachment.

The bounded KRT pose screen selected R37 center(171.25,98.5)→(148.25,95.5)mm and rotation0→90degrees. All other244component poses stayed fixed. The candidate approach distance became1.570mm. These distances are geometric diagnostics, not routed length or validity predictions.

Applying the pose detached two+3V3 track items at the old pad. Native collision cleanup removed one CH2_SBU1_IGN track explicitly identified by the native short/clearance findings. The pre-route candidate had57 missing pairs, zero physical errors and21warnings. All removal UUIDs, geometry and original findings remain in `placement-search.json` and `placement-collisions/`.

After full routing, CMD missing pairs changed1→0. No other net's missing-pair count increased; the detached+3V3 and collateral net counts recovered. Final board SHA-256 is `7cae9a8ec99e95450992d9fa620c890d5ac720f4e29c2b404afd14b3d725e0c4`, aggregate design hash `1cb2022c358f2b0978058a5777e53c0e140bb257273e607e81c094d0020fa083`. W&B/Weave board media and hashes were read back and verified.

There was no fresh unchanged-placement600-second control on this exact54parent; the original55control and intervening fixed-pose topology trials provide context, not a clean causal isolation of placement. The observed result is a completed placement-plus-routing gain. Independent all-net pad-partition review is separate evidence from the per-net missing counts.

The final board remains incomplete and has an overlapping CAN2_L drill warning. Zero error-severity findings is not a manufacturability claim. A subsequent explicitly scoped via-consolidation candidate removes one named redundant via only if every native pad partition survives, then checks the original hole rule before another full routing pass. No rule or project severity is relaxed.
