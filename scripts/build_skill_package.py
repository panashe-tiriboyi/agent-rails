#!/usr/bin/env python3
"""Build the Agent Rails skill ZIP reproducibly from canonical source."""

from __future__ import annotations

import argparse
import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "agent-rails"
OUTPUT = ROOT / "skills" / "agent-rails.zip"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )


def archive_bytes() -> bytes:
    if not SOURCE.is_dir():
        raise FileNotFoundError(f"Canonical skill source not found: {SOURCE}")
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in source_files():
            relative = path.relative_to(SOURCE.parent).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            executable = path.suffix == ".sh" or path.name.endswith(".py")
            info.external_attr = ((0o755 if executable else 0o644) & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail if the current ZIP differs from canonical source."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected = archive_bytes()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != expected:
            print(f"OUTDATED: {OUTPUT.relative_to(ROOT)}")
            return 1
        print(f"OK: {OUTPUT.relative_to(ROOT)} matches canonical source")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="agent-rails-", suffix=".zip", dir=OUTPUT.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(expected)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, OUTPUT)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f"BUILT: {OUTPUT.relative_to(ROOT)} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
