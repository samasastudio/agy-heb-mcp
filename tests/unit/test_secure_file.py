"""Tests for secure file operations."""

import json
import os
from pathlib import Path

import pytest

from texas_grocery_mcp.utils.secure_file import (
    SECURE_FILE_MODE,
    ensure_secure_permissions,
    get_temp_dir,
    write_secure_json,
)


def assert_secure_file(path: Path, expected_mode: int = SECURE_FILE_MODE) -> None:
    """Helper to verify file exists and has correct permissions on POSIX systems."""
    assert path.exists()
    if os.name != "nt":
        mode = path.stat().st_mode & 0o777
        assert mode == expected_mode, f"Expected {oct(expected_mode)}, got {oct(mode)}"


class TestGetTempDir:
    """Tests for get_temp_dir function."""

    def test_returns_existing_path(self):
        """Verify get_temp_dir returns an existing directory Path."""
        temp_dir = get_temp_dir()
        assert isinstance(temp_dir, Path)
        assert temp_dir.exists()
        assert temp_dir.is_dir()


class TestWriteSecureJson:
    """Tests for write_secure_json function."""

    def test_creates_file_with_correct_permissions(self, tmp_path):
        """Verify files are created with 0o600 permissions."""
        test_file = tmp_path / "test.json"
        write_secure_json(test_file, {"key": "value"})

        assert_secure_file(test_file)

    def test_writes_valid_json(self, tmp_path):
        """Verify JSON content is written correctly."""
        test_file = tmp_path / "test.json"
        data = {"key": "value", "nested": {"a": 1, "b": [1, 2, 3]}}
        write_secure_json(test_file, data)

        with open(test_file) as f:
            loaded = json.load(f)

        assert loaded == data

    def test_creates_parent_directories(self, tmp_path):
        """Verify parent directories are created."""
        test_file = tmp_path / "nested" / "dir" / "test.json"
        write_secure_json(test_file, {"key": "value"})

        assert test_file.exists()
        assert test_file.parent.exists()

    def test_overwrites_existing_file(self, tmp_path):
        """Verify existing files are overwritten."""
        test_file = tmp_path / "test.json"

        # Write initial content
        write_secure_json(test_file, {"old": "data"})

        # Overwrite
        write_secure_json(test_file, {"new": "data"})

        with open(test_file) as f:
            loaded = json.load(f)

        assert loaded == {"new": "data"}

    def test_fixes_insecure_permissions_on_existing_file(self, tmp_path):
        """Verify existing files get permissions corrected on rewrite."""
        test_file = tmp_path / "test.json"

        # Create with insecure permissions
        test_file.write_text("{}")
        os.chmod(test_file, 0o644)

        # Rewrite should fix permissions
        write_secure_json(test_file, {"key": "value"})

        assert_secure_file(test_file)

    def test_cleans_up_temp_file_on_json_error(self, tmp_path):
        """Verify temp files are cleaned up on serialization errors."""
        test_file = tmp_path / "test.json"

        # Create an object that can't be JSON serialized
        class NotSerializable:
            pass

        with pytest.raises(TypeError):
            write_secure_json(test_file, {"bad": NotSerializable()})

        # Temp file should be cleaned up
        temp_file = test_file.with_suffix(".tmp")
        assert not temp_file.exists()


class TestEnsureSecurePermissions:
    """Tests for ensure_secure_permissions function."""

    def test_returns_true_for_nonexistent_file(self, tmp_path):
        """Verify returns True for files that don't exist."""
        test_file = tmp_path / "nonexistent.json"
        assert ensure_secure_permissions(test_file) is True

    def test_fixes_insecure_permissions(self, tmp_path):
        """Verify insecure permissions are fixed."""
        test_file = tmp_path / "test.json"
        test_file.write_text("{}")
        os.chmod(test_file, 0o644)

        result = ensure_secure_permissions(test_file)

        assert result is True
        assert_secure_file(test_file)

    def test_leaves_secure_permissions_unchanged(self, tmp_path):
        """Verify already-secure files are not modified."""
        test_file = tmp_path / "test.json"
        test_file.write_text("{}")
        os.chmod(test_file, SECURE_FILE_MODE)

        result = ensure_secure_permissions(test_file)

        assert result is True
        assert_secure_file(test_file)

    def test_handles_world_readable_file(self, tmp_path):
        """Verify world-readable files are fixed."""
        test_file = tmp_path / "test.json"
        test_file.write_text("{}")
        os.chmod(test_file, 0o777)  # World readable/writable/executable

        result = ensure_secure_permissions(test_file)

        assert result is True
        assert_secure_file(test_file)

    def test_windows_returns_true_without_chmod(self, monkeypatch, tmp_path):
        """Verify Windows platform immediately returns True without checking POSIX mode."""
        test_file = tmp_path / "test.json"
        test_file.write_text("{}")
        monkeypatch.setattr(os, "name", "nt")
        assert ensure_secure_permissions(test_file) is True

    def test_posix_fixes_insecure_mode(self, monkeypatch, tmp_path):
        """Verify POSIX branch executes chmod when mode is insecure."""
        test_file = tmp_path / "test.json"
        test_file.write_text("{}")
        chmod_calls = []
        monkeypatch.setattr(os, "name", "posix")
        monkeypatch.setattr(os, "chmod", lambda p, m: chmod_calls.append((p, m)))

        class MockStat:
            st_mode = 0o100644

        monkeypatch.setattr(Path, "stat", lambda self: MockStat())

        result = ensure_secure_permissions(test_file)
        assert result is True
        assert len(chmod_calls) == 1
        assert chmod_calls[0][1] == SECURE_FILE_MODE
