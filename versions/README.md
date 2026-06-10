# Protocol version documents

The **current specification is [`../spec.md`](../spec.md) (v0.3, frozen)** — it
is the only document that defines new behaviour. This directory holds a
standalone document per *prior* protocol version, so an implementation that
declares 0.1 or 0.2 (see [§2.1](../spec.md#21-protocol-versions) and
`delego.__protocol_version__`) has a spec of record without filtering version
tags by hand.

| Document | Protocol | Status |
|----------|----------|--------|
| [`spec-v0.1.md`](spec-v0.1.md) | 0.1 | superseded — initial protocol; approvals fingerprint-bound only (not intent-bound, not single-use) |
| [`spec-v0.2.md`](spec-v0.2.md) | 0.2 | superseded — what the reference (`delego` 0.2.x) implements today |
| [`../spec.md`](../spec.md) | 0.3 | **current, frozen** |

**How these were produced.** Backfilled retroactively from the frozen v0.3
document by removing every clause tagged above the target version (`(since
0.2)`, `(0.3, draft …)`), keeping section numbering aligned (later-version
sections are stubbed with a pointer). They use the current canonical
terminology and carry corrected claims (e.g. the §8.1 truncation caveat), so
they are *not* byte-for-byte historical texts — the original drafts are in this
repository's git history.

**Rules:**
- These documents are **descriptive snapshots**: a change in protocol behaviour
  is never made here, only in `spec.md` (via a version bump, per §8.2/§2.1).
- Editorial fixes (typos, broken links) are fine; normative content is not.
