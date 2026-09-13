"""Persistent via eligibility and evidence-derived realization context keys."""
import hashlib
import json
from pathlib import Path
import re

ORIGINAL='Via[0-5]_600:300_um'
SMALL='Via[0-5]_450:200_um'


def context(names,scope,contacts=None):
    normalized=dict(schema_version='effective-via-rules-v1',constraint_scope=scope,allowed_via_options=sorted(set(names)))
    if contacts:
        assert contacts['version']=='split-existing-junctions-v1' and contacts['nets']
        normalized.update(schema_version='effective-routing-recipe-v2',dsn_contact_normalization=dict(version=contacts['version'],nets=sorted(set(contacts['nets']))))
    return {**normalized,'digest':hashlib.sha256(json.dumps(normalized,sort_keys=True,separators=(',',':')).encode()).hexdigest()}


def dsn_context(text,scope):
    declarations=re.findall(r'\(use_via\s+([^)]*)\)',text)
    if len(declarations)!=1:raise ValueError('Only the verified single-class DSN context is supported')
    names=re.findall(r'"([^"\n]+)"',declarations[0])
    if not names:raise ValueError('No explicit loaded via options in DSN')
    return context(names,scope)


def candidate_options(candidate,local,scope):
    paths=[Path(candidate)/'routing-options.json',Path(local)/'loop/routing-options.json']
    path=next((p for p in paths if p.exists()),None)
    options=json.loads(path.read_text()) if path else dict(schema_version=1,constraint_scope=scope,allowed_via_options=[ORIGINAL],qualification='Original export defaults only')
    assert options['constraint_scope']==scope,'Routing options belong to another original-rule scope'
    assert set(options['allowed_via_options']) in ({ORIGINAL},{ORIGINAL,SMALL}),'Unqualified via options'
    return options,context(options['allowed_via_options'],scope,options.get('dsn_contact_normalization'))


def record_context(record):
    """Infer historical context only from the DSN bytes hashed during routing."""
    if record.get('realization_context_verified'):
        return {**record['realization_context'],'provenance':'recorded_and_engine_verified'}
    path=Path(record.get('candidate',''))/'pcbgolf.dsn'
    expected=record.get('routing_scope',{}).get('execution',{}).get('coverage',{}).get('dsn_sha256')
    if not expected or not path.is_file():return dict(digest=None,provenance='unknown_legacy_context')
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:return dict(digest=None,provenance='legacy_dsn_hash_mismatch',dsn_sha256=actual)
    try:value=dsn_context(path.read_text(),record['constraint_scope'])
    except (ValueError,KeyError):return dict(digest=None,provenance='unsupported_legacy_dsn_context')
    return {**value,'provenance':'inferred_from_frozen_hashed_dsn','dsn':str(path),'dsn_sha256':actual}


def feedback_in_context(feedback,runs,digest):
    kept=[];excluded=[]
    for fact in feedback:
        path=Path(runs)/fact['attempt']/'attempt.json'
        ctx=record_context(json.loads(path.read_text())) if path.exists() else dict(digest=None,provenance='missing_attempt')
        if ctx.get('digest')==digest:kept.append({**fact,'realization_context':ctx})
        else:excluded.append(dict(attempt=fact['attempt'],realization_context=ctx,reason='Different or unknown realization context; not a failed pose in the current recipe'))
    return kept,excluded


def verify_after_exports(commands,python,script,candidate):
    result=[]
    for entry in commands:
        result.append(entry)
        if entry[0]=='export' or entry[0].endswith('_export'):
            result.append((entry[0]+'_effective_options',[str(python),str(script),str(candidate),'--phase',entry[0]],90))
    return result
