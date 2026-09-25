# Architecture and delivery

Read this reference when choosing runtime shape, state, concurrency, repository structure, or deployment topology.

## Smallest honest architecture

A local proof may receive a synthetic event, retrieve from a reviewed fixture, and render a response in one process. Label it a development proof.

A hosted assistant normally separates fast admission from variable-latency answering:

```text
Webex webhook -> ingress -> durable job store -> worker
                                             -> governed retrieval
                                             -> optional provider
                                             -> Webex Messages API
```

Use one immutable application artifact for ingress, migrations, and worker roles when practical, with distinct commands and least-privilege configuration. Store durable state outside the application filesystem.

## Component contracts

### Ingress

- Keep exact raw bytes long enough to verify the signature.
- Reject malformed, oversized, or incomplete event envelopes before expensive work.
- Derive a stable delivery key from event or message identifiers; document any hash fallback.
- Commit the verified delivery and deduplication state before returning success.
- Do not call a provider or hold a database lock across network I/O.

### Worker

- Lease work atomically and renew long-running leases.
- Fetch the exact Webex message, then enforce space, sender, mention, interaction, and self policy from those authoritative details.
- Bound attempts and move exhausted work to a reviewable dead-letter state.
- Treat a lost lease during processing differently from a lost connection after posting begins.
- Require an explicit operator decision before requeueing an uncertain post.

### Knowledge and answering

- Separate source snapshots, normalized records, review state, and indexes.
- Retrieve only records eligible for the resolved audience.
- Treat conversation context as query context, never evidence.
- Give a provider only eligible evidence and explicit output constraints.
- Validate claims, citations, links, secrets, and length after provider output.

### Delivery

- Keep a plain-text fallback for Markdown or richer content.
- Apply the current Webex payload limit after final rendering.
- Prefer one useful reply; if splitting is required, define ordering and duplicate suppression.
- Log safe status and correlation metadata, not credentials or message bodies.

## Repository boundary

A new application normally needs clear homes for Webex admission, configuration and secrets, ingestion and review, retrieval and policy, provider adapters, rendering, durable jobs and migrations, health and operator commands, synthetic tests, deployment, security, and rollback documentation.

Do not store production source content, message exports, runtime databases, or logs in the repository. Version source manifests only when they contain sanitized, reviewable metadata.

## Configuration and readiness

Validate configuration by runtime role. A disabled optional integration should not require credentials.

Production preflight should fail closed without durable shared storage, current migrations, signed-webhook enforcement, exact audience authorization, injected secrets, a responsive worker, and owned HTTPS ingress.

Liveness means the process is running. Readiness means the role can safely accept or process work. Optional-provider availability is a separate capability state.

## Delivery milestones and rollback

Track separately: local validation, package build, commit publication, infrastructure readiness, secret provisioning, ingress readiness, source activation, Webex subscription reconciliation, authorized message verification, and monitoring.

Deploy immutable revisions. Record the previous revision and webhook target before cutover. Rollback restores both when they changed, without replaying uncertain deliveries.
