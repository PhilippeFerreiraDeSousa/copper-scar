"""Export a compact, auditable action/outcome/write-back/proposal evidence chain."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];LOCAL=ROOT/'.local/copperhead'
ap=argparse.ArgumentParser();ap.add_argument('--prior',required=True);ap.add_argument('--following',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
def read(path):return json.loads(path.read_text())
def evidence(path):return dict(path=str(path.resolve()),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
p=LOCAL/'runs'/a.prior/'attempt.json';r=read(p);effects=read(Path(r['effects']));before=effects['missing_before'];after=effects['missing_after'];incident=set(r['action']['nets'])
changes={n:dict(before=before.get(n,0),after=after.get(n,0)) for n in sorted(before.keys()|after.keys()) if before.get(n,0)!=after.get(n,0)}
feedback=next(f for f in read(LOCAL/'loop/feedback.json') if f['attempt']==a.prior);snapshot=a.output/'persisted-feedback.json';snapshot.write_text(json.dumps(feedback,indent=2))
nextpath=LOCAL/'runs'/a.following/'attempt.json';following=read(nextpath);proposal=LOCAL/'runs'/a.following/'placement-proposal.json'
result=dict(prior_attempt=evidence(p),parent_board_sha256=r['before']['files']['pcbgolf.kicad_pcb'],prior_pose=r['action'].get('translation_mm'),prior_outcome={k:r['after'][k] for k in ('unconnected','errors','warnings','invariants_ok')},retained=r.get('became_incumbent',False),incident_net_changes={n:v for n,v in changes.items() if n in incident},other_net_changes={n:v for n,v in changes.items() if n not in incident},native_effects=evidence(Path(r['effects'])),persisted_feedback=evidence(snapshot),persisted_feedback_source=str(LOCAL/'loop/feedback.json'),following_attempt=evidence(nextpath),following_proposal=evidence(proposal),following_status=following['status'],feedback_link_present=a.prior in following['action']['feedback_used'],following_pose=dict(refs=following['action']['refs'],translation_mm=following['action']['translation_mm'],rotation_deg=following['action'].get('rotation_deg',0)),following_research_context=following['action'].get('research_context'),following_outcome={k:following.get('after',{}).get(k) for k in ('unconnected','errors','warnings','invariants_ok')},following_retained=following.get('became_incumbent',False),qualification='Evidence of recorded outcome and subsequent changed proposal. Human/agent circuit reasoning and queued hypotheses are distinct from automatic same-parent exclusion; no causal improvement claim follows from a geometric proxy.')
challenger=LOCAL/'proposals/can0-after-measured-rejection.json'
if challenger.exists():
 q=read(challenger);result['automatic_same_parent_exclusion']=dict(proposal=evidence(challenger),parent_matches=q['parent_board_sha256']==result['parent_board_sha256'],excluded_moves=q.get('excluded_moves'),next_translation_mm=q['translation_mm'],realized=False)
(a.output/'chain.json').write_text(json.dumps(result,indent=2))
rows='\n'.join(f"| {n} | {v['before']} | {v['after']} | {'Incident' if n in incident else 'Other affected net'} |" for n,v in changes.items())
text=f"""# Native feedback and subsequent placement evidence

The CAN0 group moved by {r['action']['translation_mm']} mm. Its matched unchanged-placement control had 55 missing pairs. The realized candidate had **{r['after']['unconnected']} missing pairs, {r['after']['errors']} physical errors and {r['after']['warnings']} warnings** and was rejected. It closed Net-(U5-CANH), but collateral failures outweighed that local repair.

| Net | Before | After | Scope |
|---|---:|---:|---|
{rows}

The immutable `persisted-feedback.json` is the actual matching record copied from the live feedback history. The following proposal lists the prior attempt in `feedback_used`: **{result['feedback_link_present']}**. It changes {following['action']['refs']} by {following['action']['translation_mm']} mm / {following['action'].get('rotation_deg',0)} degrees with other declared members fixed. Its context records the observed CAN0 collision damage and the circuit-aware review used to narrow the proposal.

Following realized attempt: `{a.following}`, status **{following['status']}**, outcome **{result['following_outcome']}**, retained **{result['following_retained']}**. A running attempt is not an evaluated gain.

Separately, rerunning the CAN0 generator against the same parent and persisted feedback excludes the rejected (+1,-1) move and selects (+0.5,-0.5). That demonstrates the automatic exclusion mechanism; this exported challenger has not itself been routed. Queue decisions also use circuit reasoning and must not be presented as a learned-model prediction.

`chain.json` contains exact source paths and SHA-256 hashes, both sets of net changes, the feedback link, and the next proposal/outcome. No valid-board or official-score claim is made.
"""
(a.output/'chain.md').write_text(text);print(json.dumps(result['following_outcome']))
