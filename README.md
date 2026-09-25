# Codex Knowledge Assistant Toolkit

This repository is a public toolkit for designing governed Webex knowledge assistants with Codex. It contains one reusable skill, a small project-planning template, architecture diagrams, and deterministic release checks. It contains no application deployment, customer data, conversation exports, credentials, production identifiers, or environment-specific provider adapters.

The repository begins with a reviewed, fresh Git history and contains no imported private commits, branches, tags, or objects. It is licensed under the [Apache License 2.0](LICENSE).

## What is included

- `skills/build-governed-webex-assistant/`: reusable Codex guidance for architecture, knowledge policy, Webex admission, delivery safety, and acceptance testing.
- `templates/webex-knowledge-assistant/`: generic planning files and synthetic examples for a new application.
- `docs/ARCHITECTURE.md`: context, runtime, retrieval, and trust-boundary diagrams.
- `docs/GUARDRAILS.md`: policy and communication-path guardrails.
- `scripts/verify_public_release.py`: deterministic checks for URL and email boundaries, credential-like values, unsafe artifacts, malformed examples, broken local Markdown links, skill metadata, and an optional reviewer-supplied denylist.

## Quick validation

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_public_release.py . --require-license
python3 scripts/verify_public_release.py . --require-license --denylist-file "$RELEASE_DENYLIST"
```

The first two commands are the portable local gate and use only the Python standard library. The third command is an additional review gate when an authorized release reviewer supplies an untracked denylist outside the repository.

## How to use the skill

Copy `skills/build-governed-webex-assistant` into a Codex skills directory, then ask Codex to use `$build-governed-webex-assistant` for a new or materially changed Webex knowledge-assistant application. The skill deliberately does not activate for one-time room exports or ordinary API lookups.

## Release boundary

This is an original, generalized toolkit. Application code, runtime configuration, operational evidence, production knowledge, bot identities, room identifiers, organization-specific adapters, and history copied from another project belong outside this repository.

For every release:

1. Preserve the Apache-2.0 license and any required notices.
2. Run the validation commands above from a clean checkout.
3. Review every file and generated archive.
4. Verify the exact remote revision and release tag.
5. Keep application repositories and their histories separate from this toolkit.

See [Publication checklist](docs/PUBLICATION_CHECKLIST.md) for the full gate.

## Documentation map

- [Architecture](docs/ARCHITECTURE.md)
- [Guardrails](docs/GUARDRAILS.md)
- [Release decisions](docs/RELEASE_DECISIONS.md)
- [Publication checklist](docs/PUBLICATION_CHECKLIST.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)
- [Apache License 2.0](LICENSE)
