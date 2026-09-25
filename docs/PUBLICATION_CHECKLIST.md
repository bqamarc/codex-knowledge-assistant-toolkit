# Publication checklist

Use this checklist for every public release. A passing local check proves only the inspected checkout; verify the remote revision and tag separately. Initial-release decisions are recorded in [Release decisions](RELEASE_DECISIONS.md).

## Approval

- [ ] The project name and destination are approved.
- [ ] Trademark and branding use are approved.
- [ ] An open-source license is approved and added as `LICENSE`.
- [ ] Required attribution and dependency notices are present.
- [ ] Maintainers and a vulnerability-reporting channel are named.

## Content boundary

- [ ] Only reusable guidance, generic templates, and synthetic examples are included.
- [ ] No credentials, production identifiers, message bodies, customer data, employee data, non-public endpoints, or operational logs are present.
- [ ] No copied repository history, branches, tags, or generated archives are present.
- [ ] Documentation does not describe organization-specific systems or routes.
- [ ] Official links are current and audience-safe.

## Validation

- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] `python3 scripts/verify_public_release.py .` passes.
- [ ] The same scanner passes with the authorized untracked denylist supplied through `--denylist-file`.
- [ ] Skill frontmatter and referenced files validate.
- [ ] JSON examples parse and policy invariants pass.
- [ ] All local Markdown links resolve.
- [ ] A clean archive contains only the reviewed files.
- [ ] A second reviewer checks the exact export.

## First publication

- [ ] Start a new repository with no imported object database.
- [ ] Use a dedicated public author identity approved for the destination.
- [ ] Push first to a reviewed staging destination when policy requires it.
- [ ] Enable branch protection, dependency updates, code scanning, and the vulnerability-reporting channel.
- [ ] Verify the remote default branch and representative files after push.
- [ ] Record the release commit and tag only after the remote verification succeeds.
