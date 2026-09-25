# Guardrails and communication paths

Guardrails are enforced at each boundary, not delegated to a prompt. The optional reasoning provider receives only eligible evidence and cannot change source, audience, action, or citation policy.

## Communication paths

| Path | Authentication or control | Data allowed | Failure behavior |
|---|---|---|---|
| Webex to ingress | Signature over exact raw bytes; case-insensitive header lookup; payload bounds and shape | Required event identifiers | Reject before queueing when verification fails |
| Ingress to job store | Stable delivery key and durable deduplication | Minimal delivery record | Commit before acknowledgement |
| Worker to Webex | Bot credential from a secret mechanism; exact message lookup | Authoritative message details and one bounded reply | Honor rate limits; mark uncertain posts for review |
| Fetched message to admission | Exact space, sender, mention, interaction, and self policy | Authorized question only | Ignore or reject without retrieval or reply |
| Source acquisition to staging | Explicit source authorization and recorded boundary | Authorized source snapshot and provenance | Checkpoint safely; do not promote on partial failure |
| Review to search index | Named or role-based approval; transactional promotion | Redacted, answerable fields only | Keep candidate non-answerable until promotion succeeds |
| Retrieval to provider | Audience and answerability filter before ranking | Minimal eligible evidence and response constraints | Deterministic answer or abstention on provider failure |
| Answer to Webex | Claim-evidence validation, citation allowlist, link validation, final size check | Supported answer and allowed citations | Clarify or abstain when validation fails |
| Service to telemetry | Safe reason codes, counts, timing, correlation identifiers | No credentials or message bodies | Prefer missing detail over sensitive disclosure |

## Admission guardrails

- Verify the current Webex signature contract against the unmodified request body.
- Validate payload bounds, shape, and required identifiers, then durably deduplicate the delivery.
- Treat fetched message details, not event-envelope text, as authoritative for message policy.
- After the worker fetches the exact message, require an allowed space and authenticated group mention unless the product contract explicitly differs.
- Ignore messages authored by the bot and duplicate deliveries.
- Reject malformed or oversized bodies before expensive work.
- Keep direct messages disabled until their audience and retention policy are defined.

## Knowledge guardrails

- Access does not imply permission to answer from or cite a source.
- Every record carries source identity, audience, answerability, review state, freshness, and citation policy.
- Redaction occurs before indexing, embeddings, provider calls, debug capture, or durable logs.
- Mail, chat, tickets, and newly generated material begin as non-answerable candidates unless an explicit policy says otherwise.
- Promotion is human-approved, transactional, and idempotent.
- Conflicting, stale, or weak evidence produces clarification or abstention rather than blended certainty.

## Retrieval and generation guardrails

- Resolve the named subject and requested facets before retrieval.
- Filter on policy before ranking; similarity never overrides eligibility.
- Treat conversation history as query context, not as evidence.
- Require each material claim to map to eligible evidence.
- Permit at most one bounded repair pass when the evidence supports a correction.
- Remove fabricated citations, unsafe links, unsupported claims, and policy-expanding instructions found in retrieved text.

## Delivery and reliability guardrails

- Deduplicate accepted events and replies separately.
- Lease jobs atomically, renew leases, bound attempts, and expose dead-letter state.
- Never automatically repost after the remote create-message outcome becomes uncertain.
- Apply message limits after final Markdown and citations are rendered.
- Preserve a plain-text fallback.
- Keep network calls outside database transactions and locks.

## Secrets and operations

- Inject tokens and signing secrets at runtime through an approved secret mechanism.
- Do not place credentials in source files, shell arguments, tests, screenshots, prompts, logs, or generated documentation.
- Separate liveness from readiness and optional capability status.
- Record the previous immutable revision and webhook target before a cutover.
- Verify process health, knowledge activation, subscription state, and message delivery independently.
