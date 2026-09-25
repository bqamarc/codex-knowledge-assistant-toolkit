# Answer routing and rendering

Read this reference when implementing question interpretation, retrieval routing, provider checks, citations, or final Webex output.

## Preserve the question contract

Resolve the smallest useful contract before retrieval:

- named product, feature, standard, or other subject;
- question type such as what, why, how, where, comparison, support, limitation, or troubleshooting;
- direction when data or actions move between systems;
- requested facets such as value, prerequisites, configuration, limits, or source location; and
- supplied version, region, deployment, audience, or date qualifier.

Decompose a bounded compound question, then answer every facet. Ask one focused clarification only when an unresolved term would materially change the answer.

## Route specific before general

Give an exact subject route first consideration. A broad overview is a fallback, not a competitor that may absorb a named subject through keyword overlap.

Carry subject and facets through query expansion, retrieval, ranking, composition, validation, and rendering. Acronyms may expand the query but cannot relax subject identity. Directional evidence for `A queries B` does not prove `A sends to B` or `B sends to A`.

Rank on subject coverage, facet coverage, audience eligibility, authority, freshness, and conflict state. Clarify or abstain when no candidate clears the gate.

## Bound provider reasoning

1. Check every requested facet and the named subject.
2. Map every material claim to eligible evidence.
3. Reject unrelated passages, copied restricted-audit wording, unsupported certainty, and fabricated links.
4. Permit one configured repair pass only when evidence supports it.
5. Clarify or abstain if validation still fails.

A provider's availability does not prove that a particular answer used it. Test and report actual invocation or fallback when that distinction matters.

## Select citations

Use concise canonical titles and audience-safe links. Keep chunk labels, extraction coordinates, raw interface text, and collection names out of the answer. Validate link scheme and host independently from retrieval rank, and ensure each source supports its nearby claim.

## Render for Webex

- Preserve short headings, paragraphs, lists, and numbered procedures with blank lines.
- Keep consistent bold labels in labeled lists.
- Convert wide tables into grouped bullets when needed.
- Deduplicate semantic blocks without removing list markers or headings.
- Keep punctuation cleanup aware of file extensions, hashes, commands, URLs, and identifiers.
- Truncate only at a complete section or list-item boundary, keeping the direct answer first.

Test the exact Markdown sent to Webex, not only an intermediate draft.
