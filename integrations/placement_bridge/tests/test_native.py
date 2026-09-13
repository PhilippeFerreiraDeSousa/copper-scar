"""Offline native identity and uncertain-worker failure gates (requires JITX)."""
from pathlib import Path
import asyncio
import copy
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import fixture_control as native
from jitx_adapter import mapping
FIXTURE=Path(__file__).parent/'fixtures'

class NativeTests(unittest.TestCase):
    def setUp(self):
        self.messages=json.loads((FIXTURE/'02-parent/final.json').read_text())
        self.request=json.loads((FIXTURE/'request.json').read_text())
    def test_current_native_ids_resolve(self):self.assertEqual(len(mapping(self.messages,self.request)),8)
    def test_wrong_native_pose_rejected(self):
        b=next(m['body'] for m in self.messages if m['type']=='board')
        b['module']['groups'][0]['pose']['center']['x']+=1
        with self.assertRaisesRegex(ValueError,'parent pose'):mapping(self.messages,self.request)
    def test_wrong_native_membership_rejected(self):
        n=next(m['body']['nets'] for m in self.messages if m['type']=='nets' and m['body'].get('complete'))
        n[0]['name']='wrong'
        with self.assertRaisesRegex(ValueError,'net membership'):mapping(self.messages,self.request)
    def test_timeout_keeps_uncertainty_and_refuses_next_controller(self):
        class Client:
            def route(self,path):return self
            async def request(self,message):
                if message.type=='reposition':raise TimeoutError('injected unresolved native request')
                async def empty():
                    if False:yield
                return empty()
        class Runtime:
            def __init__(self,**kw):self._client=Client()
            async def __aenter__(self):return self
            async def __aexit__(self,*args):pass
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);(base/'bridge_fixture').mkdir();(base/'bridge_fixture/design.py').write_text('# test')
            (base/'designs'/native.DESIGN).mkdir(parents=True);(base/'.jitx').mkdir()
            (base/'.jitx/runtime.json').write_text('{"websocket_uri":"ws://localhost/test"}')
            with patch.object(native,'BASE',base),patch.object(native,'Runtime',Runtime):
                with self.assertRaises(TimeoutError):asyncio.run(native.execute([{'type':'reposition','body':{}}],base/'attempt'))
                self.assertTrue((base/'.bridge-uncertain.json').exists())
                with self.assertRaisesRegex(RuntimeError,'completion unknown'):asyncio.run(native.execute([],base/'next'))
                self.assertFalse((base/'next').exists())

if __name__=='__main__':unittest.main()
