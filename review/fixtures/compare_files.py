from pathlib import Path
import sys
if len(sys.argv)!=3:
 print('Usage: python3 compare_files.py ORIGINAL RESTORED');sys.exit(2)
try:
 same=Path(sys.argv[1]).read_bytes()==Path(sys.argv[2]).read_bytes()
except OSError as e:
 print('ERROR: '+str(e));sys.exit(2)
print('PASS: files are byte-for-byte identical.' if same else 'FAIL: files differ.')
sys.exit(0 if same else 1)
