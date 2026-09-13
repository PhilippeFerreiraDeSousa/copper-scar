from copy import deepcopy
import pytest
from copper_scar.tools.copperhead.selection import manufacturing_repair_decision


def fixture():
    before=dict(constraint_scope='original',design_sha256='parent',invariants_ok=True,counts={},errors=0,unconnected=53,violations=[{'type':'hole_to_hole','severity':'warning'}],airwire=1000)
    after={**before,'design_sha256':'repaired','violations':[],'airwire':2000}
    return before,after,dict(scope='original',design_sha256='parent')


def test_manufacturing_repair_is_not_vetoed_by_noisy_airwire_proxy():
    before,after,incumbent=fixture()
    assert manufacturing_repair_decision(before,after,incumbent,backend_ok=True,pad_partitions_preserved=True)['eligible']


@pytest.mark.parametrize('change',[{'unconnected':54},{'errors':1},{'invariants_ok':False},{'constraint_scope':'changed'}])
def test_substantive_regression_blocks_manufacturing_repair(change):
    before,after,incumbent=fixture();after.update(change)
    assert not manufacturing_repair_decision(before,after,incumbent,backend_ok=True,pad_partitions_preserved=True)['eligible']


def test_failed_backend_or_split_connectivity_cannot_promote_repair():
    before,after,incumbent=fixture()
    assert not manufacturing_repair_decision(before,after,incumbent,backend_ok=False,pad_partitions_preserved=True)['eligible']
    assert not manufacturing_repair_decision(before,after,incumbent,backend_ok=True,pad_partitions_preserved=False)['eligible']
