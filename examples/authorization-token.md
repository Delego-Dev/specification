# Authorization Token — example

> **Illustrative.** The authorization token (spec [§9](../spec.md#9-authorization-token-normative))
> is the v0.3 protocol increment and is **not yet minted by the reference
> implementation**. The compact form below uses a placeholder signature.

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
  "fpr": "c70d4ee57957202087887cb5e9d32222977b728bd06947b7761c283b6d4ed394",
  "iht": "76f8eef1b97e1213a59eec28cedf15bb999fdb00a3fd17f8343bc4676fdbb4f3",
  "apr": "apr_4c9183f7606f",
  "pol": { "version": 1, "rule": "place-order" }
}
```

`fpr` and `iht` are the place-order's `action_fingerprint` and
`intent_hash` from [`../ctk/vectors/hashing.json`](../ctk/vectors/hashing.json).

**Compact form** (illustrative):

```
eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.<base64url(claims)>.<base64url(Ed25519 signature)>
```

Before injecting a credential, a Broker recomputes the `action_fingerprint` of
the request it is about to send and requires it equals `fpr` — so the token
authorizes **that exact action** and nothing else (spec
[§9.1](../spec.md#91-broker-verification-the-crux)).
