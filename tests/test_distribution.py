from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL = REPO_ROOT / "skills" / "agent-rails"
GENERATOR = CANONICAL / "scripts" / "generate_ai_resources.py"
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_skill_package.py"


class DistributionTests(unittest.TestCase):
    def test_installable_skill_has_no_obsolete_runtime_path(self):
        checked = [CANONICAL / "SKILL.md"]
        checked.extend((CANONICAL / "assets" / "full-ai-pack").rglob("*"))
        checked.extend((CANONICAL / "references").rglob("*.md"))
        for path in checked:
            if path.is_file():
                with self.subTest(path=path.relative_to(CANONICAL)):
                    self.assertNotIn(".agent-rails", path.read_text(encoding="utf-8"))

    def test_shared_runtime_files_match_reference_pack(self):
        shared = [
            ".ai/tools/agent_rails_memory.py",
            ".ai/tools/memory.cmd",
            ".ai/tools/memory.sh",
            ".ai/context/memory-policy.md",
            ".ai/skills/agent-rails-memory/SKILL.md",
            ".gitignore",
        ]
        template = CANONICAL / "assets" / "full-ai-pack"
        for relative in shared:
            with self.subTest(relative=relative):
                self.assertEqual(
                    (REPO_ROOT / relative).read_bytes(),
                    (template / relative).read_bytes(),
                )

    def test_generator_dry_run_apply_and_safe_gitignore_merge(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target"
            target.mkdir()
            dry_run = subprocess.run(
                [sys.executable, str(GENERATOR), "--target", str(target), "--mode", "existing", "--dry-run"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertIn("create-file: .ai\\tools\\agent_rails_memory.py", dry_run.stdout)
            self.assertFalse((target / ".ai").exists())

            applied = subprocess.run(
                [sys.executable, str(GENERATOR), "--target", str(target), "--mode", "existing", "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertTrue((target / ".ai" / "tools" / "agent_rails_memory.py").exists())
            self.assertTrue((target / ".ai" / "context" / "memory-policy.md").exists())
            self.assertEqual((target / ".gitignore").read_text(encoding="utf-8"), (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"))

            (target / ".gitignore").write_text("user-rule\n.agent-rails/\n", encoding="utf-8")
            merged = subprocess.run(
                [sys.executable, str(GENERATOR), "--target", str(target), "--mode", "existing", "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(merged.returncode, 0, merged.stderr)
            self.assertIn("merge-file: .gitignore", merged.stdout)
            merged_rules = (target / ".gitignore").read_text(encoding="utf-8")
            self.assertTrue(merged_rules.startswith("user-rule\n"))
            self.assertIn(".ai/runtime/", merged_rules)
            self.assertIn(".ai/memory/", merged_rules)
            self.assertNotIn(".agent-rails/", merged_rules)

    def test_built_zip_matches_canonical_source(self):
        completed = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        with zipfile.ZipFile(REPO_ROOT / "skills" / "agent-rails.zip") as archive:
            names = set(archive.namelist())
        self.assertIn("agent-rails/assets/full-ai-pack/.ai/tools/agent_rails_memory.py", names)
        self.assertIn("agent-rails/assets/full-ai-pack/.ai/skills/agent-rails-memory/SKILL.md", names)

    def test_generated_launcher_creates_and_reuses_virtual_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "generated"
            target.mkdir()
            generated = subprocess.run(
                [sys.executable, str(GENERATOR), "--target", str(target), "--mode", "existing", "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)
            if sys.platform == "win32":
                launcher = target / ".ai" / "tools" / "memory.cmd"
                command = ["cmd.exe", "/d", "/c", str(launcher)]
                venv_python = target / ".ai" / "runtime" / "venv" / "Scripts" / "python.exe"
            else:
                launcher = target / ".ai" / "tools" / "memory.sh"
                command = ["sh", str(launcher)]
                venv_python = target / ".ai" / "runtime" / "venv" / "bin" / "python"

            first = subprocess.run(
                [*command, "doctor"], text=True, capture_output=True, timeout=120, check=False
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertTrue(json.loads(first.stdout)["ok"])
            self.assertTrue(venv_python.exists())
            first_mtime = venv_python.stat().st_mtime_ns

            second = subprocess.run(
                [*command, "status"], text=True, capture_output=True, timeout=30, check=False
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(venv_python.stat().st_mtime_ns, first_mtime)


if __name__ == "__main__":
    unittest.main()
