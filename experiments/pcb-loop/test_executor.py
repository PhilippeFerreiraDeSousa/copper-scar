from pathlib import Path
import importlib.util,json
import pytest
spec=importlib.util.spec_from_file_location('loop_executor',Path(__file__).with_name('executor.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def request(tmp_path,stage=1):
 source=tmp_path/'source';source.write_text('immutable');return {'size_family':'test-fixture','stage':stage,'source_epoch':'raw','source_sha':'fixture','required_gates':['native','identity'],'eligible_layers':['F.Cu','B.Cu'],'via_options':[[.6,.3]],'route_budget':{'seconds':1},'action':{'primitive':'test'},'source_files':[source],'incumbent':{'valid':True,'official_score':100}}

def backend(gates,score=None,qualified=False,mutate=None):
 def run(req,folder,emit):
  report=folder/'native.json';report.write_text('{}')
  if mutate:Path(req['source_files'][0]).write_text('drift')
  return {'gates':{g:{'passed':True,'report':str(report)} for g in gates},'official_score':score,'official_score_qualified':qualified,'diagnostic_retained':True}
 return run

def test_first_valid_stage_one_stops(tmp_path):
 r=module.execute_candidate(request(tmp_path),backend(['native','identity']),tmp_path/'run');assert r['valid'] and r['stop_stage_one'] and r['handoff_stage']==2

def test_diagnostic_retention_never_masks_missing_gate(tmp_path):
 r=module.execute_candidate(request(tmp_path),backend(['native']),tmp_path/'run');assert r['diagnostic_retained'] and not r['valid'] and not r['stop_stage_one']

def test_source_drift_fails_acceptance(tmp_path):
 r=module.execute_candidate(request(tmp_path),backend(['native','identity'],mutate=True),tmp_path/'run');assert not r['valid'] and r['source_drift']

@pytest.mark.parametrize('score,qualified,retained',[(90,True,True),(110,True,False),(90,False,False),(float('nan'),True,False)])
def test_stage_two_only_qualified_lower_score(tmp_path,score,qualified,retained):
 r=module.execute_candidate(request(tmp_path,2),backend(['native','identity'],score,qualified),tmp_path/'run');assert r['retained']==retained;assert not r['stop_stage_one']
 if not qualified or score!=score:assert r['official_score'] is None
