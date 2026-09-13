#!/usr/bin/env python3
"""Independently read STEP geometry and compare named population with native inventory."""
import argparse,hashlib,json,re,importlib.metadata
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
p=argparse.ArgumentParser();p.add_argument('step',type=Path);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
text=a.step.read_text();inventory=json.loads(a.inventory.read_text());expected={f['ref'] for f in inventory['footprints'] if not f['dnp']}
matches=re.findall(r"NEXT_ASSEMBLY_USAGE_OCCURRENCE\('[^']*','([^']*)','[^']*',\s*(#\d+),\s*(#\d+)",text,re.S)
parents={parent for name,parent,child in matches if name in expected};assert len(parents)==1
assembly_parent=next(iter(parents));component_names=[name for name,parent,child in matches if parent==assembly_parent and re.fullmatch(r'[A-Z]+\d+',name)]
assert set(component_names)==expected and len(component_names)==len(expected)
r=STEPControl_Reader();assert r.ReadFile(str(a.step))==IFSelect_RetDone
roots=r.TransferRoots();shape=r.OneShape();assert roots>0 and not shape.IsNull()
bbox=Bnd_Box();BRepBndLib.AddOptimal_s(shape,bbox,False,False);lo=bbox.CornerMin();hi=bbox.CornerMax();bounds=[lo.X(),lo.Y(),lo.Z(),hi.X(),hi.Y(),hi.Z()];size=[bounds[i+3]-bounds[i] for i in range(3)]
solids=TopExp_Explorer(shape,TopAbs_SOLID);count=0;invalid=0
while solids.More():
 count+=1
 if not BRepCheck_Analyzer(solids.Current()).IsValid():invalid+=1
 solids.Next()
result=dict(step_sha256=hashlib.sha256(a.step.read_bytes()).hexdigest(),bytes=a.step.stat().st_size,reader='cadquery-ocp '+importlib.metadata.version('cadquery-ocp'),transferred_roots=roots,expected_populated_components=len(expected),named_component_instances=len(component_names),component_names_exact_match=True,excluded_DNP=inventory['summary']['dnp_refs'],solid_count=count,invalid_solids=invalid,whole_shape_valid=BRepCheck_Analyzer(shape).IsValid(),bbox_mm=dict(min=bounds[:3],max=bounds[3:],size=size),bbox_volume_mm3=size[0]*size[1]*size[2],qualification='Geometric bounds of this exported recorded-population assembly only. Not an official score, mechanical-fit check, functional proof, or manufacturing qualification. DNP header/hardware bodies and external mating parts are absent by recorded population.')
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
