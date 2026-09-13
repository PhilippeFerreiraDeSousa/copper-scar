"""Read immutable attempts with explicit, separately preserved corrections."""
import json


def load_record(path):
    record=json.loads(path.read_text())
    correction=path.parent/'retention-correction.json'
    if correction.exists():
        audit=json.loads(correction.read_text())
        assert audit['attempt']==record['attempt']
        record['historical_became_incumbent']=record.get('became_incumbent')
        record['became_incumbent']=audit.get('effective_retained',False)
        record['incumbent_after']=audit.get('selected',audit.get('restored'))
        assert record['incumbent_after'] is not None
        if audit.get('selection_decision'):record['selection_decision']=audit['selection_decision']
        record['retention_correction']=audit
    return record
