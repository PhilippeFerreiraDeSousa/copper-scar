"""Make an isolated artwork-only qualification candidate from a native report.

Move only the source body-outline graphics proven to intersect solder-mask
openings to F.Fab. Electrical/mechanical pad geometry and rule bytes stay fixed.
"""
from pathlib import Path
import argparse,collections,hashlib,json,re,shutil
import pcbnew as p

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('parent',type=Path);a.add_argument('original_drc',type=Path);a.add_argument('output',type=Path);x=a.parse_args()
 assert not x.output.exists();shutil.copytree(x.parent,x.output)
 boardpath=x.output/'pcbgolf.kicad_pcb';project=x.output/'pcbgolf.kicad_pro';project_bytes=project.read_bytes()
 original=json.loads(x.original_drc.read_text())['violations'];orig={tuple(sorted(i['uuid'] for i in v['items'])) for v in original}
 report=json.loads((x.parent/'evaluation.json').read_text());groups=collections.Counter();ids=set();evidence=[]
 for v in report['required_violations']:
  sig=tuple(sorted(i['uuid'] for i in v['items']));assert sig in orig
  owner=re.search(r' of (\w+) on ',v['items'][0]['description']).group(1)
  groups[(owner,v['type'])]+=1;evidence.append(v)
  if v['type']=='silk_over_copper':ids.add(v['items'][0]['uuid'])
 b=p.LoadBoard(str(boardpath));changes=[]
 for fp in b.GetFootprints():
  for g in fp.GraphicalItems():
   if g.m_Uuid.AsString() in ids:
    assert g.GetLayer()==p.F_SilkS
    changes.append({'reference':fp.GetReference(),'footprint':str(fp.GetFPID().GetLibItemName()),'uuid':g.m_Uuid.AsString(),'before_layer':'F.SilkS','after_layer':'F.Fab','shape':str(g.GetShape()),'start_mm':[p.ToMM(g.GetStart().x),p.ToMM(g.GetStart().y)],'end_mm':[p.ToMM(g.GetEnd().x),p.ToMM(g.GetEnd().y)],'width_mm':p.ToMM(g.GetWidth())})
    g.SetLayer(p.F_Fab)
 assert len(changes)==len(ids)
 p.SaveBoard(str(boardpath),b);project.write_bytes(project_bytes)
 # Parent completion/audit files describe the frozen parent, never this candidate.
 for f in x.output.glob('*.json'):f.unlink()
 manifest={'parent':str(x.parent.resolve()),'parent_board_sha256':digest(x.parent/'pcbgolf.kicad_pcb'),'candidate_board_sha256':digest(boardpath),'rule_project_bytes_unchanged':digest(project)==digest(x.parent/'pcbgolf.kicad_pro'),'all84_same_original_uuid_pairs':True,'groups':[{'reference':ref,'rule':rule,'count':count} for (ref,rule),count in sorted(groups.items())],'artwork_changes':changes,'original_findings':evidence,'scope':'Declared artwork-only candidate; offending body outlines transferred to assembly layer, not waived. All electrical and mechanical geometry fixed. No manufacturing-valid claim.'}
 (x.output/'repair-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'groups':manifest['groups'],'graphics_changed':len(changes),'rules_unchanged':manifest['rule_project_bytes_unchanged']}))
if __name__=='__main__':main()
