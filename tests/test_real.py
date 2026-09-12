"""Native gate contract tests. These mocks do not establish real PCB validity."""

import json
from pathlib import Path

import pytest

from copper_scar.real import board_inventory, evaluate_candidate, native_report, project_coverage, step_volume


def drc_report():
    return {"kicad_version": "10.0.6", "source": "pcbgolf.kicad_pcb",
            "violations": [], "unconnected_items": [], "schematic_parity": []}


def test_native_report_requires_complete_evidence():
    for payload in ({}, {"kicad_version": "10.0.6"}, {**drc_report(), "unconnected_items": None}):
        with pytest.raises(ValueError):
            native_report(payload, "drc", 0, "pcbgolf.kicad_pcb")
    with pytest.raises(ValueError, match="source"):
        native_report(drc_report(), "drc", 0, "wrong.kicad_pcb")
    with pytest.raises(ValueError, match="exit code"):
        native_report(drc_report(), "drc", 2, "pcbgolf.kicad_pcb")
    assert not native_report(drc_report(), "drc", 5, "pcbgolf.kicad_pcb")["ok"]


@pytest.mark.parametrize("key", ["violations", "unconnected_items", "schematic_parity"])
def test_every_native_failure_blocks(key):
    report = drc_report()
    report[key] = [{"type": "unconnected_items", "severity": "warning"}]
    assert not native_report(report, "drc", 0, "pcbgolf.kicad_pcb")["ok"]


def test_erc_requires_sheet_coverage():
    with pytest.raises(ValueError, match="coverage"):
        native_report({"kicad_version": "10.0.6", "source": "a.kicad_sch", "sheets": []},
                      "erc", 0, "a.kicad_sch")


def test_isolated_roots_do_not_prove_project_coverage(tmp_path):
    roots = [{"filename": "a.kicad_sch"}, {"filename": "b.kicad_sch"}]
    for name in ("a", "b"):
        (tmp_path / f"{name}.kicad_sch").write_text(f'(kicad_sch (uuid "{name}"))')
    isolated = {"erc-0": {"sheets": [{"uuid_path": "/a"}]},
                "erc-1": {"sheets": [{"uuid_path": "/b"}]}}
    assert not project_coverage(roots, tmp_path, isolated)["ok"]
    combined = {"erc-0": {"sheets": [{"uuid_path": "/a"}, {"uuid_path": "/b"}]}}
    assert project_coverage(roots, tmp_path, combined)["ok"]


def project_fixture(root: Path):
    root.mkdir()
    project = root / "pcbgolf.kicad_pro"
    project.write_text(json.dumps({"schematic": {"top_level_sheets": [{"filename": "pcbgolf.kicad_sch"}]}}))
    project.with_suffix(".kicad_sch").write_text('(kicad_sch)')
    project.with_suffix(".kicad_pcb").write_text('''(kicad_pcb
      (layers (0 "F.Cu" signal) (2 "B.Cu" signal))
      (footprint "X" (property "Reference" "R1") (pad "1" smd rect (net "GND"))))''')
    return project


def test_missing_tool_records_failure_and_never_promotes(tmp_path):
    reference = project_fixture(tmp_path / "reference")
    candidate = project_fixture(tmp_path / "candidate")
    result = evaluate_candidate(candidate, reference, tmp_path / "reports",
                                kicad=str(tmp_path / "absent"), promote_to=tmp_path / "best")
    assert not result["gates_ok"] and not result["promoted"]
    assert result["score"] is None
    assert not (tmp_path / "best").exists()
    assert (Path(result["run_dir"]) / "failure-record.json").is_file()
    assert "KiCad executable unavailable" in result["failures"][0]
    assert candidate.with_suffix(".kicad_pcb").read_text() == reference.with_suffix(".kicad_pcb").read_text()


def test_changed_project_rules_and_net_mapping_are_recorded(tmp_path):
    reference = project_fixture(tmp_path / "reference")
    candidate = project_fixture(tmp_path / "candidate")
    candidate.write_text(candidate.read_text() + "\n")
    board = candidate.with_suffix(".kicad_pcb")
    board.write_text(board.read_text().replace('"GND"', '"VCC"'))
    result = evaluate_candidate(candidate, reference, tmp_path / "reports", kicad=str(tmp_path / "absent"))
    assert not result["checks"]["original_inputs_preserved"]["ok"]
    assert not result["checks"]["original_pin_nets"]["ok"]
    assert not result["gates_ok"]


def test_inventory_handles_duplicate_pad_numbers(tmp_path):
    project = project_fixture(tmp_path / "reference")
    inventory = board_inventory(project.with_suffix(".kicad_pcb"))
    assert inventory["pin_nets"] == {"R1:1": ["GND"]}
    assert inventory["missing_models"] == ["R1"]
    assert inventory["copper_layers"] == 2


def test_step_envelope_measures_assembly_not_board_thickness(tmp_path):
    pytest.importorskip("OCP")
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
    from OCP.IFSelect import IFSelect_RetDone

    path = tmp_path / "assembly.step"
    writer = STEPControl_Writer()
    writer.Transfer(BRepPrimAPI_MakeBox(10, 20, 7).Shape(), STEPControl_AsIs)
    assert writer.Write(str(path)) == IFSelect_RetDone
    result = step_volume(path)
    assert result["dimensions_mm"] == pytest.approx([10, 20, 7])
    assert result["volume_mm3"] == pytest.approx(1400)
