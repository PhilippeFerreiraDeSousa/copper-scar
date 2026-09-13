import json
from copper_scar.tools.copperhead.records import load_record


def test_correction_changes_effective_retention_without_rewriting_attempt(tmp_path):
    path=tmp_path/'attempt.json'
    raw=json.dumps({'attempt':'a','became_incumbent':True,'incumbent_after':{'candidate':'new'}})
    path.write_text(raw)
    (tmp_path/'retention-correction.json').write_text(json.dumps({'attempt':'a','restored':{'candidate':'old'}}))
    record=load_record(path)
    assert record['historical_became_incumbent'] is True
    assert record['became_incumbent'] is False
    assert record['incumbent_after']=={'candidate':'old'}
    assert path.read_text()==raw
