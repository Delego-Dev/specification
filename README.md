# delego — Wire Specification

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-green.svg)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Spec](https://img.shields.io/badge/spec-v0.3--draft-orange.svg)](spec.md)

The open specification for **delego** — a deterministic **authorization & audit
protocol for AI-agent actions**. It defines how an action proposed by an agent
is authorized (with no LLM in the decision path) *before* any credential is used,
bound to the originating human instruction, and recorded in a tamper-evident,
signed audit chain.

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
**confused deputy**. delego authorizes the *action* against a deterministic
policy before any credential is used, binds it to the human instruction,
requires human approval for sensitive actions, and writes a signed, hash-chained
audit trail.

This specification exists so that independent **authorizers**, **brokers**, and
**auditors** — written by different people, in different languages — agree
byte-for-byte.

## Read the spec

📜 **[spec.md](spec.md)** — the normative protocol.

- [Canonicalization](spec.md#3-canonicalization-normative)
- [Proposed Action & hashing](spec.md#4-proposed-action)
- [Policy & decisions](spec.md#5-policy)
- [Approval binding — the confused-deputy guard](spec.md#7-approval-binding-the-confused-deputy-guard)
- [Receipt & audit chain](spec.md#8-receipt--audit-chain-normative)
- [Authorization Token](spec.md#9-authorization-token-normative)

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

**v0.3 — draft.** The spec/protocol is versioned `0.x` (the reference *package*
is `0.x.y`). 0.1–0.2 are reference-backed; 0.3 (query-string fingerprint §4.2,
authorization token §9) is specified but not yet in the reference. See the
[§2.1 version matrix](spec.md#21-protocol-versions). A breaking change to the
receipt fields bumps the version (see [§8.2](spec.md#82-schema-versioning)).

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)**. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md). Propose changes by opening an issue or a
pull request; a change to a NORMATIVE section should come with updated
[CTK vectors](ctk/README.md).

## License

[Apache License 2.0](LICENSE).
