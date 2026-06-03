# Changelog — delego wire specification

All notable changes to the protocol are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The specification is
versioned independently of the reference implementation and **leads** it: a
behaviour is specified (marked *draft — not yet in reference*) before the
reference implements it. See [`spec.md` §2.1](spec.md) for the version matrix.

## [0.3-draft] — Unreleased

### Fixed
- §8.1 corrected: hash-chaining does **not** detect truncation of the most recent
  receipts (a truncated prefix verifies clean), nor a holder of the local signing
  key. Added a normative caveat requiring external head anchoring for rollback
  detection — the prior "deleting any receipt breaks a check" claim was wrong.
- Version notation normalised to the `0.x` scheme everywhere (spec/protocol is
  `0.x`; the reference *package* is `0.x.y`). `conformance.py` now parses a
  two-component spec version.

### Added (0.3, draft — not yet in reference)
- §4.2 — the URL **query string** is folded into the `action_fingerprint`
  preimage, closing the confused-deputy gap where two requests differing only in
  their query share a fingerprint. A breaking change to the preimage; ships with
  updated `hashing` vectors when the reference implements it.
- §9 retagged as the 0.3 frontier (signed authorization token; unchanged content).

### Added (0.2, now reference-backed)
- §2.1 — a **Protocol versions** matrix (0.1 / 0.2 / 0.3) and the rule that the
  reference's `__protocol_version__` MUST be ≤ this document's version.
- §7 — approvals are bound to the `intent_hash` as well as the
  `action_fingerprint`, and are **single-use** (an approval releases its action
  at most once; a replayed release is denied). Full resolution algorithm and the
  approval status lifecycle (`pending → approved → consumed`, `denied`) specified.
- §5 / §8 — an approved action's `execution`/`allow` receipt carries the rule it
  was parked under, so `rate_limit` counts it; an unevaluable `rate_limit` denies.
- §8.1 — a malformed or partial receipt is a verification *failure*, not an error
  that aborts the walk.
- `ctk/vectors/resolve.json` — authoritative vectors for the §7 resolution rules
  (fingerprint guard, intent guard, single-use replay).
- `conformance.py` + a CI job that replays every CTK vector against the reference
  and asserts the spec leads it.

### Changed
- §6 — the determinism requirement now names *evaluation time* as an input
  (the `rate_limit` window), rather than implying a time-independent function.
- Document version → 0.3-draft.

## [0.1-draft] — initial specification

### Added
- §3 canonical JSON; §4 intent hash + action fingerprint; §5–§6 deterministic
  policy & decision; §7 fingerprint-bound approval (confused-deputy guard);
  §8 append-only, hash-linked, Ed25519-signed audit chain + verification;
  §9 authorization-token draft.
- JSON Schemas (`schema/`), CTK vectors (`ctk/`), and `validate.py`.

[0.3-draft]: https://github.com/Delego-Dev/specification
[0.1-draft]: https://github.com/Delego-Dev/specification/releases/tag/v0.1
