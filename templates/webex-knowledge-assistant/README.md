# Webex Knowledge Assistant Project Template

This directory is a planning scaffold for a new application. It does not contain a runnable bot or deployment.

## Start here

1. Record project decisions in [Architecture decisions](docs/ARCHITECTURE_DECISIONS.md).
2. Tailor [the example knowledge policy](config/knowledge-policy.example.json).
3. Replace [synthetic records](examples/sample-records.json) with an authorized acquisition and review pipeline; do not commit production content.
4. Turn [the acceptance matrix](tests/acceptance-matrix.md) into executable behavioral tests.
5. Implement ingress, durable processing, retrieval policy, delivery idempotency, migrations, readiness, rollback, and operational documentation.

Use [`.env.example`](.env.example) only as a list of variable names. Real credentials belong in the chosen hosting secret mechanism.

The full reference architecture is in the toolkit's [architecture guide](../../docs/ARCHITECTURE.md).
