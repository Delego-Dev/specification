# Contributing to the delego specification

Thanks for helping shape the delego protocol. This repository is the source of
truth for the wire format; the reference implementation lives at
[Delego-Dev/delego](https://github.com/Delego-Dev/delego).

## How to propose a change

1. **Fork the repository** and work on a branch in your fork. Open a pull request
   from the fork; direct pushes to this repo are not accepted.
2. **Open an issue** describing the problem or gap before a large change.
3. For wording, examples, or clarifications, open a pull request directly.
4. A change to a **NORMATIVE** section (canonicalization, hashing, policy
   evaluation, the receipt/audit chain, or the authorization token) MUST:
   - keep the spec consistent with the [Conformance Test Kit](ctk/README.md), and
   - update or add CTK vectors, regenerated from the reference implementation, so
     the prose and the vectors never drift.
5. Keep `validate.py` **and** `conformance.py` green — examples/vectors must
   validate against the [schemas](schema/), and the reference must reproduce
   every CTK vector. CI runs both on every push and PR.
6. Fill in the pull-request template completely, including the AI-assistance
   disclosure (see below).

## The spec leads the reference

This is the source of truth: **normative behaviour is specified here first**, then
implemented. A new behaviour lands in the spec marked *draft — not yet in
reference* (see the §2.1 version matrix), and becomes reference-backed only once
the implementation reproduces its CTK vectors. The reference's
`__protocol_version__` MUST always be ≤ this document's version; `conformance.py`
enforces it. Do not document behaviour here to *match* code that already shipped
ahead of the spec — that is the failure mode this rule exists to prevent.

## AI-assisted contributions

AI coding assistants are welcome tools, but AI-generated or AI-assisted
contributions to a security protocol carry extra risk, so:

- **Disclose it.** The PR template has a required field for whether and how AI was
  used. Be honest and specific.
- **Expect stricter review.** AI-assisted PRs — especially ones touching NORMATIVE
  sections, the threat model, or the CTK — receive closer scrutiny and may take
  longer to merge. Unreviewed, bulk-generated PRs will be closed.
- **You are accountable.** The human author is responsible for every line: its
  correctness, that the CTK vectors were regenerated (not hand-edited to pass),
  and that no invariant or security property was weakened. "The model wrote it"
  is not a defence.
- **Process is the same — fork, template, green CI.** No fast path for AI output.

## Versioning

The wire format is versioned with the spec. A breaking change to the receipt
fields or the canonicalization rules MUST bump the spec version and the relevant
schema together (see [spec §8.2](spec.md#82-schema-versioning)); otherwise
previously-signed audit chains stop verifying.

## Scope

This repository covers the **open protocol** only: the action model, policy
schema, decision semantics, the signed audit chain, and the authorization token.
Implementation-specific details belong in the implementations that adopt the
spec.

## Code of Conduct

By participating you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
