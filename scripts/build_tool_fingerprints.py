#!/usr/bin/env python3
"""Refresh the individual-tool checker from the exact files shipped in docs/."""
import hashlib
import re
from pathlib import Path
DOCS = Path(__file__).resolve().parents[1] / 'docs'
TOOLS = {'converter': 'dice-converter.html', 'descriptor': 'descriptor-tool.html', 'mapper': 'diceware-mapper.html'}
def build():
    path = DOCS / 'fingerprint-checker.html'
    text = path.read_text()
    for key, filename in TOOLS.items():
        digest = hashlib.sha256((DOCS / filename).read_bytes()).hexdigest()
        text, count = re.subn(r"('" + key + r"': ')[a-f0-9]{64}(')", lambda m: m[1] + digest + m[2], text)
        if count != 1:
            raise ValueError('Expected exactly one fingerprint slot for ' + key)
    path.write_text(text)
if __name__ == '__main__':
    build()
