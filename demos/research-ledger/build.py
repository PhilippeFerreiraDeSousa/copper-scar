#!/usr/bin/env python3
"""Index existing evidence without copying CAD, running experiments or changing owners."""
import datetime,hashlib,json,os,shutil,subprocess
from pathlib import Path
OWNER=Path('/Users/philippe/dev/copper-scar-demo');N=OWNER/'.local/copperhead';O=Path('/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs');J=Path('/Users/philippe/dev/copper-scar-jitx/runs/local-route-failure-review');OUT=O/'optimizer-research-ledger';OUT.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def evidence(p,label=None):
 p=Path(p);assert p.is_file(),p
 return {'label':label or p.name,'path':str(p),'href':os.path.relpath(p,OUT),'sha256':digest(p),'bytes':p.stat().st_size}
def commit(ref,paths=()):
 h=subprocess.check_output(['git','rev-parse',ref],cwd=OWNER,text=True).strip();date=subprocess.check_output(['git','show','-s','--format=%aI',h],cwd=OWNER,text=True).strip()
 return {'commit':h,'commit_date':date,'source_hashes':[{'path':str(OWNER/p),'git_path':p,'sha256':hashlib.sha256(subprocess.check_output(['git','show',h+':'+p],cwd=OWNER)).hexdigest(),'basis':'committed source bytes'} for p in paths]}
def working(paths):return {'commit':None,'commit_date':None,'status':'Uncommitted/private source at capture; no implementation commit verified','source_hashes':[{'path':str(p),'sha256':digest(p),'basis':'current file bytes at capture'} for p in paths]}
def attempt(uid):return json.loads((N/'runs'/uid/'attempt.json').read_text())
def frozen_source(uid):
 d=attempt(uid);p=N/'runs'/uid/'tool-source/scripts/copperhead_campaign.py';assert digest(p)==d['tool_source_hashes']['scripts/copperhead_campaign.py']
 return {'commit':d.get('source_revision'),'commit_date':None,'status':'Recorded checkout revision; frozen tool hash is authoritative and may include uncommitted changes','source_hashes':[{'path':str(p),'sha256':digest(p),'basis':'frozen run source, checked against receipt'}]}
def inp(p,label):return evidence(p,label)
rows=[]
def row(id,title,kind,hypothesis,implementation,prior,new,inputs,artifacts,result,disposition,unproven,date=None):
 rows.append(dict(id=id,title=title,evidence_class=kind,hypothesis=hypothesis,implementation=implementation,protocol_before=prior,protocol_after=new,inputs=inputs,artifacts=artifacts,result=result,disposition=disposition,unproven=unproven,event_date=date,event_date_basis='explicit run/commit timestamp' if date else 'Unknown exact execution timestamp; file modification time is not substituted',matched_performance_comparison=False,trained_model_update=False))
row('via-persistence','Via options survive export and feedback stays recipe-scoped','Correctness',
 'A board containing 450/200 vias does not prove the next DSN permits the router to create that size; old recipe failures must not exclude a pose under a changed recipe.',
 commit('2ffe377',['copper_scar/tools/copperhead/routing_options.py','scripts/copperhead_effective_options.py']),
 'Exports could reset use_via to 600/300 only; existing small vias persisted separately from new-via eligibility.',
 'Reapply candidate options after each export; verify actual loaded Java class; scope feedback by effective context digest.',
 [inp(N/'reports/routing-option-persistence/group_pose/pcbgolf.kicad_pcb','Exact group-pose test board'),inp(N/'reports/routing-option-persistence/via_seed/pcbgolf.kicad_pcb','Exact via-seed test board')],
 [evidence(N/'reports/routing-option-persistence/regression.json'),evidence(N/'reports/routing-option-context/regression.json')],
 'Export and re-export preserve 600/300 + 450/200 eligibility for two action paths. Same-context failed pose stays excluded; changed-context pose becomes eligible. No router started.',
 'Keep correctness fix; performance untested','No measured convergence benefit. Does not retroactively change the seven-seed run, whose default permitted newly created 600/300 vias only.')
row('saved-fill','Evaluate the board that is actually saved','Correctness',
 'In-memory refill can report clean copper while saved fills still fail native DRC.',commit('45ade88',['copper_scar/tools/copperhead/stage1.py']),
 'Final DRC refilled only in memory; historical154b stored45/8/18 versus refilled45/0/18.',
 'Native refill + save first, then independent no-refill saved-file DRC before final hash, retention and publication.',
 [inp(N/'reports/topology-replan-regression/wrong_removal_net/pcbgolf.kicad_pcb','Unmodified historical154b'),inp(N/'reports/saved-fill-regression/candidate/pcbgolf.kicad_pcb','Saved54eff regression board')],
 [evidence(N/'reports/saved-fill-regression/run/saved-fill.json'),evidence(N/'reports/saved-fill-regression/run/saved/evaluation.json'),evidence(O/'saved-fill-pipeline-audit.md')],
 'Exact54eff saved board checks45/0/18 without refill. Fatal save/recheck failure cannot promote; independent audit and negative save probes pass.',
 'Keep correctness fix','No new connection or placement benefit. Existing45 opens remain.',date='2026-09-13T14:00:47.194540+00:00')
uid='stage1-20260913-073500-b3f12a';run=N/'runs'/uid;d=attempt(uid)
row('original-connectivity','Compare final connectivity with the original pre-ripup board','Correctness',
 'A replan must restore original pad groups; comparing only the deliberately split intermediate would excuse damage.',commit('c9cbd7e',['copper_scar/tools/copperhead/stage1.py','scripts/copperhead_topology_replan.py']),
 'Ordinary topology changes had no explicit declared ripup/replan contract.',
 'Bounded declared removal plus new seeds; final no-split compares ORIGINAL input, while final via preservation compares post-replan snapshot. Later scoped width and target-join gates also apply.',
 [inp(run/'input/pcbgolf.kicad_pcb','Original45-open parent'),inp(run/'topology-replan-project/pcbgolf.kicad_pcb','Deliberately split pre-route board'),inp(Path(d['candidate'])/'pcbgolf.kicad_pcb','Final65f453 board')],
 [evidence(run/'attempt.json'),evidence(run/'final-pad-partitions.json'),evidence(run/'final-via-geometry.json'),evidence(run/'final-topology-widths.json')],
 'Actual600 s configured trial ended46/0/22 after614.674 s command time. CAN2 unjoined and original+5V group split; retention rejected despite via/width checks passing.',
 'Keep guard; reject tested candidate','This is a useful rejection, not convergence progress. No blanket final track freeze; scoped electrical-width suitability remains unproved.',date=d['finished_at'])
row('strict-contract','Require exact geometry declarations and recipe binding','Correctness',
 'Missing or contradictory geometry/recipe declarations must not silently pass.',commit('9bed884',['scripts/copperhead_topology_replan.py','scripts/copperhead_via_geometry.py','copper_scar/tools/copperhead/topology_contract.py']),
 'Removal geometry optional, supplied anchor fields ignored, missing recipe filled automatically, reduced geometry omitted layer diameters and arc details.',
 'Mandatory matching recipe and geometry; anchor layer/native island checks; all-layer via diameters and arc midpoint; complete authored-item comparison before routing. a976d3e additionally hashes width evidence and requires nonempty all-touched-net scope.',
 [inp(N/'reports/topology-replan-strict-regression/proposal.json','Strict explicit proposal'),inp(N/'reports/topology-replan-strict-regression/candidate/pcbgolf.kicad_pcb','Strict0894088 smoke')],
 [evidence(N/'reports/topology-replan-strict-regression/negative-checks.json'),evidence(O/'topology-replan-strict-review-proof.json'),evidence(O/'topology-replan-review.md')],
 'Six missing/contradictory cases reject before board change; exact1 removal + 2 vias and all other authored subtrees preserved. Original P2 findings closed; width hardening verified at a976d3edbf34813599fab8004d0ac8af17852959.',
 'Keep correctness fix','Smoke is not a full-router performance comparison. Passing tests is not improved convergence.')
row('placement-coverage','Resistor-only adaptive coverage is a real search limitation','Coverage gap',
 'The executable loop can be too narrow to find useful placement changes even if its evaluation works.',commit('1aee3e8',['scripts/copperhead_campaign.py']),
 'Broad component/global proposals had failures; protected circuit roles needed limits.',
 'Adaptive proposals limited to resistors, protecting oscillator R26; other parts require explicit reviewed intent. Six component-move rows in the latest window move only R37, R71, R123 or R12.',
 [inp(O/'latest-loop-experiments/data.json','Frozen eleven-experiment index')],
 [evidence(OWNER/'scripts/copperhead_campaign.py','Current campaign source at capture'),evidence(O/'latest-loop-experiments/README.md')],
 'One retained missing-pair gain (R37); R12 has no count gain; repeated R123 and R71 moves rejected. These observations do not establish broad placement optimization.',
 'Open research gap','No diverse-component controlled benchmark, policy-convergence result, or automated research loop. Do not equate executable loop with effective optimizer.')
row('dsn-contacts','Expose exact mid-trace contacts without adding copper','Correctness',
 'Native same-net connectivity may not survive DSN import when a via or junction lies inside a wire segment.',
 working([OWNER/'copper_scar/tools/copperhead/dsn_contacts.py',OWNER/'scripts/copperhead_effective_options.py',OWNER/'scripts/copperhead_contact_targets.py',OWNER/'scripts/native/CopperheadViaRules.java']),
 'Unpartitioned native wire contacts imported with incomplete pin sets; two new-anchor checks alone missed other groups.',
 'Split only exact collinear same-net wire contacts; byte reversal and idempotence checks; v2 version+net scope; native island representative versus Java pin-set gate before route.',
 [inp(N/'reports/contact-normalizer-integration-v2/can2/via-definition/island_check/contact-input.dsn','CAN2 exact DSN input'),inp(N/'reports/contact-normalizer-integration-v2/can2-power/via-definition/island_check/contact-input.dsn','CAN2+power exact DSN input')],
 [evidence(O/'contact-normalizer-review-proof.json'),evidence(O/'contact-normalizer-review.md'),evidence(N/'reports/contact-normalizer-integration-v2/can2/via-definition/island_check/loaded-via-rules.json'),evidence(N/'reports/contact-normalizer-integration-v2/can2-power/via-definition/island_check/loaded-via-rules.json')],
 'Independent exact polyline/metadata/byte replay and idempotence pass:4 CAN2 or 6 CAN2 + power wires. CAN2 pin sets match. Power native 19 pins → Java 6 fails; second 3 → 3 passes.83 tests / 1 skip is correctness evidence only.',
 'CAN2 bounded parity passes; power recipe blocked','No fresh accepted full-route outcome or convergence benefit. Sampled islands require vias; pad-only/track-only islands are not universally covered. Source snapshots identify current code at capture; the exact historical Python implementation revision for the integration cases was not frozen and remains unknown.')
row('npth-clearance','Correcting double-counted NPTH clearance does not fix A11','Correctness',
 'Pre-expanded locating-hole geometry plus runtime hole clearance could explain local endpoint insertion failure.',
 working([J/'normalize_probe.py',J/'DiagnoseA11.java',J/'ReadHoleEncoding.java']),
 'J5 right 0.66 mm NPTH encoded as six 1160 um circles; in local override context raw 580 um radius plus250 um clearance.',
 'Clone only J5 image, normalize exact six circles1160 → 660 um; keep250 um hole rule. Compare local A11 insertion and loaded geometry. Separate hole0 probe retains200 um default clearance.',
 [inp(J/'input.dsn','Original paired DSN'),inp(J/'normalized-j5-only.dsn','Bounded normalized DSN'),inp(J/'native-npth-binding.json','Native hole binding')],
 [evidence(J/'README.md'),evidence(J/'normalization.json'),evidence(J/'normalized-result.json'),evidence(J/'normalized-hole-encoding.json'),evidence(J/'hole-zero-result.json')],
 'Normalized raw 330 um radius+250 um rule proved; A11 still FAILED with no new items. Original-hole/zero-override probe also fails. Double clearance is not a sufficient explanation.',
 'Preserve negative result; reject sufficient-cause hypothesis','Local25 um edge/125 um F.Cu/no-vias/no-shove probe differs from full500 um edge context. No accepted A11 route or general full-router diagnosis. Exact test timestamp unknown in inspected receipts; reviewer reports Sep13 07:55–07:57Pacific.')
row('local-pad-api','Stock local endpoint API routes B2 but not A11','Bounded local result',
 'A stock pad-to-own-via endpoint call could realize a short native-qualified attachment that bulk routing missed.',
 working([N/'reports/local-route-api/CopperheadLocalRoute.java']),
 'Paired endpoints lacked a qualified engine-produced local route.',
 'Exact pad-to-own-via F.Cu 125 um, max 2 mm, no ripup/shove, no new vias; reverse endpoint order as a bounded check.',
 [inp(J/'input.dsn','Frozen paired DSN input'),inp(O/'connector-escape-diagnosis/paired-candidate/proposal.json','Exact paired proposal')],
 [evidence(N/'reports/local-route-api/proof.json'),evidence(N/'reports/local-route-api/result.json'),evidence(N/'reports/local-route-api/reversed-result.json'),evidence(N/'reports/local-route-api/native-full-check/saved/evaluation.json'),evidence(J/'provenance.json')],
 'B2 routed 0.900269119 mm in 0.140 s; native 48 → 47/0/21. A11 failed insertion in both orders and added no items; same SES hash. Paired acceptance false.',
 'Keep bounded B2 proof; A11 unresolved','No trunk restoration, broad optimizer improvement or paired success. Private Java hash b7c1613a58b27f10c897b7e85a1d576f1a082854084cf31c27a64756bd508427; no implementation commit verified.')
uid='stage1-20260913-044612-074e42';r=N/'runs'/uid;d=attempt(uid)
row('r37-placement','R37 pose plus full routing gives a measured gain','Full-route observation',
 'Moving R37 could improve the retained board after a fixed-budget full-route continuation.',frozen_source(uid),
 'Parent 54/0/18; R37 (171.25,98.5,0deg), existing copper retained.',
 'Move R37 (-23,-3) mm, +90 degrees; detach incident copper; six-layer whole-board600 s / 100-pass continuation.',
 [inp(r/'input/pcbgolf.kicad_pcb','Exact54-open original'),inp(r/'placement-project/pcbgolf.kicad_pcb','Actual pre-route pose'),inp(Path(d['candidate'])/'pcbgolf.kicad_pcb','Final53-open board')],
 [evidence(r/'attempt.json'),evidence(O/'demo-final/placement-gain/summary.json') if (O/'demo-final/placement-gain/summary.json').exists() else evidence(O/'latest-loop-experiments/data.json')],
 'Actual pose changed one component. Pre-route 57/0/21; final 53/0/19 retained versus 54/0/18 parent.600 s configured, 615.637 s route command.',
 'Retain candidate; attribution remains limited','No matched unchanged-parent full-route control isolates placement benefit; no convergence result or manufacturing acceptance.',date=d['finished_at'])
u1='stage1-20260913-055432-134c1a';u2='stage1-20260913-061700-fbe016';d=attempt(u2)
row('seed-feedback','J5 success gates the seven-seed heuristic expansion','Full-route observation',
 'A verified explicit-seed attachment gain can make a broader compatible seed batch eligible.',commit('5d23c220',['scripts/copperhead_campaign.py']),
 'Single J5 CAN0_H explicit seed +fullroute 52 → 51; seven-site expansion is not eligible without retained precedent and hash-bound connectivity proof.',
 'Reviewed catalog guard requires retained seed gain and all-target proof; current-parent targets revalidated. R12 intermediate 51-count tie is not an electrical gain. Then seven explicit seeds +whole-board600s route.',
 [inp(N/'runs'/u1/'input/pcbgolf.kicad_pcb','Single-seed parent52'),inp(N/'runs'/u2/'input/pcbgolf.kicad_pcb','Batch original51 parent'),inp(N/'runs'/u2/'via-seed-project/pcbgolf.kicad_pcb','Explicit seven-seed pre-route board')],
 [evidence(N/'runs'/u1/'final-seed-connectivity.json'),evidence(N/'runs'/u1/'attempt.json'),evidence(N/'runs'/u2/'attempt.json'),evidence(O/'demo-final/seed-gain/summary.json') if (O/'demo-final/seed-gain/summary.json').exists() else evidence(O/'jitx-demo/seven-seed-final-audit.json')],
 'Seven added vias, six missing pairs removed:51 → 45/0/18; CAN0_H groups 4 → 1 and CAN2_H 5 → 2, remaining separate group persists. Frozen campaign SHA 99d8d245c86df9ba4b7f7e3a70e0201955019dc0d2d977601d2b5f8b84ff13ad binds executed guard.',
 'Retain board result and heuristic eligibility rule','This is catalog/policy feedback, not model training. No unchanged-parent control or trained-policy comparison. Historical batch allowed new 600/300 creation only; explicit 450/200 seeds persisted.',date=d['finished_at'])
contract=[
 'Freeze original parent board/project/support hashes, constraints and eligible layers; retain immutable inputs.',
 'Record candidate-policy/source hash, selection version, normalization/via recipe and actual loaded engine context. This is action-policy versioning, not trained-model updating.',
 'Use the same router implementation, configured wall-time/pass budget and execution settings; record actual elapsed time and termination.',
 'Where available, compare a fresh unchanged-parent baseline against the changed candidate under that protocol. Explicitly mark absent matched control; do not imply one.',
 'Record actual component pose updates, via additions/removals/all-layer geometry, and pre-route copper changes from CAD, not proposed intent alone.',
 'Persist fills, then measure exact saved CAD: opens, physical errors, manufacturing findings, original pad-group preservation and scoped width/target gates.',
 'Publish both positive and negative outcomes, wall time and artifacts. An implementation-only change stays correctness/implementation status until the required performance comparison exists.',
 'Predeclare keep/reject criteria and evaluation sample set. No convergence claim from a unit-test pass, code push, isolated gain or proxy distance alone.'
]
for r in rows:
    for source in r['implementation']['source_hashes']:
        if source.get('git_path'):
            content=subprocess.check_output(['git','show',r['implementation']['commit']+':'+source['git_path']],cwd=OWNER)
        else:content=Path(source['path']).read_bytes()
        assert hashlib.sha256(content).hexdigest()==source['sha256']
        target=OUT/'source-snapshots'/(source['sha256']+Path(source['path']).suffix)
        target.parent.mkdir(exist_ok=True);target.write_bytes(content)
        source['snapshot_href']=str(target.relative_to(OUT))
    r['test_runs']=[]
    for e in r['artifacts']:
        if Path(e['path']).name!='attempt.json':continue
        d=json.loads(Path(e['path']).read_text()); frozen=[]
        for name in ['copper_scar/tools/copperhead/stage1.py','scripts/copperhead_campaign.py']:
            expected=d.get('tool_source_hashes',{}).get(name)
            source=Path(e['path']).parent/'tool-source'/name
            if expected:
                assert source.is_file() and digest(source)==expected
                frozen.append({'path':str(source),'sha256':expected})
        r['test_runs'].append({'attempt':d['attempt'],'recorded_checkout_revision':d.get('source_revision'),'frozen_source_hashes':frozen,'started_at':d.get('started_at'),'finished_at':d.get('finished_at'),'action_policy':d.get('policy'),'selection_policy':d.get('selection_policy_version'),'effective_context':d.get('realization_context'),'routing_budget_seconds':d.get('routing_scope',{}).get('effort_limit_seconds'),'note':'Frozen source hashes are authoritative; recorded revision may have included uncommitted changes.'})
data={'schema_version':1,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Retrospective unified index of existing optimizer research; no new experiments or research automation created','summary':'Executable placement/topology → full routing → native evaluation exists; broad effectiveness and convergence are not established. This ledger separates correctness work, coverage gaps and observed board results.','matched_convergence_comparisons_documented':0,'scope_note':'Zero refers to these indexed research claims, not an exhaustive assertion about every uninspected project artifact.','prospective_evaluation_contract':contract,'rows':rows}
(OUT/'ledger.json').write_text(json.dumps(data,indent=2));(OUT/'ledger.js').write_text('window.LEDGER='+json.dumps(data)+';')
md=['# Optimizer research ledger',data['summary'],'This is an index of existing work, not a new optimizer, benchmark harness or automated research loop. Evidence is linked in place; no CAD megacopies. Unknown dates and commits remain unknown.','']
for r in rows:
 md += [f"## {r['title']}",f"**{r['evidence_class']} · {r['disposition']}**",r['hypothesis'],f"Implementation: `{r['implementation'].get('commit') or 'UNKNOWN / private or uncommitted'}`. Exact source and artifact hashes are in ledger.json.",f"Prior: {r['protocol_before']}",f"New: {r['protocol_after']}",f"Result: {r['result']}",f"Unproven: {r['unproven']}", 'Evidence: '+ ' · '.join(f"[{e['label']}]({e['href']})" for e in r['artifacts']), '']
md+=['## Prospective evaluation contract']+[f'{i+1}. {x}' for i,x in enumerate(contract)]
(OUT/'README.md').write_text('\n\n'.join(md));shutil.copy2(Path(__file__).with_name('index.html'),OUT/'index.html')
print(json.dumps({'rows':len(rows),'output':str(OUT),'unique_evidence_paths':len({x['path'] for r in rows for x in r['inputs']+r['artifacts']})}))
