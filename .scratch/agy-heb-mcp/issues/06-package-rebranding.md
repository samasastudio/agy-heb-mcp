# 06: Package Rebranding (agy-heb-mcp) & Antigravity Global MCP Registration

**What to build:** Finalize the transition to `agy-heb-mcp`. Update package metadata in `pyproject.toml`, set up console script entrypoint `agy-heb-mcp`, update README documentation with Antigravity-specific examples, and register the server globally in `~/.gemini/config/mcp_config.json`.

**Blocked by:** 02: Integrate Apollo Persisted Query (APQ) Hash Auto-Discovery (PR #21), 03: Integrate Native H-E-B Shopping List Tools (PR #13), 05: Implement sat JWT Expiration Tracking & Honest Health Telemetry
**Status:** ready-for-agent
**GitHub Issue:** https://github.com/samasastudio/agy-heb-mcp/issues/7

- [ ] Update `pyproject.toml` name, version, and scripts entrypoint to `agy-heb-mcp`
- [ ] Ensure backward compatibility with `texas-grocery-mcp` CLI alias if needed
- [ ] Register `agy-heb-mcp` in `~/.gemini/config/mcp_config.json` using uv run/uvx
- [ ] Verify that Antigravity starts and discovers all registered tools (store, product, cart, coupon, shopping list, session)
- [ ] Update README with Antigravity quickstart and session bridge instructions
