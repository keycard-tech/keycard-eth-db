# Keycard Shell Ethereum database

The chains, ERC-20 tokens and ABI definitions the Shell ships with, built into a binary it installs
over an update. Released independently of the firmware.

The three source lists are committed here. `manifest.txt` says when and from where they were
fetched.

## Setup

[uv](https://docs.astral.sh/uv/) and Python 3.10 or newer:

    uv venv
    uv sync

## Building

    uv run python tools/shell-db.py -t erc20.json -c chain.json -a abi.json -v 20261111 -o db.bin

The version is a date and defaults to today. Without a signing flag the entries are padded into
flash pages and nothing is appended, which is the shape flashed straight into the data area. With
`-s`, `-d` or `-k` they are written back to back the way the device receives them, plus the
trailing 64 bytes.

## Reproducing a published version

Unzip the version you want and rebuild it with `-d`:

    uv run python tools/shell-db.py -t erc20.json -c chain.json -a abi.json -v 20251127 -d -o db-out.bin
    uv run python tools/database-hash.py -b db-out.bin
    uv run python tools/database-hash.py -b <unzipped>/db.bin

The two hashes must be equal. Published files are signed with a key we do not publish, so the last
64 bytes are the only difference.

## Signing

`-s` signs with a hex secp256k1 key in a file, `-k` with a Keycard. `-d` puts a digest and zeroes
where the signature goes, enough to keep the length and the hash right for a comparison.
Production databases are signed offline and uploaded by hand.

## Refreshing the sources

    uv run python tools/fetch-sources.py

Overwrites the three lists and rewrites the manifest.

## Format

`docs/format.md`
