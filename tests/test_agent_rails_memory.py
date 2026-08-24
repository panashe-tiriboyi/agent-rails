from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = REPO_ROOT / ".ai" / "tools" / "agent_rails_memory.py"
SPEC = importlib.util.spec_from_file_location("agent_rails_memory", ENGINE_PATH)
assert SPEC and SPEC.loader
memory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(memory)


def sample_record(**overrides):
    record = {
        "schema_version": 1,
        "title": "SQLite memory architecture decision",
        "summary": (
            "The project approved a repository-local SQLite FTS5 memory index backed by "
            "human-readable Markdown records. Agents query the local index before native "
            "platform memory and treat recalled content as historical evidence. The engine "
            "runs only inside an automatically created Python virtual environment."
        ),
        "kind": "decision",
        "tags": ["memory", "sqlite", "architecture"],
        "related_paths": [".ai/context/memory-policy.md"],
        "evidence": "Confirmed",
        "sources": ["docs/requirements/REQ-2026-001-sqlite-memory-engine.md"],
        "platform": "codex",
        "task_ref": "REQ-2026-001",
    }
    record.update(overrides)
    return record


class MemoryEngineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_init_add_search_duplicate_reindex_and_forget(self):
        initialized = memory.init_store(self.root)
        self.assertEqual(initialized["schema_version"], 1)

        added = memory.add_record(self.root, sample_record())
        self.assertEqual(added["stored"], 1)
        self.assertTrue((self.root / added["source"]).exists())
        self.assertNotIn(str(self.root), added["indicator"])

        duplicate = memory.add_record(self.root, sample_record())
        self.assertEqual(duplicate["status"], "duplicate")
        self.assertEqual(duplicate["stored"], 0)

        result = memory.search_records(self.root, "prior sqlite memory architecture")
        self.assertEqual(result["retrieved_count"], 1)
        self.assertEqual(result["confidence"], "high")
        self.assertFalse(result["native_fallback_allowed"])
        self.assertLessEqual(result["retrieved_tokens"], 900)

        db_path = memory.runtime_paths(self.root)["db"]
        db_path.unlink()
        for suffix in ("-wal", "-shm"):
            Path(str(db_path) + suffix).unlink(missing_ok=True)
        rebuilt = memory.reindex_store(self.root)
        self.assertEqual(rebuilt["indexed"], 1)
        self.assertEqual(rebuilt["invalid"], 0)

        forgotten = memory.forget_records(
            self.root, added["id"], None, None, None, False, True
        )
        self.assertEqual(forgotten["forgotten"], 1)
        self.assertFalse((self.root / added["source"]).exists())

    def test_empty_and_low_confidence_search_allows_native_fallback(self):
        empty = memory.search_records(self.root, "unknown history")
        self.assertEqual(empty["confidence"], "none")
        self.assertTrue(empty["native_fallback_allowed"])
        memory.add_record(self.root, sample_record())
        missing = memory.search_records(self.root, "unrelated frobnicator")
        self.assertEqual(missing["retrieved_count"], 0)
        self.assertTrue(missing["native_fallback_allowed"])

    def test_secret_like_content_is_rejected_before_store_creation(self):
        with self.assertRaises(memory.MemoryEngineError) as caught:
            memory.add_record(
                self.root,
                sample_record(summary="Use api_key=abcdefghijklmnop123456 for the integration."),
            )
        self.assertEqual(caught.exception.code, 4)
        self.assertFalse(memory.runtime_paths(self.root)["memory"].exists())

    def test_validation_and_query_sanitization(self):
        with self.assertRaises(memory.MemoryEngineError):
            memory.validate_record(sample_record(kind="transcript"))
        with self.assertRaises(memory.MemoryEngineError):
            memory.validate_record(sample_record(summary="word " * 301))
        terms = memory.query_terms('the sqlite " OR * memory ../path')
        expression = memory.fts_expression(terms)
        self.assertNotIn(" OR *", expression)
        self.assertIn('"sqlite"', expression)

    def test_markdown_round_trip_and_date_forget(self):
        first = memory.add_record(self.root, sample_record())
        parsed = memory.parse_markdown(self.root / first["source"], self.root)
        self.assertEqual(parsed["id"], first["id"])
        self.assertEqual(parsed["kind"], "decision")
        forgotten = memory.forget_records(
            self.root, None, None, "2999-12-31", None, False, True
        )
        self.assertEqual(forgotten["forgotten"], 1)

    def test_reindex_recovers_a_corrupt_database_from_markdown(self):
        added = memory.add_record(self.root, sample_record())
        db_path = memory.runtime_paths(self.root)["db"]
        db_path.write_bytes(b"not a sqlite database")
        rebuilt = memory.reindex_store(self.root)
        self.assertEqual(rebuilt["indexed"], 1)
        self.assertIsNotNone(rebuilt["recovered_backup"])
        self.assertTrue((self.root / rebuilt["recovered_backup"]).exists())
        result = memory.search_records(self.root, "sqlite architecture")
        self.assertEqual(result["results"][0]["id"], added["id"])

    def test_forget_requires_confirmation(self):
        memory.add_record(self.root, sample_record())
        with self.assertRaises(memory.MemoryEngineError):
            memory.forget_records(self.root, None, None, None, None, True, False)

    def test_doctor_reports_expected_checks(self):
        result = memory.doctor(self.root)
        self.assertIn("python_version", result["checks"])
        self.assertIn("virtual_environment", result["checks"])
        self.assertIn("sqlite_fts5", result["checks"])

    def test_concurrent_writes_are_serialized_without_loss(self):
        def write(index):
            return memory.add_record(
                self.root,
                sample_record(
                    title=f"Concurrent memory {index}",
                    summary=f"Concurrent durable outcome number {index} uses SQLite WAL and a busy timeout.",
                    task_ref=f"task-{index}",
                ),
            )

        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(write, range(8)))
        self.assertTrue(all(result["stored"] == 1 for result in results))
        self.assertEqual(memory.status_store(self.root)["chunks"], 8)

    def test_direct_cli_execution_outside_project_venv_is_rejected(self):
        base_python = getattr(sys, "_base_executable", None)
        if not base_python or Path(base_python).resolve() == Path(sys.executable).resolve():
            self.skipTest("No separate base interpreter is available")
        env = os.environ.copy()
        env["AGENT_RAILS_REPO_ROOT"] = str(self.root)
        completed = subprocess.run(
            [base_python, str(ENGINE_PATH), "status"],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(completed.returncode, 3)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["ok"])
        self.assertIn("memory.cmd", payload["error"])


class LauncherContractTests(unittest.TestCase):
    def test_windows_launcher_forwards_to_project_venv(self):
        text = (REPO_ROOT / ".ai" / "tools" / "memory.cmd").read_text(encoding="utf-8")
        self.assertIn(".ai\\runtime\\venv", text)
        self.assertIn("%VENV_PY%", text)
        self.assertIn("fts5", text)

    def test_posix_launcher_forwards_to_project_venv(self):
        text = (REPO_ROOT / ".ai" / "tools" / "memory.sh").read_text(encoding="utf-8")
        self.assertIn(".ai/runtime/venv", text)
        self.assertIn('exec "$VENV_PY"', text)
        self.assertIn("fts5", text)


if __name__ == "__main__":
    unittest.main()
