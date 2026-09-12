"""File-based native KiCad candidate evaluation. Never substitutes simulator gates."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from copper_scar.harness.score import compute_score
from copper_scar.scars.store import save_scar


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def design_files(root: Path) -> dict[str, str]:
    """Hash the CAD inputs, not local app history, git metadata or generated reports."""
    return {
        str(p.relative_to(root)): digest(p)
        for p in sorted(root.rglob("*"))
        if p.is_file() and ".git" not in p.relative_to(root).parts
        and (p.suffix in {".kicad_pcb", ".kicad_pro", ".kicad_sch", ".kicad_dru",
                          ".kicad_mod", ".kicad_sym", ".step", ".stp", ".wrl"}
             or p.name in {"fp-lib-table", "sym-lib-table"})
    }


def design_digest(files: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def _nodes(node: list, name: str) -> list[list]:
    return [n for n in node if isinstance(n, list) and n and str(n[0]) == name]


def board_inventory(path: Path) -> dict[str, Any]:
    import sexpdata

    board = sexpdata.loads(path.read_text())
    if not isinstance(board, list) or str(board[0]) != "kicad_pcb":
        raise ValueError("Not a KiCad board")
    layers = _nodes(board, "layers")[0]
    copper = [str(n[1]) for n in layers[1:] if isinstance(n, list) and str(n[1]).endswith(".Cu")]
    footprints = _nodes(board, "footprint")
    pins: dict[str, list[str]] = {}
    refs: list[str] = []
    missing_models: list[str] = []
    for fp in footprints:
        props = {str(n[1]): str(n[2]) for n in _nodes(fp, "property")}
        ref = props.get("Reference")
        if not ref or ref in refs:
            raise ValueError("Missing or duplicate footprint reference")
        refs.append(ref)
        models = _nodes(fp, "model")
        if not models:
            missing_models.append(ref)
        for model in models:
            model_path = str(model[1]).replace("${KIPRJMOD}", str(path.parent))
            if "${" in model_path or not Path(model_path).is_file():
                missing_models.append(f"{ref}: unresolved model {model[1]}")
        for pad in _nodes(fp, "pad"):
            # KiCad 10 uses (net "NAME"); previous versions use (net ID "NAME").
            nets = [str(n[-1]) for n in _nodes(pad, "net")]
            key = f"{ref}:{pad[1]}"
            pins[key] = sorted(set(pins.get(key, []) + nets))
    return {"footprints": len(footprints), "references": sorted(refs), "pin_nets": pins,
            "vias": len(_nodes(board, "via")), "tracks": len(_nodes(board, "segment")) + len(_nodes(board, "arc")),
            "copper_layers": len(copper), "missing_models": missing_models}


def native_report(raw: Any, kind: str, returncode: int, source: str) -> dict:
    """Fail on missing schema fields, invalid process status, or any reported violation."""
    if not isinstance(raw, dict) or not isinstance(raw.get("kicad_version"), str):
        raise ValueError("Missing native report metadata")
    if Path(raw.get("source", "")).name != source:
        raise ValueError("Native report source does not match checked input")
    if returncode not in (0, 5):
        raise ValueError(f"KiCad failed with exit code {returncode}")
    sheets = []
    if kind == "erc":
        sheets = raw.get("sheets")
        if not isinstance(sheets, list) or not sheets:
            raise ValueError("ERC report has no sheet coverage")
        groups = [sheet.get("violations") for sheet in sheets if isinstance(sheet, dict)]
        if len(groups) != len(sheets):
            raise ValueError("Invalid ERC sheet")
    else:
        groups = [raw.get(k) for k in ("violations", "unconnected_items", "schematic_parity")]
    if any(not isinstance(g, list) for g in groups):
        raise ValueError("Missing native violation arrays")
    violations = [v for g in groups for v in g]
    if any(not isinstance(v, dict) or not v.get("type") or not v.get("severity") for v in violations):
        raise ValueError("Invalid native violation")
    return {"ok": returncode == 0 and not violations, "count": len(violations),
            "violations": violations, "sheets": sheets}


def project_coverage(roots: list[dict], snapshot: Path, checks: dict) -> dict:
    """One native ERC invocation must cover the interconnected project, not isolated roots."""
    import sexpdata

    expected = {_nodes(sexpdata.loads((snapshot / root["filename"]).read_text()), "uuid")[0][1]
                for root in roots}
    seen_per_call = [{part for sheet in check.get("sheets", [])
                      for part in sheet.get("uuid_path", "").split("/") if part}
                     for name, check in checks.items() if name.startswith("erc-")]
    return {"ok": any(expected <= seen for seen in seen_per_call),
            "expected_root_uuids": sorted(expected),
            "observed_per_erc_call": [sorted(seen) for seen in seen_per_call],
            "note": "Separate isolated sheets cannot prove cross-sheet ERC or schematic parity"}


def run_command(args: list[str], directory: Path, name: str, timeout: int = 300) -> dict:
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        output = {"argv": args, "returncode": result.returncode}
        (directory / f"{name}.stdout.txt").write_text(result.stdout)
        (directory / f"{name}.stderr.txt").write_text(result.stderr)
    except (OSError, subprocess.TimeoutExpired) as exc:
        output = {"argv": args, "returncode": None, "error": str(exc)}
    (directory / f"{name}.command.json").write_text(json.dumps(output, indent=2) + "\n")
    return output


def step_volume(path: Path) -> dict:
    """Measure the exported assembly's axis-aligned envelope using OpenCascade."""
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    reader = STEPControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone or not reader.TransferRoots():
        raise ValueError("Cannot load assembly STEP")
    shape = reader.OneShape()
    if shape.IsNull():
        raise ValueError("Assembly STEP has no shape")
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    bounds = list(box.Get())
    lengths = [bounds[i + 3] - bounds[i] for i in range(3)]
    if any(not math.isfinite(x) or x <= 0 for x in lengths):
        raise ValueError("Invalid assembly envelope")
    return {"bounds_mm": bounds, "dimensions_mm": lengths,
            "volume_mm3": math.prod(lengths), "step_sha256": digest(path)}


def evaluate_candidate(project: Path, reference: Path, out_dir: Path, *,
                       kicad: str = "kicad-cli", copperhead: str | None = None,
                       qualification: Path | None = None, promote_to: Path | None = None) -> dict:
    """Snapshot candidate, run checks, persist evidence, optionally promote a qualified copy."""
    out_dir.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="candidate-", dir=out_dir.resolve()))
    failures: list[str] = []
    checks: dict[str, Any] = {}
    record: dict[str, Any] = {"schema_version": 1, "kind": "native-kicad-candidate",
        "created_at": datetime.now(timezone.utc).isoformat(), "run_dir": str(run_dir),
        "checks": checks, "failures": failures, "metrics": None, "score": None,
        "gates_ok": False, "promoted": False}
    snapshot = run_dir / "project"
    try:
        project, reference = project.resolve(strict=True), reference.resolve(strict=True)
        if project.suffix != ".kicad_pro" or reference.name != project.name:
            raise ValueError("Candidate and reference require matching .kicad_pro basenames")
        if run_dir.is_relative_to(project.parent):
            raise ValueError("Output directory must be outside candidate project")
        if any(p.is_symlink() for p in project.parent.rglob("*") if ".git" not in p.parts):
            raise ValueError("Candidate project must contain files, not symlinks")
        shutil.copytree(project.parent, snapshot, ignore=shutil.ignore_patterns(".git", "reports", "*-backups"))
        files = design_files(snapshot)
        reference_files = design_files(reference.parent)
        fingerprint = design_digest(files)
        record.update({"design_sha256": fingerprint, "files": files,
                       "reference_sha256": design_digest(reference_files)})
        board_name = project.with_suffix(".kicad_pcb").name
        changes = sorted(k for k in set(files) | set(reference_files)
                         if k != board_name and files.get(k) != reference_files.get(k))
        checks["original_inputs_preserved"] = {"ok": not changes, "changed": changes}
        if changes:
            failures.append("Original schematics, rules, libraries or models changed; review required")
        inventory = board_inventory(snapshot / board_name)
        original = board_inventory(reference.with_suffix(".kicad_pcb"))
        record["board_inventory"] = inventory
        parity = inventory["pin_nets"] == original["pin_nets"] and inventory["references"] == original["references"]
        checks["original_pin_nets"] = {"ok": parity}
        if not parity:
            failures.append("Reference/pad/net mapping differs from original challenge board")
        config = json.loads((snapshot / project.name).read_text())
        roots = config["schematic"]["top_level_sheets"]
        if not roots or any(not isinstance(s.get("filename"), str) for s in roots):
            raise ValueError("Missing explicit top-level schematic coverage")
        version = run_command([kicad, "version"], run_dir, "version")
        if version["returncode"] != 0:
            raise ValueError("KiCad executable unavailable; see version.command.json")
        version_text = (run_dir / "version.stdout.txt").read_text().strip()
        record["kicad_version"] = version_text
        if int(version_text.split(".")[0]) < 10:
            raise ValueError("Official challenge requires KiCad 10 or newer")
        targets = [(f"erc-{i}", "erc", root["filename"]) for i, root in enumerate(roots)]
        targets.append(("drc", "drc", board_name))
        for name, kind, filename in targets:
            input_path = snapshot / filename
            if not input_path.is_file() or not input_path.resolve().is_relative_to(snapshot):
                raise ValueError(f"Missing or invalid native input: {filename}")
            report = run_dir / f"{name}.json"
            args = [kicad, "sch" if kind == "erc" else "pcb", kind, "--format", "json",
                    "--severity-all", "--exit-code-violations", "--output", str(report)]
            if kind == "drc":
                args += ["--all-track-errors", "--schematic-parity", "--refill-zones"]
            command = run_command(args + [str(input_path)], run_dir, name)
            try:
                checks[name] = native_report(json.loads(report.read_text()), kind, command["returncode"], filename)
            except (OSError, ValueError, TypeError, KeyError) as exc:
                checks[name] = {"ok": False, "error": str(exc)}
            if not checks[name]["ok"]:
                failures.append(f"{name} failed or evidence missing")
        checks["schematic_project_coverage"] = project_coverage(roots, snapshot, checks)
        if not checks["schematic_project_coverage"]["ok"]:
            failures.append("Whole-project schematic coverage unresolved; individual-sheet diagnostics only")
        if copperhead:
            # Secondary convenience check. Native evidence above remains authoritative.
            cp = run_command([copperhead, "--repo", str(snapshot), "--json", "check"], run_dir, "copperhead")
            try:
                summary = json.loads((run_dir / "copperhead.stdout.txt").read_text())
                cp_ok = cp["returncode"] == 0 and summary.get("ok") is True and all(
                    isinstance(summary.get(k), dict) and summary[k].get("ok") is True for k in ("erc", "drc"))
            except (OSError, ValueError, AttributeError):
                cp_ok = False
            checks["copperhead"] = {"ok": cp_ok}
            if not cp_ok:
                failures.append("Copperhead check failed")
        checks["assembly_models"] = {"ok": not inventory["missing_models"], "missing": inventory["missing_models"]}
        if inventory["missing_models"]:
            failures.append("Assembly models incomplete; no qualified assembly score")
        if checks["drc"]["ok"] and checks["assembly_models"]["ok"]:
            assembly = run_dir / "assembly.step"
            exported = run_command([kicad, "pcb", "export", "step", "--output", str(assembly), str(snapshot / board_name)],
                                   run_dir, "step-export")
            if exported["returncode"] != 0:
                raise ValueError("STEP export failed")
            envelope = step_volume(assembly)
            record["assembly"] = envelope
            record["metrics"] = {"volume_mm3": envelope["volume_mm3"], "vias": inventory["vias"],
                                 "copper_layers": inventory["copper_layers"]}
            record["score"] = compute_score(**record["metrics"])
        review = json.loads(qualification.read_text()) if qualification else {}
        # Human engineering review is separate from ERC/DRC; never fabricate these flags.
        qualified = review.get("design_sha256") == fingerprint and bool(review.get("reviewer")) and all(
            review.get(k) is True for k in ("manufacturing", "assembly", "electrical", "connector_compatibility"))
        checks["engineering_review"] = {"ok": qualified, "evidence": review}
        if not qualified:
            failures.append("Candidate-bound engineering qualification is missing")
        if design_files(snapshot) != files:
            failures.append("CAD inputs changed during checks")
        record["gates_ok"] = not failures and record["metrics"] is not None
        if promote_to and record["gates_ok"]:
            # Never overwrite a previous best board. This is an explicit, reviewable destination.
            shutil.copytree(snapshot, promote_to)
            record["promoted"] = True
            record["promoted_to"] = str(promote_to.resolve())
    except (OSError, ValueError, KeyError, IndexError, TypeError, ImportError) as exc:
        failures.append(str(exc))
        record["gates_ok"] = False
    save_scar(record, run_dir / "failure-record.json")
    return record


def run_real_cli(args: Any) -> int:
    result = evaluate_candidate(Path(args.project), Path(args.reference), Path(args.out_dir),
        kicad=args.kicad, copperhead=args.copperhead,
        qualification=Path(args.qualification) if args.qualification else None,
        promote_to=Path(args.promote_to) if args.promote_to else None)
    print(json.dumps({k: result[k] for k in ("run_dir", "gates_ok", "score", "promoted", "failures")}, indent=2))
    return 0 if result["gates_ok"] else 1
