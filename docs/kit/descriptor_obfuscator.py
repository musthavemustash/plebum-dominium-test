#!/usr/bin/env python3
"""Plebum Dominium public-test wallet-map file encryption (GnuPG required)."""
import argparse
import getpass
from pathlib import Path
import subprocess
import sys

TOOL_VERSION = '2026.11.06-t4.1'
S2K_COUNT = '65011712'


def wipe(secret):
    if secret is not None:
        for i in range(len(secret)):
            secret[i] = 0


def read_passphrase(confirm=False):
    # getpass hides all typing on Windows; never echo the password.
    for _ in range(3):
        first = getpass.getpass('Map passphrase (typing hidden): ')
        if not first:
            raise ValueError('Passphrase cannot be empty.')
        if '\n' in first or '\r' in first or '\x00' in first:
            raise ValueError('Passphrase cannot contain line breaks or NUL.')
        if not confirm or getpass.getpass('Map passphrase again: ') == first:
            return bytearray(first.encode('utf-8'))
        print('[ERROR] Passphrases do not match. Try again.')
    raise ValueError('Too many mismatches.')


def gpg_run(args, payload, passphrase):
    """Use one anonymous stdin pipe on all platforms: password line, then data.

    GnuPG reads the password line from fd 0 before reading its input payload.
    No pass_fds, shell, password argument, environment variable, or temp file.
    Immutable Python/subprocess buffers cannot be reliably wiped.
    """
    if any(c in passphrase for c in (0, 10, 13)):
        raise ValueError('Passphrase cannot contain line breaks or NUL.')
    proc = subprocess.run(
        ['gpg', '--batch', '--pinentry-mode', 'loopback',
         '--no-symkey-cache', '--passphrase-fd', '0', *args],
        input=bytes(passphrase) + b'\n' + payload,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode:
        # Withhold any partial plaintext emitted by GnuPG on integrity failure.
        raise RuntimeError('GPG operation failed. Incorrect passphrase, damaged file, or unsupported GPG setup.')
    return proc.stdout


def encrypt_descriptor(plaintext, passphrase):
    return gpg_run([
        '--rfc4880', '--symmetric', '--cipher-algo', 'AES256',
        '--s2k-mode', '3', '--s2k-digest-algo', 'SHA512',
        '--s2k-count', S2K_COUNT, '--armor',
    ], plaintext, passphrase)


def decrypt_descriptor(ciphertext, passphrase):
    return gpg_run(['--decrypt'], ciphertext, passphrase)


def write_output(path, data):
    # Exclusive create prevents an unnoticed overwrite, including after a race.
    try:
        with path.open('xb') as handle:
            handle.write(data)
    except FileExistsError:
        raise ValueError('Output already exists. Choose a new output filename.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--encrypt', metavar='INPUT', type=Path)
    mode.add_argument('--decrypt', metavar='INPUT', type=Path)
    parser.add_argument('--output', type=Path, help='New output file; existing files are never overwritten')
    parser.add_argument('--version', action='version', version=TOOL_VERSION)
    args = parser.parse_args()
    print('PLEBUM DOMINIUM — WALLET MAP FILE ENCRYPTION TOOL')
    print('Version:', TOOL_VERSION)
    print('PUBLIC TEST ONLY. Disconnect networking before testing. Use no real wallet secrets.')
    passphrase = None
    try:
        subprocess.run(['gpg', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if args.encrypt is not None or args.decrypt is not None:
            encrypting = args.encrypt is not None
            source = args.encrypt if encrypting else args.decrypt
        else:
            choice = input('Choice ([E]ncrypt / [D]ecrypt / [Q]uit): ').strip().lower()
            if choice in ('q', 'quit'):
                return 0
            if choice not in ('e', 'd'):
                raise ValueError('Choose E, D, or Q.')
            encrypting = choice == 'e'
            source = Path(input('Input file path (drag in a file or paste its path): ').strip().strip('"'))
        target = args.output
        if target is None:
            if args.encrypt is not None or args.decrypt is not None:
                raise ValueError('--output is required with --encrypt or --decrypt.')
            target = Path(input('New output file path: ').strip().strip('"'))
        if source.resolve() == target.resolve():
            raise ValueError('Input and output must be different files.')
        if target.exists():
            raise ValueError('Output already exists. Choose a new output filename.')
        payload = source.read_bytes()
        if not payload:
            raise ValueError('Input file is empty.')
        passphrase = read_passphrase(confirm=encrypting)
        result = encrypt_descriptor(payload, passphrase) if encrypting else decrypt_descriptor(payload, passphrase)
        write_output(target, result)
        print('[OK] Written:', target)
        print('Preserve the original until the saved file has been reopened, decrypted, and compared exactly.')
        return 0
    except (KeyboardInterrupt, EOFError):
        print('\n[NOTICE] Cancelled.')
        return 1
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print('[ERROR]', exc)
        return 1
    finally:
        wipe(passphrase)


if __name__ == '__main__':
    sys.exit(main())
