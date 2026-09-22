#!/usr/bin/env python3
"""Lab 3.2 — Merkle tree (starter, completed)."""
import hashlib

def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def merkle_root(leaves: list[bytes]) -> bytes:
    if not leaves:
        return H(b"")
    level = leaves[:]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        level = [H(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]

def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    proof = []
    level = leaves[:]
    idx = index
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        if idx % 2 == 0:
            sibling, sibling_is_left = level[idx + 1], False
        else:
            sibling, sibling_is_left = level[idx - 1], True
        proof.append((sibling, sibling_is_left))
        level = [H(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        idx //= 2
    return proof

def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    h = leaf_hash
    for sibling, sibling_is_left in proof:
        h = H(sibling + h) if sibling_is_left else H(h + sibling)
    return h == root

if __name__ == "__main__":
    txs = [f"tx{i}: A->B {i} coin".encode() for i in range(8)]
    leaves = [H(t) for t in txs]
    root = merkle_root(leaves)
    print("root:", root.hex())

    ok = all(verify_proof(leaves[i], merkle_proof(leaves, i), root) for i in range(8))
    print("CHECK 1 (all 8 proofs valid):", "OK" if ok else "FAIL")

    print("CHECK 2 (proof length == 3):", "OK" if len(merkle_proof(leaves, 4)) == 3 else "FAIL")

    fake = H(b"tx4: A->B 999999 coin")
    print("CHECK 3 (tampered leaf fails):",
          "OK" if not verify_proof(fake, merkle_proof(leaves, 4), root) else "FAIL")

    l7 = leaves[:7]
    r7 = merkle_root(l7)
    print("CHECK 4 (odd count works):",
          "OK" if all(verify_proof(l7[i], merkle_proof(l7, i), r7) for i in range(7)) else "FAIL")