#!/usr/bin/env python3
"""Give Tor Browser temporary read access to this extracted public-test folder.

Run on the Tails host with Python, after checking the package. This does not
start a web server, change network settings or launch any wallet tool.
"""
from pathlib import Path
import subprocess
import sys


def export_folder(folder):
    folder = Path(folder).resolve()
    if (folder / 'START.html').is_file() and (folder / 'verify_package.py').is_file():
        landing = 'START.html'
    elif all((folder / name).is_file() for name in
             ('TESTING.txt', 'dice-converter.html', 'verify_package.py')):
        landing = 'dice-converter.html'
    else:
        raise ValueError('Run the helper supplied inside the extracted package, not a separately downloaded copy.')
    result = subprocess.run(
        ['flatpak', 'document-export', '--unique', '--transient',
         '--app=org.boum.tails.TorBrowser', str(folder)],
        check=True, capture_output=True, text=True, timeout=30)
    exported = result.stdout.strip()
    if not exported or '\n' in exported or not Path(exported).is_absolute():
        raise ValueError('Flatpak did not return one absolute folder path. Stop and record its output.')
    return (Path(exported) / landing).as_uri()


def main():
    print('Keep OS networking disabled. Use only the verified public-test package.')
    print('Giving Tor Browser temporary read access to this extracted folder...')
    try:
        url = export_folder(Path(__file__).resolve().parent)
    except FileNotFoundError:
        print('STOP: Flatpak is unavailable. This helper is for Tails with Flatpak Tor Browser.', file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print('STOP: folder access was not granted. Record this error:', file=sys.stderr)
        print(error.stderr.strip(), file=sys.stderr)
        return 1
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print('STOP: ' + str(error), file=sys.stderr)
        return 1
    print('\nCopy this WHOLE address into Tor Browser\'s address bar, then press Enter:\n')
    print(url)
    print('\nContinue through the links on that page. Close earlier broken tabs.')
    print('Run this helper again after a new Tails boot or a moved/re-extracted folder.')
    print('It does not verify the package or prove that networking is disabled.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
