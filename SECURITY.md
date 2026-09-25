# Security

## Reporting a vulnerability

Report vulnerabilities through the repository's GitHub private vulnerability-reporting channel. Do not include credentials, tokens, message contents, customer information, or exploit data in a public issue.

## Security model

The toolkit treats these as separate trust boundaries:

- webhook admission;
- authorization for spaces and interaction modes;
- knowledge eligibility and audience policy;
- optional reasoning providers;
- outbound citations and links;
- durable queue state and reply idempotency; and
- deployment secrets and operational logs.

The template is planning material, not a secure deployment by itself. A real application must validate its Webex contract, hosting model, storage, secret mechanism, monitoring, rollback, and retention policy.
