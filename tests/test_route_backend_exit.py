import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace
import pytest


@pytest.mark.parametrize('backend', ['nonzero','external_timeout'])
def test_partial_session_cannot_hide_backend_failure(tmp_path,monkeypatch,backend):
    (tmp_path/'pcbgolf.dsn').write_text('(pcb test (structure (layer F.Cu)) (network) (placement))')
    (tmp_path/'pcbgolf.ses').write_text('partial session evidence')
    def failed_run(*args,**kwargs):
        if backend=='external_timeout':raise subprocess.TimeoutExpired(['backend'],1)
        return SimpleNamespace(returncode=23)
    monkeypatch.setattr(subprocess,'run',failed_run)
    scripts=Path(__file__).resolve().parents[1]/'scripts'
    monkeypatch.syspath_prepend(str(scripts))
    monkeypatch.setattr(sys,'argv',['copperhead_route.py',str(tmp_path),'--seconds','10'])
    with pytest.raises(SystemExit) as error:
        runpy.run_path(str(scripts/'copperhead_route.py'),run_name='__main__')
    assert error.value.code==(124 if backend=='external_timeout' else 23)
    evidence=json.loads((tmp_path/'execution.json').read_text())
    assert evidence['session_exists'] is True
    assert evidence['timeout']==(backend=='external_timeout')
    assert (tmp_path/'pcbgolf.ses').read_text()=='partial session evidence'
