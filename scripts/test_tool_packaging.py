"""Check deterministic assembly and rejection of mismatched candidate files."""
import tempfile
from pathlib import Path
from prepare_tool_candidate import ROOT, build, check

with tempfile.TemporaryDirectory() as temp:
    first, second = Path(temp) / 'first', Path(temp) / 'second'
    build(first)
    build(second)
    check(first)
    check(second)
    assert {p.name: p.read_bytes() for p in first.iterdir()} == {p.name: p.read_bytes() for p in second.iterdir()}
    with (first / 'dice-converter.html').open('ab') as f:
        f.write(b'changed')
    try:
        check(first)
    except AssertionError:
        pass
    else:
        raise AssertionError('Tampered standalone file accepted')
    try:
        build(ROOT / 'docs/candidate')
    except ValueError:
        pass
    else:
        raise AssertionError('Published candidate output accepted')
print('PASS: deterministic ZIP/manifest/verifier; tampering rejected; repository writes rejected')
