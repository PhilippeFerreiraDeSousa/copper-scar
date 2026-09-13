"""Read immutable attempts with explicit, separately preserved corrections."""
import json


def load_record(path):
    record=json.loads(path.read_text())
    correction=path.parent/'retention-correction.json'
    if correction.exists():
        audit=json.loads(correction.read_text())
        assert audit['attempt']==record['attempt']
        record['historical_became_incumbent']=record.get('became_incumbent')
        record['became_incumbent']=False
        record['incumbent_after']=audit['restored']
        record['retention_correction']=audit
    return record
