import hashlib

from secp256k1Crypto import PrivateKey

# Both values are properties of the Shell's flash, not of this database: the STM32H5 programs the
# data area in 16-byte words and erases it in 8kb pages.
PAGE_SIZE = 8192
WORD_SIZE = 16

def sign(sign_key, m):
    key = PrivateKey(bytes(bytearray.fromhex(sign_key)), raw=True)
    sig = key.ecdsa_sign(m, raw=True)
    return key.ecdsa_serialize_compact(sig)

def hash_db(db):
    h = hashlib.sha256()
    h.update(db[:-64])
    return h.digest()
