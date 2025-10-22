"""Pre-commit hook to ensure no emoji characters are committed."""
from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Iterable, Iterator, Sequence

LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

DEFAULT_EXCLUDED_DIRS: tuple[str, ...] = (
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "build",
    "dist",
    "__pycache__",
)

EMOJI_PATTERN = (
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F004"
    "\U0001F0CF"
    "\U00002600-\U000026FF"
    "\U0001F1E6-\U0001F1FF"
    "\U00002300-\U000023FF"
    "\U0001F018-\U0001F270"
    "\U0001F000-\U0001F02F"
    "]"
)
EMOJI_REGEX = re.compile(EMOJI_PATTERN)


def parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail when files contain emoji characters.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="File or directory paths to scan. Defaults to staged files in pre-commit.",
    )
    parser.add_argument(
        "--exclude",
        "-e",
        action="append",
        default=list(DEFAULT_EXCLUDED_DIRS),
        help="Relative paths to exclude from the search.",
    )
    return parser.parse_args(argv)


def collect_files(paths: Iterable[str], exclude: Sequence[str]) -> Iterator[Path]:
    excluded = {Path(item).resolve() for item in exclude}
    seen: set[Path] = set()

    for raw_path in paths:
        path = Path(raw_path).resolve()
        if _is_excluded(path, excluded):
            continue
        if path.is_dir():
            for child in iter_directory(path, excluded):
                if child not in seen:
                    seen.add(child)
                    yield child
        elif path.is_file():
            if path not in seen:
                seen.add(path)
                yield path


def iter_directory(directory: Path, excluded: set[Path]) -> Iterator[Path]:
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        if _is_excluded(root_path, excluded):
            dirs[:] = []
            continue

        dirs[:] = [
            directory
            for directory in dirs
            if not _is_excluded((root_path / directory).resolve(), excluded)
        ]

        for file_name in files:
            file_path = (root_path / file_name).resolve()
            if _is_excluded(file_path, excluded):
                continue
            yield file_path


def _is_excluded(path: Path, excluded: set[Path]) -> bool:
    return any(candidate == path or candidate in path.parents for candidate in excluded)


def file_contains_emoji(path: Path) -> Iterator[tuple[int, str]]:
    try:
        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if EMOJI_REGEX.search(line):
                    yield line_number, line.rstrip("\n")
    except UnicodeDecodeError:
        LOGGER.debug("Skipping binary file %s", path)
    except OSError as error:
        LOGGER.debug("Unable to read %s: %s", path, error)


def main(argv: Sequence[str] | None = None) -> int:
    argument_list = list(sys.argv[1:] if argv is None else argv)
    args = parse_arguments(argument_list)
    paths = list(args.paths)

    if not paths:
        LOGGER.info("No paths provided to check for emojis.")
        return 0

    violations: list[tuple[Path, int, str]] = []
    for file_path in collect_files(paths, args.exclude):
        for line_number, line in file_contains_emoji(file_path):
            violations.append((file_path, line_number, line))

    if not violations:
        LOGGER.info("No emoji characters detected.")
        return 0

    for file_path, line_number, line in violations:
        LOGGER.error("Emoji found in %s:%s -> %s", file_path, line_number, line)

    return 1


if __name__ == "__main__":
    sys.exit(main())
