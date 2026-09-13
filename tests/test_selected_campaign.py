import hashlib,importlib.util,json,subprocess
from pathlib import Path
import pytest
HERE=Path(__file__).parent
script=HERE/'copperhead_selected_campaign.py'
if not script.exists():script=HERE.parent/'scripts/copperhead_selected_campaign.py'
spec=importlib.util.spec_from_file_location('consumer',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def fixture(tmp_path):
 root=tmp_path/'repo';root.mkdir();folder=root/'policies';folder.mkdir()
 configs=[dict(id='placement_first',version=1,ranking='placement_then_endpoint'),dict(id='island_first',version=1,ranking='split_burden_then_topology_then_endpoint')]
 for cfg in configs:(folder/(cfg['id']+'.json')).write_text(json.dumps(cfg))
 subprocess.run(['git','init','-q',str(root)],check=True);subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Fixture policy'],check=True)
 commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
 policies=[dict(**cfg,source_path=str(folder/(cfg['id']+'.json')),source_sha256=m.digest(folder/(cfg['id']+'.json')),source_commit=commit) for cfg in configs];policy=policies[0]
 board=tmp_path/'board.kicad_pcb';board.write_text('fixture board bytes');decision={'kept_policy':policy['id']};dp=tmp_path/'decision.json';dp.write_text(json.dumps(decision))
 protocol={'N':3};protocol_sha=hashlib.sha256(json.dumps(protocol,sort_keys=True).encode()).hexdigest();experiment='test-fixture'
 (tmp_path/'manifest.json').write_text(json.dumps({'status':'completed','decision':decision,'common_protocol':protocol,'common_protocol_sha256':protocol_sha,'experiment_id':experiment,'policies':policies}))
 events=[{'type':'experiment_started','common_protocol':protocol,'common_protocol_sha256':protocol_sha}]
 for arm in policies:
  events.extend({'type':'lower_completed','policy':arm,'lower':{'index':i}} for i in [1,2,3]);events.append({'type':'policy_completed','policy':arm,'lower':{'index':3,'retained_board_path':str(board),'retained_board_sha256':m.digest(board)}})
 events.append({'type':'policy_decision','decision':decision})
 for e in events:e['experiment_id']=experiment
 (tmp_path/'events.jsonl').write_text('\n'.join(json.dumps(e) for e in events));selection={'policy':policy,'decision_path':str(dp),'next_campaign_initial_board':str(board)};sp=tmp_path/'selected-policy.json';sp.write_text(json.dumps(selection));return sp,board,root

def test_exact_committed_config_and_completed_board_are_consumed(tmp_path):
 sp,board,root=fixture(tmp_path);assert m.verify_selection(sp,root)[3]['verified']

def test_ranking_tamper_rejected_even_with_same_id_version(tmp_path):
 sp,_,root=fixture(tmp_path);x=json.loads(sp.read_text());x['policy']['ranking']='split_burden_then_topology_then_endpoint';sp.write_text(json.dumps(x))
 with pytest.raises(AssertionError,match='configuration differs'):m.verify_selection(sp,root)

def test_changed_retained_board_rejected(tmp_path):
 sp,board,root=fixture(tmp_path);board.write_text('changed')
 with pytest.raises(AssertionError):m.verify_selection(sp,root)

def test_decision_must_match_append_only_outcome(tmp_path):
 sp,_,root=fixture(tmp_path);events=tmp_path/'events.jsonl';x=[json.loads(l) for l in events.read_text().splitlines()];x[-1]['decision']['kept_policy']='island_first';events.write_text('\n'.join(json.dumps(e) for e in x))
 with pytest.raises(AssertionError,match='append-only'):m.verify_selection(sp,root)

def test_incomplete_other_arm_rejected(tmp_path):
 sp,_,root=fixture(tmp_path);events=tmp_path/'events.jsonl';x=[json.loads(l) for l in events.read_text().splitlines()];x=[e for e in x if not(e['type']=='lower_completed' and e['policy']['id']=='island_first' and e['lower']['index']==3)];events.write_text('\n'.join(json.dumps(e) for e in x))
 with pytest.raises(AssertionError,match='Incomplete or duplicate'):m.verify_selection(sp,root)
