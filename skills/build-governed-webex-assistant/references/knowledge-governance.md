# Knowledge governance

Read this reference before importing, indexing, retrieving, or citing knowledge.

## Source classes

| Class | Intended use | Answerable | Citable |
|---|---|---:|---:|
| official-current | Controlled publication or authoritative documentation | Yes | Yes |
| approved | Reviewed guidance for its defined audience | Policy-dependent | Policy-dependent |
| restricted-audit | Aggregate intent and gap signals only | No | No |
| candidate | New extraction or generated material awaiting review | No | No |
| synthetic | Tests and demonstrations | Test only | Test only |

Access does not make a source answerable. Audience, purpose, ownership, retention, answerability, and citation permission are separate decisions.

## Required metadata

Retain enough metadata to explain eligibility:

- stable source and record identifiers;
- title and canonical location when shareable;
- source class, audience, citation mode, owner, and approving role;
- captured, published, reviewed, and expiry dates when applicable;
- checksum or immutable revision;
- answerable and review-required state;
- extraction method and parser version when relevant; and
- supersession and conflict links.

Keep sensitive provenance in a separately controlled field when its title or location would reveal restricted context.

## Ingestion pipeline

1. Acquire only authorized inputs and record the boundary.
2. Preserve a checksum-addressed snapshot when policy allows.
3. Extract structure and provenance before chunking.
4. Redact secrets, personal data, customer identifiers, and prohibited context.
5. Classify audience, answerability, citation mode, freshness, and review state.
6. Stage chat- or model-derived content as non-answerable candidates.
7. Require recorded human approval before promotion.
8. Promote transactionally and idempotently.
9. Index only sanitized fields allowed for retrieval or provider use.
10. Supersede old versions and rebuild or retire derived records when a source expires or changes.

Redact before embeddings, provider submission, debug capture, or durable logs. An embedding is still derived data and follows the same policy.

## Retrieval and conflict handling

- Filter by audience and answerability before ranking.
- Prefer authoritative current sources over repeated social claims.
- Keep distinct claims separate when they differ by product, version, region, entitlement, or date.
- Define a strong-match threshold and an ambiguity path.
- Recheck drift-prone facts at the authoritative source when current accuracy matters.
- Do not let conversation context, model memory, or restricted-audit material fill an evidence gap.

Insufficient evidence produces a scoped abstention that says what is missing and, when safe, how to verify it.

## Answer and citation boundary

Build from eligible claim-evidence pairs, then independently validate citations and links for the resolved audience.

Restricted-audit material may contribute aggregate question themes when policy allows, but cannot provide answer text, citations, author identities, quoted wording, customer context, or collection names.

An optional provider may improve classification or phrasing. It cannot promote a source, invent a citation, replace evidence with model knowledge, convert a plan into a commitment, broaden an audience, or override a required abstention.

## Retention and deletion

Define retention separately for snapshots, normalized records, embeddings, context, delivery state, and metrics. Deletion covers derived indexes and caches, not only the visible record.

Bound conversation context by age and turn count. Store only what reference resolution requires, and never promote conversation history silently into durable knowledge.
