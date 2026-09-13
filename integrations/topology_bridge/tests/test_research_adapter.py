import hashlib
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research_adapter import moves_from_research

def test_stale_pose_and_hash_rejected(tmp_path):
    board=tmp_path/'parent';board.write_bytes(b'parent')
    p={'kind':'group_pose','parent_board_sha256':hashlib.sha256(b'parent').hexdigest(),'refs':['TP4'],'from_poses':{'TP4':{'x_mm':148,'y_mm':102,'angle_deg':0}},'translation_mm':[-2,2]}
    assert moves_from_research(p,board,{'TP4':{'xy':[8,6]}},{'TP4':[148,102,0]})=={'TP4':[6,4]}
    with pytest.raises(ValueError,match='pose'):moves_from_research(p,board,{'TP4':{'xy':[8,6]}},{'TP4':[149,102,0]})
    board.write_bytes(b'changed')
    with pytest.raises(ValueError,match='Stale'):moves_from_research(p,board,{}, {})
