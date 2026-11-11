import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent

SOURCES = {
    "erc20.json": ("https://tokens.uniswap.org/", "ERC20 token list source"),
    "chain.json": ("https://chainid.network/chains.json", "Chain list source"),
    "abi.json": ("https://github.com/keycard-tech/eth-abi-repo/releases/latest/download/abi.json", "ABI list source"),
}

def fetch(name, url):
    # the token list CDN answers 403 to urllib's default User-Agent
    request = urllib.request.Request(url, headers={"User-Agent": "keycard-eth-db"})
    body = urllib.request.urlopen(request).read()
    # parsed before writing, so an error page never replaces a good source
    json.loads(body)
    (ROOT / name).write_bytes(body)
    print(f"{name} <- {url} ({len(body)} bytes)")

if __name__ == "__main__":
    for name, (url, label) in SOURCES.items():
        fetch(name, url)

    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [f"Sources fetched: {fetched}"]
    lines += [f"{label}: {url}" for url, label in SOURCES.values()]
    (ROOT / "manifest.txt").write_text("\n".join(lines) + "\n")
    print(f"manifest.txt ({fetched})")
