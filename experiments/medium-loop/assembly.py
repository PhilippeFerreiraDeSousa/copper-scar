"""Read-only native inventory and OpenCascade envelope helpers from small-loop9af03f0."""

from __future__ import annotations

from pathlib import Path

from typing import Any

import hashlib,math

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

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
