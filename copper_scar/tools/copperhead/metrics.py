"""Versioned feasibility diagnostics, never an official PCB score."""
import math
import re

VERSION = 'native-defects-v1'

def item_key(v):
    return (v['type'], tuple(sorted(i.get('uuid','') for i in v.get('items',[]))))

def measure(report):
    unique={item_key(v):v for v in report['violations']+report['schematic_parity']+report['unconnected_items']}
    shorts=0;physical=0;clearances=0;deficits=[];missing=[];errors=0;warnings=0
    for v in unique.values():
        kind=v['type']
        if kind=='unconnected_items':
            points=[i.get('pos') for i in v.get('items',[])]
            distance=None
            if len(points)==2 and all(q and 'x' in q and 'y' in q for q in points):
                distance=math.hypot(points[1]['x']-points[0]['x'],points[1]['y']-points[0]['y'])
            missing.append(distance)
            continue
        errors+=v['severity']=='error';warnings+=v['severity']=='warning'
        if kind=='shorting_items':shorts+=1
        elif kind in ['clearance','hole_clearance','edge_clearance','courtyards_overlap','solder_mask_bridge']:
            clearances+=1
            m=re.search(r'(?:clearance|minimum|min)\s+([0-9.]+) mm; actual\s+([0-9.]+) mm',v['description'])
            if m:deficits.append(max(0,float(m[1])-float(m[2])))
        elif v['severity']=='error':physical+=1
    return dict(version=VERSION,short_item_pairs=shorts,other_error_findings=physical,clearance_findings=clearances,
                maximum_measured_clearance_shortfall_mm=max(deficits,default=0),total_measured_clearance_shortfall_mm=sum(deficits),
                clearance_severity_coverage=dict(measured=len(deficits),findings=clearances),missing_endpoint_pairs=len(missing),
                total_missing_endpoint_distance_mm=sum(v for v in missing if v is not None),missing_distance_coverage=dict(measured=sum(v is not None for v in missing),findings=len(missing)),
                raw_unconnected_report_count=len(report['unconnected_items']),errors=errors,warnings=warnings,
                note='Endpoint-pair distance is an airwire proxy, not minimum route length, unique electrical islands or official score.')

def ordering(metrics, invariants_ok):
    return (int(not invariants_ok),metrics['short_item_pairs'],metrics['other_error_findings'],metrics['clearance_findings'],
            round(metrics['maximum_measured_clearance_shortfall_mm'],6),metrics['missing_endpoint_pairs'],
            round(metrics['total_missing_endpoint_distance_mm'],3),metrics['warnings'])
