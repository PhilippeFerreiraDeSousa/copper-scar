# Original-rule coverage inventory

> Current status: policy-v3 incumbent009 has310 opens,44 errors,237 warnings; no valid board. Native routing stopped. The surviving002 lacks via definitions; source reload is unqualified after007 crash. See [current via and warning review](jitx-via-workflow-and-warning-review.md). Earlier numeric status below describes its recorded experiment.

All faithful-native claims remain unproven. KiCad is authoritative for supported original DRC/ERC checks; independent engineering gates remain required.

| Category | Rule | Source | Native status |
|---|---|---|---|
| physical_minimum | max_error | 0.005 | external-only-unproven |
| physical_minimum | min_clearance | 0.0762 | translatable-not-equivalence-tested |
| physical_minimum | min_connection | 0.0 | external-only-unproven |
| physical_minimum | min_copper_edge_clearance | 0.025 | translatable-not-equivalence-tested |
| physical_minimum | min_groove_width | 0.0 | external-only-unproven |
| physical_minimum | min_hole_clearance | 0.25 | translatable-not-equivalence-tested |
| physical_minimum | min_hole_to_hole | 0.25 | translatable-not-equivalence-tested |
| physical_minimum | min_microvia_diameter | 0.2 | external-only-unproven |
| physical_minimum | min_microvia_drill | 0.1 | external-only-unproven |
| physical_minimum | min_resolved_spokes | 2 | external-only-unproven |
| physical_minimum | min_silk_clearance | 0.0 | external-only-unproven |
| physical_minimum | min_text_height | 0.8 | translatable-not-equivalence-tested |
| physical_minimum | min_text_thickness | 0.08 | external-only-unproven |
| physical_minimum | min_through_hole_diameter | 0.2 | translatable-not-equivalence-tested |
| physical_minimum | min_track_width | 0.1016 | translatable-not-equivalence-tested |
| physical_minimum | min_via_annular_width | 0.0762 | translatable-not-equivalence-tested |
| physical_minimum | min_via_diameter | 0.3524 | external-only-unproven |
| physical_minimum | solder_mask_to_copper_clearance | 0.0 | external-only-unproven |
| physical_minimum | use_height_for_length_calcs | True | external-only-unproven |
| drc_severity | annular_width | error | external-only |
| drc_severity | clearance | error | external-only |
| drc_severity | connection_width | warning | external-only |
| drc_severity | copper_edge_clearance | error | external-only |
| drc_severity | copper_sliver | warning | external-only |
| drc_severity | courtyards_overlap | error | external-only |
| drc_severity | creepage | error | external-only |
| drc_severity | diff_pair_gap_out_of_range | error | external-only |
| drc_severity | diff_pair_uncoupled_length_too_long | error | external-only |
| drc_severity | drill_out_of_range | error | external-only |
| drc_severity | duplicate_footprints | warning | external-only |
| drc_severity | extra_footprint | warning | external-only |
| drc_severity | footprint | error | external-only |
| drc_severity | footprint_filters_mismatch | ignore | external-only |
| drc_severity | footprint_symbol_field_mismatch | warning | external-only |
| drc_severity | footprint_symbol_mismatch | warning | external-only |
| drc_severity | footprint_type_mismatch | ignore | external-only |
| drc_severity | hole_clearance | error | external-only |
| drc_severity | hole_to_hole | warning | external-only |
| drc_severity | holes_co_located | warning | external-only |
| drc_severity | invalid_outline | error | external-only |
| drc_severity | isolated_copper | warning | external-only |
| drc_severity | item_on_disabled_layer | error | external-only |
| drc_severity | items_not_allowed | error | external-only |
| drc_severity | length_out_of_range | error | external-only |
| drc_severity | lib_footprint_issues | warning | external-only |
| drc_severity | lib_footprint_mismatch | warning | external-only |
| drc_severity | malformed_courtyard | error | external-only |
| drc_severity | microvia_drill_out_of_range | error | external-only |
| drc_severity | mirrored_text_on_front_layer | warning | external-only |
| drc_severity | missing_courtyard | ignore | external-only |
| drc_severity | missing_footprint | warning | external-only |
| drc_severity | missing_tuning_profile | warning | external-only |
| drc_severity | net_conflict | warning | external-only |
| drc_severity | nonmirrored_text_on_back_layer | warning | external-only |
| drc_severity | npth_inside_courtyard | error | external-only |
| drc_severity | padstack | warning | external-only |
| drc_severity | pth_inside_courtyard | error | external-only |
| drc_severity | shorting_items | error | external-only |
| drc_severity | silk_edge_clearance | warning | external-only |
| drc_severity | silk_over_copper | warning | external-only |
| drc_severity | silk_overlap | warning | external-only |
| drc_severity | skew_out_of_range | error | external-only |
| drc_severity | solder_mask_bridge | error | external-only |
| drc_severity | starved_thermal | error | external-only |
| drc_severity | text_height | warning | external-only |
| drc_severity | text_on_edge_cuts | error | external-only |
| drc_severity | text_thickness | warning | external-only |
| drc_severity | through_hole_pad_without_hole | error | external-only |
| drc_severity | too_many_vias | error | external-only |
| drc_severity | track_angle | error | external-only |
| drc_severity | track_dangling | warning | external-only |
| drc_severity | track_not_centered_on_via | ignore | external-only |
| drc_severity | track_on_post_machined_layer | error | external-only |
| drc_severity | track_segment_length | error | external-only |
| drc_severity | track_width | error | external-only |
| drc_severity | tracks_crossing | error | external-only |
| drc_severity | tuning_profile_track_geometries | ignore | external-only |
| drc_severity | unconnected_items | error | external-only |
| drc_severity | unresolved_variable | error | external-only |
| drc_severity | via_dangling | warning | external-only |
| drc_severity | zones_intersect | error | external-only |
| erc_severity | bus_definition_conflict | error | external-only |
| erc_severity | bus_entry_needed | error | external-only |
| erc_severity | bus_to_bus_conflict | error | external-only |
| erc_severity | bus_to_net_conflict | error | external-only |
| erc_severity | different_unit_footprint | error | external-only |
| erc_severity | different_unit_net | error | external-only |
| erc_severity | duplicate_reference | error | external-only |
| erc_severity | duplicate_sheet_names | error | external-only |
| erc_severity | endpoint_off_grid | ignore | external-only |
| erc_severity | extra_units | error | external-only |
| erc_severity | field_name_whitespace | warning | external-only |
| erc_severity | footprint_filter | ignore | external-only |
| erc_severity | footprint_link_issues | warning | external-only |
| erc_severity | four_way_junction | ignore | external-only |
| erc_severity | ground_pin_not_ground | warning | external-only |
| erc_severity | hier_label_mismatch | error | external-only |
| erc_severity | isolated_pin_label | warning | external-only |
| erc_severity | label_dangling | error | external-only |
| erc_severity | label_multiple_wires | warning | external-only |
| erc_severity | lib_symbol_issues | warning | external-only |
| erc_severity | lib_symbol_mismatch | warning | external-only |
| erc_severity | missing_bidi_pin | warning | external-only |
| erc_severity | missing_input_pin | warning | external-only |
| erc_severity | missing_power_pin | error | external-only |
| erc_severity | missing_unit | warning | external-only |
| erc_severity | multiple_net_names | warning | external-only |
| erc_severity | net_not_bus_member | warning | external-only |
| erc_severity | no_connect_connected | warning | external-only |
| erc_severity | no_connect_dangling | warning | external-only |
| erc_severity | pin_not_connected | error | external-only |
| erc_severity | pin_not_driven | error | external-only |
| erc_severity | pin_to_pin | error | external-only |
| erc_severity | power_pin_not_driven | ignore | external-only |
| erc_severity | same_local_global_label | warning | external-only |
| erc_severity | similar_label_and_power | warning | external-only |
| erc_severity | similar_labels | warning | external-only |
| erc_severity | similar_power | warning | external-only |
| erc_severity | simulation_model_issue | ignore | external-only |
| erc_severity | single_global_label | ignore | external-only |
| erc_severity | stacked_pin_name | warning | external-only |
| erc_severity | unannotated | error | external-only |
| erc_severity | unconnected_wire_endpoint | warning | external-only |
| erc_severity | undefined_netclass | error | external-only |
| erc_severity | unit_value_mismatch | error | external-only |
| erc_severity | unresolved_variable | error | external-only |
| erc_severity | wire_dangling | error | external-only |
| netclass:Default | bus_width | 12 | external-only-unproven |
| netclass:Default | clearance | 0.2 | translatable-not-equivalence-tested |
| netclass:Default | diff_pair_gap | 0.25 | external-only-unproven |
| netclass:Default | diff_pair_via_gap | 0.25 | external-only-unproven |
| netclass:Default | diff_pair_width | 0.2 | external-only-unproven |
| netclass:Default | line_style | 0 | external-only-unproven |
| netclass:Default | microvia_diameter | 0.3 | external-only-unproven |
| netclass:Default | microvia_drill | 0.1 | external-only-unproven |
| netclass:Default | name | Default | external-only-unproven |
| netclass:Default | pcb_color | rgba(0, 0, 0, 0.000) | external-only-unproven |
| netclass:Default | priority | 2147483647 | external-only-unproven |
| netclass:Default | schematic_color | rgba(0, 0, 0, 0.000) | external-only-unproven |
| netclass:Default | track_width | 0.2 | external-only-unproven |
| netclass:Default | tuning_profile |  | external-only-unproven |
| netclass:Default | via_diameter | 0.6 | external-only-unproven |
| netclass:Default | via_drill | 0.3 | external-only-unproven |
| netclass:Default | wire_width | 6 | external-only-unproven |
| erc | pin_map | [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2], [0, 2, 0, 1, 0, 0, 1, 0, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2], [0, 1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2], [0, 2, 1, 2, 0, 0, 1, 0, 0, 2, 2, 2], [0, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 2], [0, 2, 1, 1, 0, 0, 1, 0, 2, 0, 0, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]] | missing-native |
| keepout | PJ-002AH pad exclusion | tracks/vias/pads/pour prohibited; footprints allowed | partial-native |
| custom_rules | .dru | [] | source-absent |
| challenge | JLCPCB manufacturing | PCBGolf README | external-only |
| challenge | assembly feasibility | PCBGolf README | external-only |
| challenge | electrical functionality | PCBGolf README | external-only |
| challenge | mating connector compatibility | PCBGolf README | external-only |
| challenge | assembly volume/models | PCBGolf README | external-only |
