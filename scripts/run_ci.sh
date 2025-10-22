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
  python -m compileall .
  find . -name '__pycache__' -type d -print > cache-dirs.txt

  if [[ -s cache-dirs.txt ]]; then
    tar -czf build-artifacts/bytecode.tar.gz -T cache-dirs.txt
  else
    tar -czf build-artifacts/bytecode.tar.gz --files-from /dev/null
  fi

  rm -f cache-dirs.txt
fi
