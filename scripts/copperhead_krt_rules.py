"""Compare producer project settings without accepting them as source rules."""
import hashlib
import json


def setting_changes(before, after, path=''):
    if isinstance(before, dict) and isinstance(after, dict):
        changes=[]
        for key in sorted(before.keys() | after.keys()):
            location=path+'.'+key if path else key
            if key not in before or key not in after:
                changes.append(dict(path=location,before=before.get(key),after=after.get(key)))
            else:
                changes.extend(setting_changes(before[key],after[key],location))
        return changes
    return [] if before==after else [dict(path=path,before=before,after=after)]


def project_audit(original, producer):
    changes=setting_changes(json.loads(original),json.loads(producer))
    return dict(original_sha256=hashlib.sha256(original).hexdigest(),
                producer_sha256=hashlib.sha256(producer).hexdigest(),
                semantic_changes=changes,producer_rule_preservation='violated' if changes else 'verified',
                authoritative_rules='original project bytes only; producer settings are not adopted')
