# delego — Wire Specification

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-green.svg)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Spec](https://img.shields.io/badge/spec-v0.3-blue.svg)](spec.md)

delego is a **deterministic pre-action authorization layer for AI agents**: it
sits between an agent that proposes actions and the credential broker that
executes them, and answers, for each action, `allow` / `needs_approval` / `deny`
— with no language model in the decision path, before any credential is used,
bound to the originating human instruction and the exact action, and recorded in
a tamper-evident, signed audit chain. It addresses the agent-authorization gap
catalogued as **OWASP ASI03 (Excessive Agency)**.

This repository is the source of truth for the protocol. The reference
implementation is **[delego](https://github.com/Delego-Dev/delego)**.

## Table of Contents

- [About](#about)
- [Read the spec](#read-the-spec)
- [Ecosystem](#ecosystem)
- [Conformance](#conformance)
- [Status & versioning](#status--versioning)
- [Contributing](#contributing)
- [License](#license)

## About

Credential brokers ensure an agent never holds a raw secret — but they can't
tell whether *this specific action* is the thing the human authorized. So a
prompt injection can redirect an in-scope, validly-credentialed action: the
**confused deputy**. delego is the **Policy Decision Point (PDP)** that authorizes
the *action* against a deterministic policy before any credential is used, binds
it to the human instruction, requires human approval for sensitive actions, and
writes a signed, hash-chained audit trail; the credential broker is the **Policy
Enforcement Point (PEP)** and the only component that ever touches a credential.
("Firewall" is sometimes used as a loose analogy for this — but delego is an
action-authorization layer, not a network firewall; see
[§11](spec.md#11-security-considerations).)

This specification exists so that independent **authorizers**, **brokers**, and
**auditors** — written by different people, in different languages — agree
byte-for-byte.

## Read the spec

📜 **[spec.md](spec.md)** — the normative protocol.

- [Canonicalization](spec.md#3-canonicalization-normative)
- [Proposed Action & hashing](spec.md#4-proposed-action)
- [Policy & decisions](spec.md#5-policy)
- [Approval binding — the confused-deputy guard](spec.md#7-approval-binding-the-confused-deputy-guard)
- [Authorization properties (P1–P4)](spec.md#71-authorization-properties-normative-03-draft--additive)
- [Receipt & audit chain](spec.md#8-receipt--audit-chain-normative)
- [Authorization Token](spec.md#9-authorization-token-optional-profile)

## Ecosystem

| Component | What it is |
|-----------|------------|
| **[Specification](spec.md)** | This document — the protocol. |
| **[Schemas](schema/)** | JSON Schemas for the policy, the audit receipt, and the authorization token. |
| **[Conformance Test Kit](ctk/README.md)** | Language-agnostic vectors any implementation can check itself against. |
| **[delego](https://github.com/Delego-Dev/delego)** | The reference implementation (Python) — policy engine, CLI, and MCP server. |

Planned (open source): broker adapters that verify authorization tokens, and
language SDKs. Contributions welcome.

## Conformance

The [Conformance Test Kit](ctk/README.md) ships authoritative vectors generated
by the reference implementation — action → hashes, policy + action → decision,
and signed chains (valid and tampered). A conformant implementation MUST
reproduce them; see [§10 Conformance](spec.md#10-conformance).

## Status & versioning

**v0.3 — frozen.** The spec/protocol is versioned `0.x` (the reference *package*
is `0.x.y`). 0.1–0.2 are reference-backed; each prior protocol version has a
standalone document of record in [`versions/`](versions/README.md)
([0.1](versions/spec-v0.1.md), [0.2](versions/spec-v0.2.md) — what the reference
implements today). 0.3 adds **additive hardening clauses**
— the §4.2 Broker query obligation, policy-schema validation (§5.1), the
authorization properties P1–P4 (§7.1), head-anchoring (§8.3), and the
authorization-token profile (§9) — which tighten obligations **without changing
any hashed or signed bytes** and so MAY be adopted on the 0.2 preimage. One item
is **deferred**: folding the URL query into the `action_fingerprint` preimage
(§4.2) is a breaking change held for a later draft. See the
[§2.1 version matrix](spec.md#21-protocol-versions). A breaking change to the
receipt fields bumps the version (see [§8.2](spec.md#82-schema-versioning)).

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)**. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md). Propose changes by opening an issue or a
pull request; a change to a NORMATIVE section should come with updated
[CTK vectors](ctk/README.md).

## License

[Apache License 2.0](LICENSE).
