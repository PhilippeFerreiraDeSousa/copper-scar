"""Compatibility launcher for the shared native electrical/mechanical pad checker."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1]/'pcb-loop/native_geometry.py'),run_name='__main__')
