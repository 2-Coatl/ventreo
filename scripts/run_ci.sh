#!/usr/bin/env bash
set -euo pipefail

ruff check .

set +e
pytest
status=$?
set -e
if [[ $status -ne 0 && $status -ne 5 ]]; then
  exit "$status"
fi

if [[ "${CI_SKIP_BYTECODE:-0}" != "1" ]]; then
  mkdir -p build-artifacts
  python <<'PY'
"""Compile project bytecode quietly while skipping cache-heavy directories."""
from __future__ import annotations

import compileall
import pathlib
import re

ROOT = pathlib.Path(".").resolve()
EXCLUDED = re.compile(r"/(?:\.git|\.venv|venv|build|dist|__pycache__)(?:/|$)")

compileall.compile_dir(
    str(ROOT),
    maxlevels=20,
    quiet=1,
    rx=EXCLUDED,
)
PY

  find . -type d -name '__pycache__' -print > cache-dirs.txt

  if [[ -s cache-dirs.txt ]]; then
    tar -czf build-artifacts/bytecode.tar.gz -T cache-dirs.txt
  else
    tar -czf build-artifacts/bytecode.tar.gz --files-from /dev/null
  fi

  while IFS= read -r cache_dir; do
    rm -rf "$cache_dir"
  done < cache-dirs.txt

  rm -f cache-dirs.txt
fi
