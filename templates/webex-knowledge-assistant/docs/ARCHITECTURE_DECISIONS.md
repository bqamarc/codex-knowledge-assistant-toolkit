# Architecture decisions

Complete these decisions before treating the application design as stable.

## Product contract

- Intended users:
- Allowed group spaces or enrollment policy:
- Direct-message policy:
- Mention policy:
- Answer length and interaction behavior:
- Availability objective:

## Knowledge contract

- Approved source owners:
- Answerable source classes:
- Citation rules:
- Review and promotion owner:
- Freshness and expiry rules:
- Redaction rules:
- Retention and deletion rules:

## Runtime contract

- Ingress host and ownership:
- Durable database and job store:
- Search approach:
- Optional provider and allowed endpoint policy:
- Secret mechanism:
- Worker concurrency and retry bounds:
- Health, readiness, monitoring, and alerting:
- Deployment revision and rollback method:

## Trust-boundary checklist

- [ ] Signature verification uses exact raw bytes.
- [ ] Space authorization is exact and reviewable.
- [ ] Accepted work is durable before acknowledgement.
- [ ] Redaction happens before indexing and provider submission.
- [ ] Source eligibility is applied before ranking.
- [ ] Provider output is revalidated against claim-evidence pairs.
- [ ] Reply idempotency is separate from event deduplication.
- [ ] An uncertain post cannot be automatically repeated.
- [ ] Logs and health responses expose only safe metadata.
- [ ] Production preflight fails closed.
