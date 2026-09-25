# Contributing

Contributions are accepted under the repository's [Apache License 2.0](LICENSE). Keep them narrowly reusable:

- use synthetic examples and placeholder identifiers;
- keep organization-specific policy, knowledge, endpoints, and deployment state out of the toolkit;
- never add tokens, secrets, real message bodies, people, customer details, or production URLs;
- add a negative test for every new safety rule;
- preserve abstention when eligible evidence is missing; and
- run the complete local gate before opening a change.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_public_release.py . --require-license
```

Documentation changes must keep all local Markdown links valid. Skill changes must preserve a discriminating frontmatter description, referenced-file routing, and safe behavior for unknown live targets.
