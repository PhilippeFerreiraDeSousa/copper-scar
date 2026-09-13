from copper_scar.tools.copperhead.manufacturing import findings


def test_warning_severity_does_not_waive_overlapping_drill_holes():
    physical={'type':'hole_to_hole','severity':'warning','description':'minimum0.2500mm; actual0.0000mm'}
    library={'type':'lib_footprint_issues','severity':'warning'}
    assert findings({'violations':[physical,library]})==[physical]
