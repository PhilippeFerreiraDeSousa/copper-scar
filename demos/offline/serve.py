#!/usr/bin/env python3
"""Serve offline files on loopback only. Directly opening index.html also works."""
import http.server, os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
print('Copper Scar offline replay: http://127.0.0.1:8765')
http.server.ThreadingHTTPServer(('127.0.0.1',8765),http.server.SimpleHTTPRequestHandler).serve_forever()
