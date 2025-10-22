"""Tests for the `check_no_emojis` utility."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest
from pytest import LogCaptureFixture

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import check_no_emojis as checker  # noqa: E402


@pytest.fixture(autouse=True)
def reset_logger_handlers():
    """Reset logger handlers to ensure predictable logging during tests."""
    logger = logging.getLogger(checker.__name__)
    previous_handlers = list(logger.handlers)
    for handler in previous_handlers:
        logger.removeHandler(handler)
    yield
    for handler in previous_handlers:
        logger.addHandler(handler)


def create_file(path: Path, content: str = "") -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_collect_files_ignores_excluded_directories(tmp_path: Path) -> None:
    base = tmp_path / "project"
    base.mkdir()
    allowed_file = create_file(base / "allowed.txt", "plain text\n")

    excluded_dir = base / "build"
    excluded_dir.mkdir()
    create_file(excluded_dir / "artifact.txt", "🚀 release")

    collected = list(
        checker.collect_files(
            [str(base)],
            exclude=[str(excluded_dir)],
        )
    )

    assert collected == [allowed_file.resolve()]


def test_file_contains_emoji_detects_unicode(tmp_path: Path) -> None:
    file_with_emoji = create_file(tmp_path / "emoji.txt", "Hola 👋 mundo\n")

    results = list(checker.file_contains_emoji(file_with_emoji))

    assert results == [(1, "Hola 👋 mundo")]


def test_main_returns_error_when_emoji_found(
    tmp_path: Path, caplog: LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    file_with_emoji = create_file(tmp_path / "emoji.txt", "Hola 👋 mundo\n")

    exit_code = checker.main([str(file_with_emoji)])

    assert exit_code == 1
    assert any("Emoji found" in message for message in caplog.messages)


def test_main_succeeds_without_paths(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)

    exit_code = checker.main([])

    assert exit_code == 0
    assert "No paths provided" in " ".join(caplog.messages)
