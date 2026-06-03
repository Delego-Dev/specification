#!/usr/bin/env python3
"""Validate the spec's examples and CTK vectors against the JSON Schemas.

Run locally or in CI:  python validate.py
Requires: jsonschema, pyyaml.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
errors = 0


def load(rel: str):
    text = (ROOT / rel).read_text(encoding="utf-8")
    return yaml.safe_load(text) if rel.endswith((".yaml", ".yml")) else json.loads(text)


def check(name: str, instance, schema) -> None:
    global errors
    found = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: e.path)
    if found:
        errors += 1
        print(f"  FAIL {name}")
        for e in found:
            loc = "/".join(map(str, e.path)) or "<root>"
            print(f"        {loc}: {e.message}")
    else:
        print(f"  ok   {name}")


policy_schema = load("schema/policy.json")
receipt_schema = load("schema/receipt.json")
token_schema = load("schema/authorization-token.json")

print("policy:")
check("examples/policy.example.yaml", load("examples/policy.example.yaml"), policy_schema)

print("receipts (chain.jsonl):")
for i, line in enumerate((ROOT / "ctk/vectors/chain.jsonl").read_text().splitlines()):
    if line.strip():
        check(f"chain receipt[{i}]", json.loads(line), receipt_schema)

print("authorization token:")
check("examples/authorization-token.json", load("examples/authorization-token.json"), token_schema)

print()
if errors:
    print(f"{errors} schema validation failure(s).")
    sys.exit(1)
print("all examples and vectors validate against the schemas.")
