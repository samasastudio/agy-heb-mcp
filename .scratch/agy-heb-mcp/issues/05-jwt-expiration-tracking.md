# 05: Implement sat JWT Expiration Tracking & Honest Health Telemetry

**What to build:** Implement inspection of the `sat` cookie's JWT `exp` claim to prevent false-positive session health reports and silent `401 Unauthorized` errors. Currently, `session_status` can report success even when the 30-minute `sat` token has expired. This ticket adds precise JWT parsing, calculates actual remaining lifespan, and provides truthful lifecycle messages to the agent.

**Blocked by:** 04: Build Antigravity Browser Session Sync Bridge
**Status:** ready-for-agent
**GitHub Issue:** https://github.com/samasastudio/agy-heb-mcp/issues/6

- [ ] Parse and decode JWT payload of the `sat` cookie without verifying external signature
- [ ] Calculate remaining session lifetime based on `exp` timestamp vs current UTC time
- [ ] Update `session_status` to set `needs_refresh: True` if `sat` is expired or within auto-refresh threshold
- [ ] Update `cart_check_auth` and tool preconditions to warn before 401 Unauthorized occurs
- [ ] Add unit tests in `tests/unit/test_session_refresh.py` asserting accurate status for expired vs fresh JWTs
