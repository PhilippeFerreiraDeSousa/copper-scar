"""Add one through-via option without rewriting existing DSN geometry or rules."""
import argparse
import hashlib
import json
import re
from pathlib import Path

NAME = 'Via[0-5]_450:200_um'
LAYERS = ('F.Cu', 'In1.Cu', 'In2.Cu', 'In3.Cu', 'In4.Cu', 'B.Cu')


def add_definition(source, rules):
    assert rules['min_via_diameter'] <= .45
    assert rules['min_through_hole_diameter'] <= .2
    assert rules['min_via_annular_width'] <= (.45-.2)/2
    definition = '(padstack "'+NAME+'"\n'+''.join('      (shape (circle '+layer+' 450))\n' for layer in LAYERS)+'      (attach off)\n    )'
    # Exported KiCad through-via definitions contain exactly six circles and attach.
    pattern = r'\(padstack "'+re.escape(NAME)+r'"\s*(?:\(shape \(circle [^)]+\)\)\s*){6}\(attach off\)\s*\)'
    found = list(re.finditer(pattern, source))
    if '"'+NAME+'"' in source:
        assert len(found) == 1, 'Unexpected existing new padstack definition'
        assert re.sub(r'\s+', ' ', found[0][0]) == re.sub(r'\s+', ' ', definition)
    else:
        old = re.search(r'\(padstack "Via\[0-5\]_600:300_um"\s*(?:\(shape \(circle [^)]+\)\)\s*){6}\(attach off\)\s*\)', source)
        assert old, 'Expected original six-layer through-via definition'
        source = source[:old.end()]+'\n    '+definition+source[old.end():]
    # Only declarations match: wiring via instances have coordinates, not just names.
    changes = []
    def eligible(match):
        text = match[0]
        if '"'+NAME+'"' in text:
            return text
        changes.append(text)
        return text[:-1]+' "'+NAME+'")'
    result = re.sub(r'\((?:via|use_via)\s+(?:"[^"\n]+"\s*)+\)', eligible, source)
    assert re.search(r'\(via\s+(?:"[^"\n]+"\s*)*"'+re.escape(NAME)+r'"', result)
    assert re.search(r'\(use_via\s+(?:"[^"\n]+"\s*)*"'+re.escape(NAME)+r'"', result)
    return result, dict(name=NAME, diameter_mm=.45, drill_mm=.2, layers=list(LAYERS), eligibility_declarations_changed=len(changes), existing_geometry_rewritten=False)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--phase',required=True);a=ap.parse_args()
    path=a.folder/'pcbgolf.dsn';original=path.read_text()
    rules=json.loads((a.folder/'pcbgolf.kicad_pro').read_text())['board']['design_settings']['rules']
    result,report=add_definition(original,rules)
    evidence=a.folder/'via-definition';evidence.mkdir(exist_ok=True)
    (evidence/(a.phase+'-before.dsn')).write_text(original)
    (evidence/(a.phase+'-after.dsn')).write_text(result)
    report.update(input_sha256=hashlib.sha256(original.encode()).hexdigest(),output_sha256=hashlib.sha256(result.encode()).hexdigest(),original_rules=rules)
    (evidence/(a.phase+'.json')).write_text(json.dumps(report,indent=2));path.write_text(result)
    print(json.dumps(report))


if __name__=='__main__':main()
