# 01: Fix Windows Platform Compatibility & Permission Guards

**What to build:** Fix all Windows and NTFS incompatibilities in the codebase so that tests and runtime file operations succeed cleanly on Windows. Replaces hardcoded POSIX `/tmp` screenshot paths with `tempfile.gettempdir()` and guards POSIX `chmod 0o600` mode assertions in file security and credential utilities when running on Windows.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent
**GitHub Issue:** https://github.com/samasastudio/agy-heb-mcp/issues/2

- [ ] In `secure_file.py`, guard `0o600` permission enforcement so it only runs when `os.name != 'nt'`
- [ ] In `credentials.py`, ensure credential file writing succeeds without failing on Windows NTFS permissions
- [ ] In `tests/unit/test_secure_file.py` and `tests/unit/test_credentials.py`, test platform-appropriate file mode behavior
- [ ] Replace hardcoded `/tmp/heb-login-*.png` screenshot paths in `browser_refresh.py` with `tempfile.gettempdir()`
- [ ] Run `pytest tests/unit` and verify 100% of tests pass on Windows (0 failures)
