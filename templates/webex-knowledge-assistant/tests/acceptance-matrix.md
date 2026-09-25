# Acceptance matrix

Convert each row into an executable behavioral test using only synthetic fixtures and mocked network calls.

| Boundary | Positive case | Negative or failure case | Required assertion |
|---|---|---|---|
| Webhook signature | Valid signature over exact bytes | Missing, changed, or invalid signature | Invalid request creates no delivery job |
| Delivery envelope | Valid bounded shape and identifiers | Malformed, oversized, or incomplete envelope | Invalid request creates no delivery job |
| Fetched-message policy | Allowed space and required mention | Unknown space or missing mention | No retrieval or reply |
| Identity | User-authored fetched message | Bot-authored fetched message | No retrieval or reply |
| Deduplication | One event | Same event repeated | One accepted job |
| Source policy | Reviewed answerable record | Candidate or restricted-audit record | Only eligible evidence reaches composition |
| Redaction | Synthetic safe text | Fixture containing a synthetic secret marker | Marker never reaches index, provider, or logs |
| Retrieval | Exact subject and facet match | Keyword overlap with wrong subject | Wrong-subject passage is rejected |
| Conflict | Aligned current records | Two eligible records conflict | Clarification or abstention |
| Provider | Supported draft | Fabricated claim or citation | Unsafe draft is rejected or repaired once |
| Rendering | Short Markdown answer | Answer beyond configured limit | Complete blocks are retained; no partial token corruption |
| Rate limit | Successful post | `429` with `Retry-After` | Bounded delayed retry |
| Delivery certainty | Confirmed post | Connection loss after post begins | Job becomes uncertain; no automatic repost |
| Worker recovery | Lease completes | Worker stops before post begins | Expired lease is safely recoverable |
| Readiness | Current migrations and healthy worker | Missing migration or stale worker | Production readiness fails closed |
