# Contributing to the delego specification

Thanks for helping shape the delego protocol. This repository is the source of
truth for the wire format; the reference implementation lives at
[Delego-Dev/delego](https://github.com/Delego-Dev/delego).

## How to propose a change

1. **Open an issue** describing the problem or gap before a large change.
2. For wording, examples, or clarifications, open a pull request directly.
3. A change to a **NORMATIVE** section (canonicalization, hashing, policy
   evaluation, the receipt/audit chain, or the authorization token) MUST:
   - keep the spec consistent with the [Conformance Test Kit](ctk/README.md), and
   - update or add CTK vectors, regenerated from the reference implementation, so
     the prose and the vectors never drift.
4. Keep `validate.py` green — examples and vectors must validate against the
   [schemas](schema/). CI runs it on every push and PR.

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
