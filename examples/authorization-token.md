# Authorization Token — example

> **Illustrative.** The authorization token (spec [§9](../spec.md#9-authorization-token-optional-profile-03--reference-backed-since-delego-033))
> is an **optional 0.3 profile** for carrying a PDP→PEP decision across a process
> or network boundary; it is **not** the protocol's load-bearing control. The
> reference mints and verifies it since **delego 0.3.3** (see
> [`../ctk/vectors/token.json`](../ctk/vectors/token.json) for signed verifier
> vectors). The compact form below uses a placeholder signature.

A delego authorization token is a compact **JWS / JWT** (`header.payload.signature`,
each segment base64url-encoded) signed with `alg = EdDSA` (Ed25519).

**Header**

```json
{ "alg": "EdDSA", "typ": "JWT" }
```

**Claims** — the decoded payload, in [`authorization-token.json`](authorization-token.json):

```json
{
  "iss": "delego:local",
  "aud": "broker:onecli",
  "iat": 1759000000,
  "exp": 1759000045,
  "jti": "01JBQK9Z6X8N3M2P0R5T7V9W1Y",
  "cns": "01JBQK9Z6X8N3M2P0R5T7V9W2Z",
  "fpr": "4327df2637072bf058622d1f8baea6e431726f7332a50cd12ec970d6e43c2fd2",
  "iht": "76f8eef1b97e1213a59eec28cedf15bb999fdb00a3fd17f8343bc4676fdbb4f3",
  "apr": "apr_4c9183f7606f",
  "sub": "agent:onecli/session-7f3a",
  "pol": { "version": 1, "rule": "place-order" }
}
```

`fpr` and `iht` are the place-order's `action_fingerprint` and
`intent_hash` from [`../ctk/vectors/hashing.json`](../ctk/vectors/hashing.json).
`cns` is the **consumption nonce**: it binds this token to a single credential
release, so the token inherits the single-use property of the authorization it
carries (spec §7.1 P3, §9). `sub` is the OPTIONAL agent/session identity, present
when the token composes with an agent-identity layer (§9.3).

**Compact form** (illustrative):

```
eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.<base64url(claims)>.<base64url(Ed25519 signature)>
```

Before injecting a credential, a Broker verifies the signature, requires `aud` to
match its own identifier **exactly**, checks `exp` is in the future, refuses a
previously-seen `jti` and a previously-consumed `cns`, and recomputes the
`action_fingerprint` of the request it is about to send, requiring it equals
`fpr` — so the token authorizes **that exact action**, **once**, and nothing else
(spec [§9.1](../spec.md#91-broker-verification-the-crux)).
