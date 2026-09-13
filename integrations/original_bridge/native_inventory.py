"""Read-only native KiCad geometry inventory; mutations remain in unsaved memory."""
import argparse
import hashlib
import json
from pathlib import Path
import pcbnew as k

INTERFACE={'R37','R42','J2','U3'}
DETAIL=INTERFACE|{'J1','J3','J5','J6','J7','J8','U4'}

def polygon(item,layer,clearance=0):
    result=k.SHAPE_POLY_SET()
    item.TransformShapeToPolygon(result,layer,clearance,1,k.ERROR_INSIDE)
    return [[[result.COutline(j).CPoint(i).x/1e6,result.COutline(j).CPoint(i).y/1e6]
             for i in range(result.COutline(j).PointCount())] for j in range(result.OutlineCount())]

def inventory(path):
    board=k.LoadBoard(str(path.resolve()))
    if board is None:raise ValueError('KiCad did not load this board; inspect raw export syntax')
    fps={};members={}
    for f in board.GetFootprints():
        ref=f.GetReference();pose=[f.GetPosition().x/1e6,f.GetPosition().y/1e6,f.GetOrientationDegrees()]
        # Localize one footprint in this private in-memory board, never SaveBoard.
        f.SetPosition(k.VECTOR2I(0,0));f.SetOrientationDegrees(0)
        pads=[]
        for p in f.Pads():
            net=p.GetNetname();key=ref+'.'+p.GetNumber()
            if net:members.setdefault(net,[]).append(key)
            d={'name':p.GetNumber(),'net':net,'uuid':p.m_Uuid.AsString(),
               'at':[p.GetPosition().x/1e6,p.GetPosition().y/1e6,p.GetOrientationDegrees()],
               'size':[p.GetSize().x/1e6,p.GetSize().y/1e6],'shape':p.GetShape(),'roundrect_ratio':p.GetRoundRectRadiusRatio(),
               'attribute':p.GetAttribute(),'drill':[p.GetDrillSize().x/1e6,p.GetDrillSize().y/1e6],
               'layers':[board.GetLayerName(l) for l in p.GetLayerSet().Seq()],
               'mask_expansion':p.GetSolderMaskExpansion(k.F_Mask)/1e6}
            if ref in DETAIL:
                d['polygons']={}
                for label,layer in [('F.Cu',k.F_Cu),('F.Mask',k.F_Mask),('B.Mask',k.B_Mask),('F.Paste',k.F_Paste)]:
                    if p.IsOnLayer(layer):
                        clearance=p.GetSolderMaskExpansion(layer) if label.endswith('Mask') else 0
                        d['polygons'][label]=polygon(p,layer,clearance)
            pads.append(d)
        graphics={}
        if ref in DETAIL:
            for item in f.GraphicalItems():
                if item.GetClass()=='PCB_TEXT':
                    continue  # Annotation glyphs are not component body/obstacle geometry.
                layer=item.GetLayer();label=board.GetLayerName(layer)
                if label in ('F.Cu','F.Mask','B.Mask','F.Paste','F.CrtYd','F.Fab','F.SilkS'):
                    try:graphics.setdefault(label,[]).extend(polygon(item,layer))
                    except (TypeError,AttributeError):pass
        fps[ref]={'pose':pose,'uuid':f.m_Uuid.AsString(),'pads':pads,'graphics':graphics}
    return {'board_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kicad_version':k.GetBuildVersion(),
            'text_annotations_excluded_from_obstacle_union':True,'polygon_max_error_mm':.000001,'footprints':fps,'net_memberships':{n:sorted(v) for n,v in members.items()},
            'copper_layers':[board.GetLayerName(l) for l in board.GetEnabledLayers().CuStack()],
            'source_path':str(path),'saved_board':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('board',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    data=inventory(a.board)
    with a.output.open('x') as f:json.dump(data,f)
