"""Explicit4layer stackup proposal, preserving1.6mm nominal board thickness and BOM."""
from pathlib import Path
import argparse,json,shutil,subprocess
import sexpdata as sx
from campaign import KIPY,ROOT,write,sha
from audit import nodes,first
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);a=ap.parse_args();base=a.base.resolve();parent=base/'stage2/primitive-uniform-01/candidate-02';out=base/'stage2/four-layer-input';out.mkdir();d=sx.loads((parent/'pcbgolf.kicad_pcb').read_text());d[:]=[v for v in d if not(isinstance(v,list) and v and str(v[0]) in ['segment','via','arc','zone'])];layers=first(d,'layers');copper=[sx.loads('(0 "F.Cu" signal)'),sx.loads('(4 "In1.Cu" signal)'),sx.loads('(6 "In2.Cu" signal)'),sx.loads('(2 "B.Cu" signal)')];layers[1:]=copper+[v for v in layers[1:] if not str(v[1]).endswith('.Cu')];setup=first(d,'setup');setup[:]=[v for v in setup if not(isinstance(v,list) and v and str(v[0])=='stackup')]
setup.append(sx.loads('''(stackup
(layer "F.SilkS" (type "Top Silk Screen"))
(layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))
(layer "F.Cu" (type "copper") (thickness 0.035))
(layer "dielectric 1" (type "prepreg") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
(layer "In1.Cu" (type "copper") (thickness 0.035))
(layer "dielectric 2" (type "core") (thickness 1.04) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
(layer "In2.Cu" (type "copper") (thickness 0.035))
(layer "dielectric 3" (type "prepreg") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
(layer "B.Cu" (type "copper") (thickness 0.035))
(layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))
(layer "B.SilkS" (type "Bottom Silk Screen"))
(copper_finish "None") (dielectric_constraints no))'''))
(out/'pcbgolf.kicad_pcb').write_text(sx.dumps(d));m=json.loads((base/'input/circuit.json').read_text());m['expected_copper_layers']=4;write(out/'circuit.json',m);inc=json.loads((parent/'score.json').read_text());write(out/'proposal.json',{'kind':'qualified_layer_count_trial','source_board_sha256':sha(parent/'pcbgolf.kicad_pcb'),'eligible_layers':['F.Cu','In1.Cu','In2.Cu','B.Cu'],'explicit_stackup_mm':{'copper_each':.035,'dielectric':[.2,1.04,.2],'mask_each':.01,'total':1.6},'BOM_unchanged':True,'rule_values_unchanged':True,'expected_score_terms':{'assembly_volume_assumption':inc['terms']['pcba_bbox_volume_mm3'],'via_count_target':'unknown;morelayersmayreducecongestionbutmustbemeasured','layer_penalty':20000,'score_lower_bound_zero_vias':inc['terms']['pcba_bbox_volume_mm3']+20000},'rationale':'Qualify actual4layer nativepipeline and scorecost. Onthisfixedgeometry evenzero vias cannotbeat2layerincumbent; runasexplicitcapability/penaltycontrol, neverclaimoptimizationwin.'});print(out)
