"""Acceptance-focused tests: incomplete comparisons, rejection and event integrity."""
import json,tempfile,unittest
from pathlib import Path
from model import fold,read_events
class TestProjection(unittest.TestCase):
 def setUp(self):self.manifest={'experiment_id':'test','common_protocol':{'N':3},'policies':[{'id':'p'}]};self.events=[]
 def emit(self,typ,lower):self.events.append({'event_id':str(len(self.events)),'experiment_id':'test','timestamp_utc':'2026-09-13T00:00:00+00:00','policy':{'id':'p'},'type':typ,'lower':lower})
 def test_rejection_keeps_best_and_incomplete_has_no_cost_at_n(self):
  self.emit('policy_started',{'index':0,'nativecost':{'opens':45},'retainedbest':{'opens':45,'pad_groups_preserved':True}})
  self.emit('lower_completed',{'index':1,'status':'completed_rejected','nativecost':{'opens':44,'pad_groups_preserved':False},'retainedbest':{'opens':45,'pad_groups_preserved':True},'retained':False})
  self.emit('lower_started',{'index':2})
  p=fold(self.manifest,self.events)['policies'][0];self.assertEqual([x['best']['opens'] for x in p['points']],[45,45]);self.assertFalse(p['points'][1]['attempted']['pad_groups_preserved']);self.assertIsNone(p['cost_at_n']);self.assertEqual(p['completed_decisions'],1)
 def test_screen_decisions_count_without_invented_routes(self):
  for i in range(1,4):self.emit('lower_completed',{'index':i,'status':'precheck_rejected','retainedbest':{'opens':45},'retained':False,'routed_dispatch_count':0})
  p=fold(self.manifest,self.events)['policies'][0];self.assertEqual(p['cost_at_n']['opens'],45);self.assertEqual(p['completed_decisions'],3);self.assertEqual(p['routed_completed'],0);self.assertEqual(p['routed_dispatch_count'],0)
 def test_partial_tail_and_conflicting_id(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'events.jsonl';p.write_text('{"event_id":"one"}\n{"event_');raw,events=read_events(p);self.assertEqual(len(events),1);self.assertTrue(raw.endswith(b'\n'))
   p.write_text('{"event_id":"one"}\n{"event_id":"one","changed":true}\n')
   with self.assertRaises(AssertionError):read_events(p)
if __name__=='__main__':unittest.main()
