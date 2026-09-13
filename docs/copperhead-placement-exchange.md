# Future placement / routing exchange

Copperhead owns placement proposal generation and native placement checks. JITX owns incremental multilayer realization and routing diagnostics. This is a file-level contract for a future handoff, not an implemented shared runtime or permission to merge tracks.

A proposal identifies the exact parent board SHA-256 and constraint-file digests, component references plus native UUIDs, rigid group membership, and each proposed component pose in millimetres/degrees. It declares fixed components, preserved within-group offsets, outline and copper-layer constraints, affected nets by name and pin membership, and copper handling (retained/transformed items versus explicitly removed boundary-net items). It includes the native pre-route gate and the measured reason for proposing the move. A surrogate geometric gain is labeled as a proxy, never as connectivity or validity improvement.

The realization request includes a full-board routing scope, unchanged legal layer/via/rule definitions, an explicit effort budget, parent routed state, and the immutable proposed native board. An affected-net set tells the router where to invalidate stale copper; it does not restrict final evaluation to those nets.

The result identifies the request and exact input/output hashes, immutable routed board, actual changed copper/poses, elapsed effort, termination reason, eligible input scope and known per-net attempt coverage. It returns native missing endpoint pairs, physical errors, warnings and constraint gates; failures preserve their partial board and logs. Diagnostics should identify net, component/pad UUID, location/layer, failing phase and violated constraint. A router's heuristic label is not an established cause of failure.

Copperhead independently verifies the returned native CAD and retains or rejects it against the incumbent. Realization failure stays separate from placement illegality and from a completed but inferior routing result. Neither a lower geometric proxy nor a successful router exit can promote a physically invalid design. No Stage Two score is emitted before the existing validity gate passes.
