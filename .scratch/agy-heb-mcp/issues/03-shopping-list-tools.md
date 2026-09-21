# 03: Integrate Native H-E-B Shopping List Tools (PR #13)

**What to build:** Integrate upstream PR #13 (by @fsesma) to provide complete H-E-B shopping list capabilities via 6 new FastMCP tools. Enables users to inspect lists, add single or bulk items with confirmation gates and verification, and remove list items.

**Blocked by:** 02: Integrate Apollo Persisted Query (APQ) Hash Auto-Discovery (PR #21)
**Status:** ready-for-agent
**GitHub Issue:** https://github.com/samasastudio/agy-heb-mcp/issues/4

- [ ] Register 6 shopping list tools in `server.py` (`shopping_list_check_auth`, `shopping_list_get`, `shopping_list_add`, `shopping_list_add_many`, `shopping_list_add_with_retry`, `shopping_list_remove`)
- [ ] Implement shopping list domain logic in `tools/shopping_list.py` and GraphQL operations in `clients/graphql.py`
- [ ] Enforce human confirmation gate (`confirm=True`) on destructive mutations
- [ ] Support named lists via `list_name` parameter and `HEB_DEFAULT_SHOPPING_LIST` environment variable
- [ ] Pass all shopping list unit tests in `tests/unit/test_shopping_list_tools.py`
