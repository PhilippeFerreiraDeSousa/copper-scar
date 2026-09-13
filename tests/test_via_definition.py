import importlib.util
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location('via_definition',Path(__file__).parents[1]/'scripts/copperhead_via_definition.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def source():
    old='Via[0-5]_600:300_um'
    pad='(padstack "'+old+'" '+''.join('(shape (circle '+layer+' 600)) ' for layer in module.LAYERS)+'(attach off))'
    return '(pcb test (structure (via "'+old+'")) (library '+pad+') (network (class default GND (circuit (use_via "'+old+'")))) (wiring (via "'+old+'" 123 456 (net GND)(type route))))'


RULES=dict(min_via_diameter=.3524,min_through_hole_diameter=.2,min_via_annular_width=.0762)


def test_addition_preserves_every_existing_dsn_expression():
    import sexpdata
    original=source();result,report=module.add_definition(original,RULES)
    before=sexpdata.loads(original);after=sexpdata.loads(result)
    after[2][1].remove(module.NAME)
    after[3]=[x for x in after[3] if not isinstance(x,list) or x[1]!=module.NAME]
    after[4][1][3][1].remove(module.NAME)
    assert after==before
    assert report['eligibility_declarations_changed']==2
    assert module.add_definition(result,RULES)[0]==result


@pytest.mark.parametrize('key,value',[('min_via_diameter',.46),('min_through_hole_diameter',.21),('min_via_annular_width',.126)])
def test_original_dimensional_rules_reject_ineligible_definition(key,value):
    with pytest.raises(AssertionError):module.add_definition(source(),{**RULES,key:value})
