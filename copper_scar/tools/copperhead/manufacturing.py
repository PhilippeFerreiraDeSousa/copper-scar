"""Manufacturing rule findings remain blockers even at warning severity."""
RULE_TYPES=frozenset({
    'shorting_items','clearance','copper_edge_clearance','edge_clearance',
    'hole_clearance','hole_to_hole','holes_co_located','track_width',
    'annular_width','via_diameter','drill_out_of_range','solder_mask_bridge',
    'starved_thermal',
})


def findings(report):
    return [item for item in report['violations'] if item['type'] in RULE_TYPES]
