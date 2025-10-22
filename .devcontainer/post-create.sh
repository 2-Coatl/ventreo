#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="$(dirname "$0")"
LOG_FILE="$LOG_DIR/post-create.log"
mkdir -p "$LOG_DIR"
: > "$LOG_FILE"

exec > >(tee -a "$LOG_FILE") 2>&1

log() {
  printf '[%s] %s\n' "$(date --iso-8601=seconds)" "$1"
}

run_with_sudo() {
  if command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    "$@"
  fi
}

log "Starting post-create setup"

PACKAGE_MANAGER="apt-get"

if command -v "$PACKAGE_MANAGER" >/dev/null 2>&1; then
  log "Updating package lists"
  if run_with_sudo "$PACKAGE_MANAGER" update -y; then
    log "Installing core packages"
    if run_with_sudo "$PACKAGE_MANAGER" install -y build-essential curl git python3 python3-pip; then
      log "Core packages installed"
    else
      log "Unable to install core packages"
    fi
  else
    log "Unable to update package lists"
  fi
else
  log "Package manager apt-get not available"
fi

PYTHON_BIN="python3"
if command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  log "Upgrading pip"
  if "$PYTHON_BIN" -m pip install --upgrade pip; then
    log "Pip upgraded"
  else
    log "Unable to upgrade pip"
  fi

  log "Installing project tooling"
  if "$PYTHON_BIN" -m pip install --user pipenv; then
    log "Project tooling installed"
  else
    log "Unable to install project tooling"
  fi
else
  log "Python 3 not available"
fi

log "Post-create setup completed"
