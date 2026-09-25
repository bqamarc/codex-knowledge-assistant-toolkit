# Webex security and operations

Read this reference before implementing authentication, webhook admission, message delivery, subscription changes, or a live test.

## Recheck official contracts

API behavior can change. Verify the current contract in official Webex sources before implementation or release:

- [Bots](https://developer.webex.com/create/docs/bots)
- [Webhooks API](https://developer.webex.com/messaging/docs/api/v1/webhooks)
- [Messages API](https://developer.webex.com/messaging/docs/api/v1/messages)
- [Rate limiting](https://developer.webex.com/blog/rate-limiting-and-the-webex-api)

Do not copy tokens from examples. Confirm the correct Webex environment for the deployment.

## Identity and access

A bot token authenticates a bot. An integration acts for a consenting user. Choose the identity type from the product contract; do not use a user token merely to gain broader history access.

For a question-answering bot:

- inject the bot token through a secret mechanism;
- resolve and pin the bot person identity for self-event suppression;
- authorize exact spaces or a separately reviewed enrollment flow;
- keep direct messages disabled until audience and retention are defined; and
- remember that membership alone is not an authorization boundary.

Historical extraction is a separate read-only authorization path and must not reuse the production bot credential.

## Webhook admission

Use an owned HTTPS endpoint. Register a secret and verify Webex's signature over the exact raw request bytes before parsing or normalization. Header lookup must be case-insensitive and comparison constant-time.

Implement only the signature headers and algorithms supported by the current webhook contract. Keep compatibility behavior only when the deployment needs it.

Reject at ingress when the signature or secret is absent, verification fails, the payload is oversized or malformed, or required delivery identifiers are missing. Log a safe reason code and correlation identifier, never the rejected body.

Do not treat event-envelope text or sender fields as authoritative message content. After the worker fetches the exact message through the API, enforce space authorization, sender and self policy, interaction mode, and the required mention before retrieval or reply.

## Delivery semantics

Webhook events can be duplicated. Deduplicate before accepting work and maintain a separate idempotency boundary for replies.

Fetch the exact message details needed for authoritative admission. Strip mentions using Webex identity metadata rather than display-name guesses.

For outgoing messages:

- target the exact authorized space and thread relationship;
- render supported Markdown with a text fallback;
- enforce the current payload limit after rendering;
- validate citations and links;
- honor `429 Retry-After` with bounded retry; and
- treat a timeout after message creation begins as uncertain unless non-acceptance is proven.

Do not automatically repost an uncertain outcome. Surface it for reconciliation.

## Subscription lifecycle

Reconcile subscriptions by resource, event, filter, target URL, and ownership label. Avoid duplicates.

Before a live change, confirm bot identity and environment, prove ingress readiness, capture current owned subscription details for rollback, change only the intended subscription, verify the returned configuration, and run one authorized synthetic path when required.

Monitor subscription status and successful admission. Repair the receiver before re-enabling a subscription disabled after repeated failures.

## Secrets and logs

Do not put bot tokens, integration secrets, signing secrets, OAuth refresh tokens, provider credentials, raw bodies, or restricted source locations in source control, shell arguments, issues, tests, logs, traces, prompts, or generated skill files.

Use secret injection or mounted secret files. Rotate suspected exposures at the owning service; removing one file does not erase prior copies.
