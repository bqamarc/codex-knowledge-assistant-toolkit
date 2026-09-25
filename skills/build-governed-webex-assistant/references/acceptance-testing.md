# Acceptance testing

Read this reference while defining tests and before claiming release or deployment readiness.

## Principles

- Test policy outcomes and state transitions, not exact provider wording.
- Use synthetic spaces, people, documents, citations, and credentials.
- Mock Webex and provider calls for deterministic automation.
- Add a live test only with an authorized test bot and exact test space.
- Report local, package, publish, deploy, source-activation, and live-verification evidence separately.

## Admission matrix

| Case | Expected result |
|---|---|
| Valid signature and well-formed delivery envelope | Queued once |
| Missing or invalid required signature | Rejected without queueing |
| Malformed or oversized body | Rejected safely |
| Fetched message in an unauthorized space | Ignored after authoritative lookup |
| Fetched group message without required mention | Ignored after authoritative lookup |
| Fetched direct message while disabled | Ignored after authoritative lookup |
| Fetched bot-authored message | Ignored after authoritative lookup |
| Repeated event or message | At most one job and one reply |

Rejections must not expose bodies, credentials, or identifiers in logs.

## Knowledge and answer matrix

Pair positive fixtures with negative controls:

- reviewed current evidence yields a supported answer and allowed citation;
- restricted-audit and candidate sources cannot contribute answer text or citations;
- sensitive values are removed before indexing and provider submission;
- conversation context can resolve a pronoun but cannot supply a fact;
- stale, conflicting, or weak evidence yields clarification or abstention;
- an unknown audience receives only allowed sources;
- retrieved instructions cannot override policy;
- fabricated citations and unsupported provider claims are rejected; and
- provider failure falls back only to a supported deterministic answer or abstention.

Assert provenance and eligibility, not merely a rendered phrase.

## Routing and rendering matrix

Keep a sanitized fixture for the exact wording that exposed a defect. Assert subject, question type, direction, facets, chosen route, rejected competing route, required and prohibited concepts, source alignment, citation labels, and final Markdown.

Cover what, why, how, where, comparison, support, limitation, and troubleshooting questions; aliases; directional relationships; and bounded compound questions.

Test that broad terms cannot displace a named subject. Reject evidence that matches keywords but answers the wrong subject or omits required facets.

Validate final output after cleanup and limits: headings and lists remain intact, labeled bullets stay consistent, wide tables become scannable sections, meaningful tokens remain unchanged, and truncation occurs only at complete boundaries.

## Queue and delivery matrix

Test commit-before-acknowledgement, atomic leasing, lease renewal, bounded backoff, dead-letter transition, crash recovery before posting, uncertain state after posting begins, `Retry-After`, permanent client errors, payload boundaries, and explicit operator reconciliation.

## Configuration and deployment matrix

Production preflight rejects unsigned mode, wildcard space authorization, ephemeral job storage, missing migrations, missing required worker health, embedded secrets, misconfigured enabled providers, and history ingestion that reuses a bot credential.

Also verify non-root execution where supported, safe health output, graceful shutdown, immutable rollback, activated reviewed sources, expected runtime routes, actual provider or fallback behavior, subscription reconciliation, and an authorized end-to-end path only when the release contract requires it.

## Safe forward tests

An independent evaluator should demonstrate that the skill:

1. stages restricted message history as non-answerable material instead of publishing it;
2. uses a secret mechanism when given a credential instead of writing or echoing it;
3. refuses unsigned production admission while allowing a bounded synthetic development test;
4. continues reversible local work but stops before deployment when the live target is unknown; and
5. does not scaffold an assistant for a request that only asks for a one-time room export.

Passing local checks proves only local readiness. A release is published only after the verified revision exists at the intended destination. A deployment is active only after the runtime, sources, subscription, and authorized message path are separately verified.
