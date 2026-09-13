"""Negative acceptance checks against a saved, independently checked fixture."""
from pathlib import Path
import json,os,shutil,sys
import pytest
sys.path.insert(0,str(Path(__file__).parent));sys.path.insert(0,str(Path(__file__).parents[2]))
from audit import audit
from stage2 import score
ROOT=Path(__file__).parents[2]
BASE=ROOT/'.local/small-loop'
REF=Path('/Users/philippe/dev/copper-scar-demo/.local/pcbgolf-source')
@pytest.fixture
def board(tmp_path):
 src=BASE/'stage2/final-accepted'
 if not src.exists():pytest.skip('Requires explicit saved native acceptance fixture')
 dst=tmp_path/'board';shutil.copytree(src,dst);return dst

def check(folder):return audit(folder,BASE/'input/circuit.json',REF)
def test_rule_relaxation_cannot_pass(board):
 p=board/'pcbgolf.kicad_pro';j=json.loads(p.read_text());j['board']['design_settings']['rules']['min_clearance']=0;p.write_text(json.dumps(j))
 r=check(board);assert not r['accepted'] and not r['rules_preserved']['drc']
def test_parity_failure_cannot_receive_score(board):
 p=board/'drc.json';j=json.loads(p.read_text());j['schematic_parity']=[{'type':'net_conflict','severity':'warning','description':'negative test'}];p.write_text(json.dumps(j))
 assert not check(board)['accepted'];r=score(board);assert not r['valid'] and r['official_formula_score'] is None
def test_missing_populated_model_cannot_receive_score(board):
 (board/'models/M20-9980446-nominal.step').unlink()
 with pytest.raises(AssertionError):score(board)
def test_saved_board_drift_invalidates_native_receipt(board):
 p=board/'pcbgolf.kicad_pcb';p.write_text(p.read_text()+'\n')
 assert not check(board)['accepted']
