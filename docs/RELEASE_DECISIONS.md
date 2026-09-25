# Release decisions

This file records the governance decisions for the initial public release. Remote Git state remains the authoritative publication record.

## Problem and success criterion

The useful methods for building a governed Webex knowledge assistant need a reusable home that does not carry application code, environment state, organization-specific language, production identifiers, or another repository's history.

Success means the repository contains only generalized guidance, synthetic examples, and deterministic validation; all tests and release checks pass; repository history begins with the reviewed public tree rather than imported objects or references; and the Apache-2.0 license gate remains mandatory.

## Trigger boundary

- Positive: “Build a Webex bot that answers from reviewed documents and cites its sources.”
- Near miss: “Export the last month of messages from this Webex room.”

The positive request should invoke the skill. The near miss should use a bounded room-export workflow and must not scaffold an assistant.

## Dependencies and overlap

The skill depends on Codex's skill format and current official Webex API contracts. It does not depend on an application repository, knowledge base, local profile, model provider, deployment platform, or live Webex credential.

The application owns its code, source packages, runtime tests, configuration, migrations, deployment, and operational evidence. This toolkit owns only reusable design and validation methods.

## Risk and validation

Classification: **sensitive**, because a later publication error could disclose material that does not belong in a public repository.

Required checks include positive validation and safe-failure tests for an external denylist, non-example email addresses, credential-like assignments, broken links, permissive candidate policy, runtime artifacts, and a missing publication license. Repository history and generated archives require separate review before publication.

## Learning path

Reusable, generalized methods live in the skill references only after a requested review. Project decisions stay in project documentation. Raw operational evidence, source material, identifiers, and credentials have no destination in this toolkit.

Zero eligible search results are a successful policy outcome and produce a scoped abstention. Recovery is bounded to authorized acquisition, review, or a focused clarification; it does not widen source eligibility.

## Semantic precision

An ambiguous shared term is not enough to merge concepts. A strong integration claim requires named entities, direction, scope, and a working mechanism such as an API, connector, data flow, or service contract. Tests should keep keyword overlap from promoting a different subject.

## Distribution and local state

Selected publication destination: a GitHub.com repository named `codex-knowledge-assistant-toolkit`. The initial repository starts with the reviewed public tree, uses the Apache License 2.0, and must not import another project's objects, branches, or tags. The initial skill release tag is `skill-build-governed-webex-assistant-v0.1.0`.

The skill reads no local knowledge base, profile, index, or schema, so a local-state compatibility file is not applicable.

Every release still requires a clean-checkout review, the complete validation gate, and verification that the exact local commit and tag match the public remote.
