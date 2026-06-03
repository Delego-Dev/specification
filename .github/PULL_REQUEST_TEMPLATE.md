<!-- Fork the repo and open this PR from a branch in your fork. See CONTRIBUTING.md. -->

## What & why

<!-- What does this change to the protocol do, and why? Link any issue. -->

## AI assistance disclosure (required)

<!-- AI-assisted PRs are welcome but get stricter review. Be specific. -->

- [ ] No AI assistance.
- [ ] AI-assisted. Tool(s) and how used: ______
- [ ] AI-generated, human-reviewed. I have read every line and am accountable for it.

## Kind of change

- [ ] Editorial only (wording, examples, links) — no normative change.
- [ ] **Normative** change (canonicalization, hashing, policy/decision, audit
  chain, approval binding, or the authorization token).

## Checklist

- [ ] Forked the repo; this PR comes from a branch in my fork.
- [ ] `python validate.py` is green (examples/vectors validate against the schemas).
- [ ] `python conformance.py` is green (the reference reproduces every CTK vector).

## For a normative change (additionally)

- [ ] Updated or added **CTK vectors, regenerated from the reference** (not hand-edited).
- [ ] Updated the **§2.1 version matrix** and tagged new clauses *(since 0.x)* or
  *(0.x, draft — not yet in reference)*.
- [ ] The spec **leads** the reference: new behaviour is specified before/independent
  of code shipping it; the reference's `__protocol_version__` stays ≤ this spec's version.
- [ ] If the receipt fields or canonicalization changed: bumped the spec version
  and the schema version together (§8.2), and updated `CHANGELOG.md`.
