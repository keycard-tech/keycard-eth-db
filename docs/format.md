# Database format

## Blob

Entries back to back. Each entry is a 4 byte header and its payload:

    magic  2 bytes, little endian
    len    2 bytes, payload length, header excluded

A published database is the version entry, all the chains, all the tokens, all the ABIs, and 64
bytes of signature over the SHA256 of everything before it. Nothing else is padded: the device
copies the entries into its own storage log, which aligns them as it writes.

    0x4532  version
    0x4348  chain
    0x3020  ERC-20
    0x4142  ABI

`tools/database-hash.py` prints the hash the signature is made on.

## Version

    version  4 bytes, little endian, YYYYMMDD

## Chain

    chain id      4 bytes, little endian
    ticker        null terminated ASCII
    network name  null terminated ASCII
    short name    null terminated ASCII

## ERC-20

    addresses  1 byte, count
    count times:
        chain id  4 bytes, little endian
        address   20 bytes
    decimals   1 byte
    ticker     null terminated ASCII

## ABI

A function struct, with its arguments as argument structs chained inside it. The 2 byte pointers
are offsets from the start of the struct holding them, 0 meaning absent.

Function, 13 byte header:

    selector      4 bytes, first 4 of keccak256 over the canonical signature
    ext selector  4 bytes, first 4 of keccak256 over the selector
    name          2 bytes, offset, always 13
    arguments     2 bytes, offset of the first argument
    attrs         1 byte, 1 when the function is payable
    name          null terminated ASCII
    arguments     the argument structs

Argument, 6 byte header, followed by the structs it points to:

    type    2 bytes
    next    2 bytes, offset of the next argument
    child   2 bytes, offset of the child type

Only functions whose stateMutability is payable or nonpayable are written.

### Types

Size in the low byte, kind in the high bits:

    uintN      0x1000 | N/8     uint alone is 32 bytes
    intN       0x1100 | N/8
    bool       0x1401
    address    0x1214
    bytesN     N
    bytes      0x2000
    string     0x2100
    tuple      0x4200   components in the child chain
    T[n]       0x4000 | n    element type in the child
    T[]        0x4100   element type in the child
    fixedNxM   0x1920
    ufixedNxM  0x1820

The fixed types keep their flag but take the 32 byte size of an integer.
