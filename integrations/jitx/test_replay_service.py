import unittest,json,hashlib
from replay_service import completed_records,select_history,logical
class ReplayHistoryTests(unittest.TestCase):
 def record(self,name,**kw):return {'candidate':'/candidates/'+name,'policy_version':'jitx-feasibility-v3',**kw}
 def snapshots(self,records):return {hashlib.sha256(json.dumps(r,indent=2).encode()).hexdigest():{'evaluation_sha256':str(i)} for i,r in enumerate(records) if r.get('candidate')}
 def test_partial_tail_is_not_a_completed_record(self):
  self.assertEqual(completed_records(b'{"a":1}\n{"a":'),[{'a':1}])
 def test_recheck_keeps_action_order_and_latest_measurement(self):
  old=self.record('stage1-routed-002',policy_version='jitx-feasibility-v2');a=self.record('stage1-routed-002-v2-ids-v3',measurement=1);b={**a,'measurement':2};base=self.record('stage1-baseline-v4-ids-v3');new=self.record('iteration-009-power-neighborhood-routed')
  rows=[old,base,a,new,b];steps=select_history(rows,self.snapshots(rows));self.assertEqual([s['source_action'] for s in steps],['stage1-baseline','stage1-routed-002','iteration-009-power-neighborhood-routed']);self.assertEqual(steps[1]['evaluation']['measurement'],2)
 def test_unpublished_capture_excluded_failures_and_unreliable_kept(self):
  a=self.record('stage1-baseline-v4-ids-v3');b=self.record('trial-input',evaluation_reliable=False);c=self.record('trial-routed');failure={'error':'native crash','proposal':{'id':'failed'}}
  steps=select_history([a,failure,b,c],self.snapshots([a,b]));self.assertEqual(len(steps),3);self.assertTrue(steps[1]['held']);self.assertFalse(steps[2]['evaluation']['evaluation_reliable'])
if __name__=='__main__':unittest.main()

class ReplayQueueTests(unittest.TestCase):
 def test_newer_request_is_queued_during_render(self):
  import tempfile
  from pathlib import Path
  from unittest.mock import patch
  import replay_service as service
  request={'key':'new','run':'/unused','captured_at':2,'cutoff_checkpoint':'newest','cutoff_record_index':4,'cutoff_time':2,'earliest':'baseline'}
  with tempfile.TemporaryDirectory() as tmp,patch.object(service,'L',Path(tmp)),patch.object(service,'status',return_value={'state':'building','key':'old'}),patch.object(service,'freeze',return_value=request):
   result=service.start();self.assertEqual(result['queued_cutoff'],'newest');self.assertEqual(json.loads((Path(tmp)/'replay-pending.json').read_text()),request)
