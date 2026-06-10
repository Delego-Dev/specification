#!/usr/bin/env python3
"""Replay the Conformance Test Kit against the reference implementation.

This is the gate that keeps the **spec ahead of the code**: it reproduces every
CTK vector with the installed ``delego`` reference and asserts the reference's
protocol version never exceeds this document's version. CI fails on any drift.

Run locally or in CI:  python conformance.py
Requires: the ``delego`` reference (``pip install delego`` or from git), pyyaml.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VEC = ROOT / "ctk" / "vectors"
fails = 0


def fail(msg: str) -> None:
    global fails
    fails += 1
    print(f"  FAIL {msg}")


def ok(msg: str) -> None:
    print(f"  ok   {msg}")


try:
    import delego
    from delego import ProposedAction, build_firewall
    from delego.config import Paths
except ImportError:  # pragma: no cover
    print("delego is not installed; install the reference to run conformance.")
    print("  pip install delego        # or: pip install git+https://github.com/Delego-Dev/delego")
    sys.exit(1)


def spec_version() -> tuple[int, ...]:
    text = (ROOT / "spec.md").read_text(encoding="utf-8")
    # Spec/protocol versions are two-component (0.x); tolerate a patch too.
    m = re.search(r"\*\*Version:\*\*\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)", text)
    return tuple(int(x) for x in m.group(1).split("."))


def ver(s: str) -> tuple[int, ...]:
    return tuple(int(x) for x in s.split("."))


def build(policy_name: str = "examples/policy.example.yaml"):
    home = Path(tempfile.mkdtemp())
    shutil.copy(ROOT / policy_name, home / "policy.yaml")
    return build_firewall(Paths.resolve(home))


def action(a: dict) -> ProposedAction:
    return ProposedAction(a["instruction"], a["method"], a["url"], a.get("params", {}))


# --- spec leads the reference ------------------------------------------------ #
print("protocol version:")
ref = getattr(delego, "__protocol_version__", None)
if ref is None:
    fail("reference does not expose __protocol_version__")
elif ver(ref) > spec_version():
    fail(f"reference protocol {ref} EXCEEDS spec {'.'.join(map(str, spec_version()))} — spec must lead")
else:
    ok(f"reference {ref} <= spec {'.'.join(map(str, spec_version()))}")

# --- §4 hashing -------------------------------------------------------------- #
print("hashing (§4):")
for e in json.loads((VEC / "hashing.json").read_text()):
    a = action(e["action"])
    if a.intent_hash == e["intent_hash"] and a.fingerprint == e["action_fingerprint"]:
        ok(e["action"]["url"])
    else:
        fail(f"hash mismatch for {e['action']['url']}")

# --- §5–§6 decisions --------------------------------------------------------- #
print("decisions (§5–§6):")
for e in json.loads((VEC / "decisions.json").read_text()):
    fw = build()
    got = list(fw.policy.evaluate(action(e["action"]), fw.audit))
    if got == [e["outcome"], e["rule"], e["reasons"]]:
        ok(f"{e['outcome']:14} {e['action']['url']}")
    else:
        fail(f"decision {got} != {[e['outcome'], e['rule'], e['reasons']]}")

# --- §7 resolve / approval lifecycle (0.2) ----------------------------------- #
print("resolve (§7, 0.2):")
for e in json.loads((VEC / "resolve.json").read_text()):
    fw = build()
    approval_id = "apr_vector"
    if e["approval"] is not None:
        rec = {
            "id": approval_id,
            "status": e["approval"]["status"],
            "action_fingerprint": e["approval"]["action_fingerprint"],
            "intent_hash": e["approval"]["intent_hash"],
            "rule": e["approval"].get("rule"),
            "instruction": e["presented_action"]["instruction"],
            "summary": "",
            "approver": "human",
            "created_at": None,
            "decided_at": None,
        }
        fw.approvals._append(rec)  # seed the store with the vector's parked approval
    d = fw.resolve(approval_id, action(e["presented_action"]))
    want = e["expected"]
    if d.outcome == want["outcome"] and any(want["reason_contains"] in r for r in d.reasons):
        ok(f"{d.outcome:14} {e['name']}")
    else:
        fail(f"{e['name']}: got ({d.outcome}, {d.reasons}) want {want}")

# --- §8.1 chain verification ------------------------------------------------- #
print("chain verification (§8.1):")


def verify_chain(jsonl: str):
    from cryptography.hazmat.primitives import serialization
    from delego.audit import AuditLog

    home = Path(tempfile.mkdtemp())
    shutil.copy(VEC / "signing_key.pub", home / "signing_key.pub")
    log = AuditLog(home / "audit.log.jsonl", home / "signing_key.pem", home / "signing_key.pub")
    shutil.copy(VEC / jsonl, log.path)
    log._pub = serialization.load_pem_public_key((home / "signing_key.pub").read_bytes())
    log._load_keys = lambda: None
    return log.verify()


valid, _ = verify_chain("chain.jsonl")
exp = json.loads((VEC / "chain.expected.json").read_text())
ok("chain.jsonl valid") if valid == exp["valid"] else fail("chain.jsonl validity mismatch")

tvalid, tprobs = verify_chain("chain.tampered.jsonl")
texp = json.loads((VEC / "chain.tampered.expected.json").read_text())
if tvalid == texp["valid"] and tprobs == texp["problems"]:
    ok("chain.tampered.jsonl fails as expected")
else:
    fail(f"tampered chain: got valid={tvalid} problems={tprobs}")

# --- §9 authorization token (optional profile, reference >= 0.3.3) ------------ #
# The reference implements the §9 token profile from 0.3.3; replay the verifier
# vectors. Skipped (not failed) on an older reference that lacks verify_token.
try:
    from delego.token import TokenError, verify_token
except ImportError:
    print("token (§9): reference < 0.3.3 — token profile not implemented, skipping")
else:
    print("token (§9 / §9.1):")
    from cryptography.hazmat.primitives import serialization as _ser

    _pub = _ser.load_pem_public_key((VEC / "token_signing_key.pub").read_bytes())
    _tok = json.loads((VEC / "token.json").read_text())
    _leeway = _tok.get("_leeway_seconds", 60)
    for c in _tok["cases"]:
        try:
            claims = verify_token(
                c["token"], public_key=_pub, audience=c["audience"], now=c["now"], leeway=_leeway
            )
            got = "accept"
        except TokenError:
            claims, got = None, "reject"
        if got != c["expect"]:
            fail(f"token: {c['name']}: got {got}, want {c['expect']}")
        elif got == "accept" and not all(claims.get(k) == v for k, v in c.get("expected_claims", {}).items()):
            fail(f"token: {c['name']}: claims mismatch")
        else:
            ok(f"{got:6} {c['name']}")

print()
if fails:
    print(f"{fails} conformance failure(s) — reference does not match the spec's CTK.")
    sys.exit(1)
print("reference reproduces every CTK vector; spec leads the reference.")
