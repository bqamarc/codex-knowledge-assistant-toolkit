---
name: build-governed-webex-assistant
description: Design, implement, harden, test, or package a Webex bot that answers from a governed knowledge corpus. Use for webhook admission, durable processing, source review, retrieval, citations, abstention, delivery safety, and deployment readiness. Do not use for a one-time room export, a general Webex API lookup, or ordinary document editing.
---

# Build Governed Webex Assistant

## Outcome

Create or extend a Webex knowledge assistant that:

- accepts only authorized Webex events;
- answers from reviewed, attributable evidence;
- protects restricted material and credentials;
- cites allowed sources or abstains clearly;
- tolerates retries without duplicate replies; and
- has an honest path from local validation to an explicitly chosen deployment.

Report local code, a passing test gate, repository publication, infrastructure readiness, active knowledge, webhook state, and live delivery as separate states.

## Establish the contract

Resolve the decisions that materially change the design:

- audience and allowed interaction modes;
- exact spaces or reviewable enrollment policy;
- approved source classes, citation policy, freshness, and review ownership;
- retention, redaction, and conversation-context limits;
- local proof versus hosted availability;
- existing repository, stack, and deployment constraints; and
- authority to provision a bot, change a webhook, deploy, or rotate secrets.

Inspect an existing project before replacing its structure. Preserve uncommitted work and established tests unless the user requests a change. Local implementation and synthetic tests are reversible; live Webex, DNS, deployment, and secret operations require the exact authorized target.

## Design boundaries

Read [architecture and delivery](references/architecture-and-delivery.md) when selecting runtime components, state, concurrency, repository shape, or deployment topology.

Define six boundaries explicitly:

1. **Admission:** verify the webhook, validate payload bounds and shape, deduplicate and durably record the delivery, then enforce space, sender, mention, interaction, and self policy after fetching the authoritative message.
2. **Processing:** durably record accepted work when retries matter; keep network calls outside database locks.
3. **Knowledge:** acquire, normalize, redact, classify, review, index, retrieve, and cite evidence under deterministic policy.
4. **Answering:** use conversation only to interpret the question; constrain any provider to eligible evidence; validate claims, citations, links, and length.
5. **Delivery:** post one bounded response and distinguish retryable work from an uncertain remote post.
6. **Operations:** expose safe health, readiness, migrations, queue state, monitoring, rollback, and secret rotation.

Keep a reasoning provider behind an interface. It may classify or phrase an answer, but it cannot widen source, audience, action, or citation policy.

## Govern knowledge and retrieval

Read [knowledge governance](references/knowledge-governance.md) before importing, indexing, retrieving, or citing sources. Read [answer routing and rendering](references/answer-routing-and-rendering.md) when implementing question interpretation, route selection, provider validation, citations, or final Webex formatting.

At minimum:

- give every record stable provenance, authority, audience, freshness, answerability, review state, and citation policy;
- redact before indexing, embedding, provider submission, or durable logs;
- keep unreviewed and restricted-audit material non-answerable;
- require recorded human approval before promoting a candidate;
- preserve version, regional, entitlement, and date differences rather than blending them;
- keep the named subject, direction, and requested facets through retrieval and composition; and
- clarify or abstain when eligible evidence is missing, weak, stale, or conflicting.

Do not infer an integration from related terminology alone. A strong integration claim needs named entities, direction, scope, and a functioning mechanism such as an API, connector, data flow, or service contract.

## Implement Webex safely

Read [Webex security and operations](references/webex-security-and-operations.md) before authentication, webhook admission, message delivery, subscription changes, or a live test.

Production defaults:

- signature verification over unmodified request bytes before parsing;
- durable delivery deduplication before acknowledgement;
- authoritative message lookup before exact space, sender, mention, interaction, and self policy;
- authenticated mentions in group spaces unless the product contract differs;
- fail-closed behavior when the signing secret or required policy is absent;
- acknowledgement only after the verified delivery is durably committed;
- bounded retries that honor `Retry-After`;
- no automatic repost when a create-message outcome is uncertain; and
- runtime-injected credentials that never enter source, fixtures, prompts, logs, or generated docs.

An unsigned receiver, in-memory queue, local database file, temporary tunnel, or combined process may support an explicit development proof. Do not present it as a hosted production control.

## Verify observable behavior

Read [acceptance testing](references/acceptance-testing.md) while defining tests and before claiming readiness. Use synthetic fixtures and mocked network calls.

The local gate should cover:

- valid, invalid, malformed, unauthorized, self-authored, and duplicate events;
- answerable, candidate, restricted-audit, stale, and conflicting evidence;
- redaction before indexing and provider calls;
- exact subject and facet routing, including near misses;
- claim-to-source alignment, allowed citations, and abstention;
- provider failure and unsafe provider output;
- final Markdown structure and payload limits;
- queue leases, bounded retries, dead letters, rate limits, and uncertain posts; and
- production configuration, migrations, readiness, shutdown, and rollback.

Use an authorized dedicated test bot and exact test space for any live smoke test. Record only safe metadata.

## Deliver and report

Keep application code, runtime tests, source packages, and deployment configuration in the application repository. Keep this skill limited to reusable methods and synthetic examples. Never copy credentials, tenant data, source records, logs, databases, runtime state, message exports, or project-specific identifiers into a reusable skill.

Report what changed, exact validation outcomes, external mutations, remaining provisioning, rollback for live changes, and every intentionally unverified state.

Reusable methods may enter this skill only when the user explicitly requests a skill update and the method remains valid across projects. Project decisions stay in project documentation. Raw operational evidence and identifiers have no durable memory destination.
