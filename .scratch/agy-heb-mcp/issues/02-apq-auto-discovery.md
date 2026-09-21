# 02: Integrate Apollo Persisted Query (APQ) Hash Auto-Discovery (PR #21)

**What to build:** Integrate upstream PR #21 (by @spunkedy) to provide automatic discovery and renewal of Apollo Persisted Query (APQ) SHA-256 hashes. When H-E-B deploys new frontend code and operations fail with `PersistedQueryNotFound`, the `PersistedQueryManager` scans H-E-B's live JavaScript bundles, extracts the latest hashes, caches them to disk, and retries the GraphQL operation transparently.

**Blocked by:** 01: Fix Windows Platform Compatibility & Permission Guards
**Status:** ready-for-agent
**GitHub Issue:** https://github.com/samasastudio/agy-heb-mcp/issues/3

- [ ] Incorporate `PersistedQueryManager` in `clients/persisted_queries.py`
- [ ] Connect APQ auto-discovery and retry handling into `clients/graphql.py`
- [ ] Cache discovered hashes to disk with TTL to prevent repeated discovery overhead
- [ ] Incorporate multi-step React login selectors from PR #21 in `auth/browser_refresh.py`
- [ ] Pass all 18 APQ unit tests in `tests/unit/test_persisted_queries.py`
