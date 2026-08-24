#!/usr/bin/env sh
set -eu

TOOLS_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$TOOLS_DIR/../.." && pwd)
VENV_DIR="$REPO_ROOT/.ai/runtime/venv"
VENV_PY="$VENV_DIR/bin/python"
ENGINE="$TOOLS_DIR/agent_rails_memory.py"

find_python() {
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 &&
      "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)' >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

if [ ! -x "$VENV_PY" ]; then
  if ! BOOTSTRAP_PY=$(find_python); then
    printf '%s\n' '{"ok":false,"error":"Python 3.11 or newer was not found. Install Python, then rerun this launcher."}'
    exit 3
  fi
  if ! "$BOOTSTRAP_PY" -m venv "$VENV_DIR"; then
    printf '%s\n' '{"ok":false,"error":"Could not create .ai/runtime/venv. Verify that Python venv support is installed and the repository is writable."}'
    exit 3
  fi
fi

if ! "$VENV_PY" -c "import sqlite3; c=sqlite3.connect(':memory:'); c.execute('CREATE VIRTUAL TABLE t USING fts5(x)')" >/dev/null 2>&1; then
  printf '%s\n' '{"ok":false,"error":"The selected Python sqlite3 module does not include FTS5. Install a Python 3.11+ build with FTS5."}'
  exit 3
fi

exec "$VENV_PY" "$ENGINE" "$@"
