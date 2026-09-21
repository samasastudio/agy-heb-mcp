# Spec: agy-heb-mcp - Antigravity Integration, APQ Auto-Discovery, Shopping Lists, and Windows Compatibility

## Problem Statement

Users attempting to automate H-E-B grocery orders in an Antigravity environment on Windows face multiple points of friction with the upstream codebase:
1. **Apollo Persisted Query (APQ) Rot**: Whenever H-E-B deploys frontend updates, hardcoded GraphQL hashes for cart additions and search operations rot (`PersistedQueryNotFound`), causing immediate failures.
2. **Akamai/Imperva Bot Interception**: The upstream tool relies on an isolated headless Playwright browser loop that is consistently blocked by H-E-B's bot detection (ErrorCode 15) and fails to maintain the short-lived 30-minute `sat` authentication JWT.
3. **Windows & Platform Incompatibilities**: The codebase assumes a POSIX environment, hardcoding `/tmp` paths for screenshots and enforcing octal `0o600` file permissions on NTFS, causing 6 test failures and broken error reporting on Windows.
4. **Missing Grocery Planning Surface**: Upstream lacks support for H-E-B's native shopping list features, forcing users to immediately add items to their active cart rather than curating lists over time.

## Solution

Transform the forked repository into `agy-heb-mcp`, a robust, Antigravity-native MCP server for H-E-B grocery automation:
1. **Incorporate APQ Auto-Discovery**: Merge upstream PR #21 to automatically scan live H-E-B JavaScript bundles at runtime when hashes expire, caching discovered hashes to disk and retrying GraphQL calls transparently.
2. **Add Native Shopping List Tools**: Merge upstream PR #13 to introduce full H-E-B shopping list capabilities (create, inspect, bulk add, and remove list items with human confirmation).
3. **Cross-Platform & Windows Hardening**: Replace POSIX path assumptions with system-appropriate temporary directories and guard file-permission assertions on Windows platforms.
4. **Antigravity Browser Session Bridge**: Provide a high-reliability session sync from Antigravity's persistent browser profile into the MCP storage state, eliminating headless bot blocks and providing accurate `sat` JWT expiry telemetry.
5. **Rebase Parity**: Keep grocery and GraphQL models architecturally decoupled from the session bridge so upstream changes remain easily mergeable.

## User Stories

1. As an Antigravity user, I want the MCP to automatically discover and update Apollo Persisted Query hashes when H-E-B deploys new frontend code, so that my cart and search tools never break due to stale hashes.
2. As an Antigravity user, I want discovered query hashes cached locally on disk with a TTL, so that repeated operations do not incur discovery latency on every server restart.
3. As a grocery shopper, I want to inspect and manage my H-E-B shopping lists via MCP tools, so that I can organize weekly grocery plans before transferring items to my cart.
4. As a grocery shopper, I want bulk-add tools for shopping lists with a single confirmation gate, so that I can add full recipe ingredient lists efficiently.
5. As a grocery shopper, I want destructive list operations (removing items or bulk adding) to require human-in-the-loop confirmation, so that accidental modifications are prevented.
6. As a grocery shopper, I want list tools to support targeted list names as well as an environment-configured default list, so that multiple lists can be organized independently.
7. As an Antigravity user on Windows, I want all unit and integration tests to pass cleanly without failing on POSIX file permission assertions, so that I have complete confidence in the codebase on Windows.
8. As an Antigravity user on Windows, I want screenshots and debug artifacts to be stored in the OS-standard temporary directory, so that login challenges do not trigger file not found errors.
9. As an Antigravity user, I want to authenticate against H-E-B using Antigravity's integrated browser, so that I can solve CAPTCHAs, Akamai challenges, and multi-step password forms naturally.
10. As an Antigravity user, I want my active browser session cookies (`sat`, `sst`, `JSESSIONID`) and `reese84` WAF tokens to sync directly into the MCP storage state, so that the MCP can make sub-second GraphQL requests without launching background browsers.
11. As an Antigravity user, I want `session_status` to evaluate the actual expiration time of the `sat` JWT token, so that I receive honest warnings before authentication expires rather than false positive health reports.
12. As an Antigravity user, I want search, cart, and coupon tools to execute directly against H-E-B's GraphQL API via `httpx`, so that grocery operations run in milliseconds rather than minutes.
13. As an Antigravity user, I want the MCP server registered globally in `~/.gemini/config/mcp_config.json`, so that it is instantly accessible to coding and planning agents across all workspace sessions.
14. As an Antigravity developer, I want all custom logic isolated to session, platform utility, and configuration modules, so that upstream changes from `texas-grocery-mcp` can be rebased cleanly without merge conflicts.

## Implementation Decisions

### Architectural Layering
- **Persisted Query Manager**: A dedicated APQ manager that intercepts `PersistedQueryNotFound` GraphQL responses, queries H-E-B's entrypoint HTML, extracts script asset URLs, parses 64-character SHA-256 hashes matching known operation signatures, caches valid hashes to disk, and replays the failed request with the discovered hash.
- **Shopping List Domain Module**: A dedicated tools module and GraphQL client extension supporting list querying, item addition with verification, batch addition, and item deletion. All destructive operations conform to the project's confirmation contract (`confirm=True`).
- **Cross-Platform File System Normalization**: The file utility module dynamically resolves temporary directories using standard cross-platform conventions. File permission enforcement (`0o600`) is conditionally applied only on non-Windows platforms where POSIX mode bits are supported by the operating system.
- **Session Bridge Contract**: Authentication state is stored in the standard Playwright storage state schema (`cookies` array and `origins` LocalStorage array containing `reese84`). Session validation checks the existence of `sat`, decodes its JWT expiration payload to confirm active lifespan, and validates that `reese84` has not passed its renew timestamp.
- **Package Identity**: The package configuration defines `agy-heb-mcp` as the package identity while maintaining internal module structure for upstream git compatibility.

## Testing Decisions

### Quality & Seam Philosophy
- Tests must assert external contract behavior (tool responses, GraphQL HTTP requests/responses, and file state) rather than private internal implementation details.
- Testing seams should reside at the highest practical layers: the FastMCP tool functions and the GraphQL client boundary.

### Modules Tested
- **Persisted Query Auto-Discovery**: Validate hash discovery from mocked JavaScript bundles, cache persistence, cache corruption recovery, and GraphQL retry handling on stale hash response.
- **Shopping List Tools**: Validate list retrieval, single addition, bulk addition, deletion, auth gating, and confirmation requirements using mocked GraphQL fixtures.
- **Platform Utilities**: Validate that secure file writing and reading succeed across Windows and POSIX platforms without raising permission or path errors.
- **Session Lifecycle**: Validate session status reporting across various states (valid token, expired `sat` JWT, expired `reese84` token, and missing credentials).

### Prior Art
- Leverage existing `respx` mock patterns in `tests/unit/test_graphql_client.py` and `tests/unit/test_cart_tools.py`.
- Follow the fixture conventions established in `tests/conftest.py`.

## Out of Scope
- Direct browser DOM clicking for grocery searches or item additions (all shopping operations remain on the GraphQL API).
- Automated payment method submission or placing final order checkout charges without explicit user execution.
- Third-party delivery driver tracking or external store integrations outside of H-E-B.

## Further Notes
- Upstream PR #21 (`spunkedy`) and PR #13 (`fsesma`) provide the foundation for APQ auto-discovery and shopping list tools.
- Git upstream remote `https://github.com/mgwalkerjr95/texas-grocery-mcp.git` is configured to facilitate future rebases.
