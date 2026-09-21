# 04: Build Antigravity Browser Session Sync Bridge

**What to build:** Build a session sync bridge that extracts authenticated H-E-B session state (cookies: `sat`, `sst`, `JSESSIONID` and localStorage `reese84` bot token) from Antigravity's persistent browser context directly into `~/.texas-grocery-mcp/auth.json`. Eliminates headless bot-detection interception and allows users to authenticate once natively in Antigravity's browser.

**Blocked by:** 01: Fix Windows Platform Compatibility & Permission Guards
**Status:** ready-for-agent
**GitHub Issue:** https://github.com/samasastudio/agy-heb-mcp/issues/5

- [ ] Implement an Antigravity session extraction utility in `auth/antigravity_bridge.py`
- [ ] Read active H-E-B cookies and `reese84` token from browser storage/CDP
- [ ] Export state into standard Playwright `storage_state` JSON at `auth_state_path`
- [ ] Wire the bridge into `session_refresh` so Antigravity users can trigger session sync directly
- [ ] Verify `session_status` reports `authenticated: True, needs_refresh: False` when synced
