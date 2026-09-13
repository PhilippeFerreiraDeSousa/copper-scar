"""Build a preserved five-sheet hierarchy in a fresh, track-local candidate."""
from pathlib import Path
import argparse, json, shutil, uuid
import sexpdata as sx

def nodes(n,k): return [v for v in n if isinstance(v,list) and v and str(v[0])==k]
def walk(n):
    if isinstance(n,list):
        yield n
        for v in n: yield from walk(v)
def S(v):return sx.Symbol(v)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('candidate',type=Path);args=ap.parse_args()
    if args.candidate.exists():raise SystemExit('Refusing existing candidate')
    shutil.copytree(args.source,args.candidate,ignore=shutil.ignore_patterns('.git','.copperhead'))
    project=json.loads((args.source/'pcbgolf.kicad_pro').read_text())
    root=str(uuid.uuid5(uuid.NAMESPACE_URL,'copper-scar/native/full-reference-v1'))
    wrapper=[S('kicad_sch'),[S('version'),20260306],[S('generator'),'eeschema'],[S('generator_version'),'10.0'],[S('uuid'),root],[S('paper'),'A4'],[S('lib_symbols')]]
    mapping=[]
    for i,item in enumerate(project['schematic']['top_level_sheets']):
        filename=item['filename']; d=sx.loads((args.source/filename).read_text())
        instance=nodes(nodes(nodes(nodes(d,'symbol')[0],'instances')[0],'project')[0],'path')[0][1]
        old=instance.strip('/'); newpath=f'/{root}/{old}'
        newfile='pcbgolf_power.kicad_sch' if filename=='pcbgolf.kicad_sch' else filename
        changes=0
        for n in walk(d):
            if len(n)>1 and str(n[0])=='path' and isinstance(n[1],str) and n[1]==instance:
                n[1]=newpath;changes+=1
        (args.candidate/newfile).write_text(sx.dumps(d))
        sheet=sx.loads(f'''(sheet (at {20+i*35} 30) (size 30 20) (stroke (width 0) (type default)) (fill (color 0 0 0 0)) (uuid "{old}") (property "Sheetname" "Sheet{i+1}" (at {20+i*35} 29 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" "{newfile}" (at {20+i*35} 51 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "pcbgolf" (path "/{root}" (page "{i+2}")))))''')
        wrapper.append(sheet)
        mapping.append(dict(source=filename,child=newfile,old_instance_root=old,actual_root=nodes(d,'uuid')[0][1],new_instance_path=newpath,instance_paths_updated=changes))
    wrapper.append(sx.loads('(sheet_instances (path "/" (page "1")))'))
    (args.candidate/'pcbgolf.kicad_sch').write_text(sx.dumps(wrapper))
    # Only instance addressing changes; preserve circuit objects and drawing geometry.
    board=sx.loads((args.candidate/'pcbgolf.kicad_pcb').read_text())
    for fp in nodes(board,'footprint'):
        for path in nodes(fp,'path'):
            path[1]='/'+root+path[1]
    (args.candidate/'pcbgolf.kicad_pcb').write_text(sx.dumps(board))
    project['schematic']['top_level_sheets']=[dict(filename='pcbgolf.kicad_sch',uuid=root)]
    (args.candidate/'pcbgolf.kicad_pro').write_text(json.dumps(project,indent=2)+'\n')
    (args.candidate/'hierarchy-conversion.json').write_text(json.dumps(dict(root=root,sheets=mapping,policy='Only instance paths and wrapper changed; native electrical partition comparison required.'),indent=2))
    print(args.candidate)
if __name__=='__main__':main()
