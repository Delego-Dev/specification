# Security Policy

This repository is the **specification** for delego — a deterministic
authorization & audit protocol for AI-agent actions. The security-relevant
artifact here is the *protocol itself*: a normative clause that permits an action
it should forbid is a vulnerability, even when an implementation follows it
faithfully.

## Reporting a vulnerability

**Please do not open a public issue for security vulnerabilities.**

Report privately via GitHub's
[private vulnerability reporting](https://github.com/Delego-Dev/specification/security/advisories/new),
or email **koishore@gmail.com**. Include the affected section of [`spec.md`](spec.md)
(or the conformance vector), why it weakens a guarantee, and a concrete scenario.
We aim to acknowledge within 72 hours.

## In scope

Weaknesses in the protocol as specified, for example:

- A normative rule whose plain reading authorizes an action the model should
  deny — e.g. a gap in the **forbidden → rules → default** order, or a
  fail-open constraint.
- A way for an approval bound to one action to release a *different* action — a
  break in the confused-deputy / action-fingerprint binding as specified.
- An audit-chain construction the spec mandates that does **not** detect a class
  of tampering it claims to (beyond the documented tail-truncation limit).
- A conformance vector in [`ctk/`](ctk/) that is wrong or contradicts the prose.

## Out of scope

- Bugs in a particular *implementation* — report those against that project
  (e.g. the reference implementation,
  [delego](https://github.com/Delego-Dev/delego/security)).
- Documented design boundaries (see the threat-model section of the spec); a
  bypass *within* those boundaries is in scope.

## Supported versions

The spec is pre-1.0 and versioned in tiers (0.1 / 0.2 / 0.3-draft). Security
corrections target the latest published tier.
