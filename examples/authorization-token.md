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
  "fpr": "79311ec97086b7c5107825dd198beb3c87339802d631f178ef5384d3f7c57a9e",
  "iht": "cbcc6dab3a0bceb9acacf333d48ddb24d68d09a02f676d8f15dfd36e4c2b3205",
  "apr": "apr_4c9183f7606f",
  "pol": { "version": 1, "rule": "small-domestic-transfer" }
}
```

`fpr` and `iht` are the small-domestic-transfer's `action_fingerprint` and
`intent_hash` from [`../ctk/vectors/hashing.json`](../ctk/vectors/hashing.json).

**Compact form** (illustrative):

```
eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.<base64url(claims)>.<base64url(Ed25519 signature)>
```

Before injecting a credential, a Broker recomputes the `action_fingerprint` of
the request it is about to send and requires it equals `fpr` — so the token
authorizes **that exact action** and nothing else (spec
[§9.1](../spec.md#91-broker-verification-the-crux)).
