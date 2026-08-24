#!/usr/bin/env python3
"""Generate a conservative AI resource scaffold for a target repository."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "full-ai-pack"

SCAFFOLD_DIRS = [
    ".ai",
    ".ai/agents",
    ".ai/context",
    ".ai/prompts",
    ".ai/skills",
    ".ai/skills/agent-rails-memory",
    ".ai/tools",
    "docs",
    "docs/requirements",
]

MARKER_DIRS = [
    ".ai/agents",
    ".ai/prompts",
    ".ai/skills",
]

REQUEST_TEMPLATE = Path("docs/requirements/change-request-template.md")
PLACEHOLDER_RE = re.compile(r"\{[A-Z0-9_\-| ]+\}")
GITIGNORE_TEMPLATE = Path(".gitignore")
REQUIRED_IGNORE_RULES = (".ai/runtime/", ".ai/memory/", "__pycache__/", "*.py[cod]")
OBSOLETE_IGNORE_LINES = {
    ".agent-rails/",
    "# Agent Rails private local runtime: virtual environment, Markdown memories, and SQLite index.",
}


@dataclass
class Action:
    kind: str
    path: Path
    detail: str = ""

    def line(self, root: Path) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        suffix = f" - {self.detail}" if self.detail else ""
        return f"{self.kind}: {rel}{suffix}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold Agent Rails guidance, local memory, and requirements resources."
    )
    parser.add_argument("--target", required=True, help="Target project directory.")
    parser.add_argument(
        "--mode",
        choices=["new", "existing"],
        default="existing",
        help=(
            "State of the target directory: 'new' bootstraps an empty or fresh "
            "folder, 'existing' merges into a repo with prior content. "
            "Controls merge behavior, not pack content."
        ),
    )
    parser.add_argument(
        "--resource-mode",
        choices=["new-project", "existing-project", "migration"],
        help=(
            "Shape of the AI-resource pack to emit (the workflow the kit "
            "prompts describe). Defaults from --mode; use 'migration' to "
            "include migration-oriented context. Independent of --mode: "
            "e.g. --mode existing --resource-mode migration adds migration "
            "resources to an existing repo without overwriting it."
        ),
    )
    parser.add_argument(
        "--tier",
        choices=["lightweight", "standard", "strict"],
        default="standard",
        help="Governance level recorded in the generated pack.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview only.")
    parser.add_argument("--apply", action="store_true", help="Write files.")
    parser.add_argument("--project-name")
    parser.add_argument("--project-description")
    parser.add_argument("--current-state")
    parser.add_argument("--decision-authority")
    parser.add_argument("--code-map")
    parser.add_argument("--test-map")
    parser.add_argument("--docs-map")
    parser.add_argument("--deployment-map")
    parser.add_argument("--verification-command", action="append", default=[])
    parser.add_argument("--source-doc", action="append", default=[])
    parser.add_argument("--local-tooling-exclusion", action="append", default=[])
    args = parser.parse_args()
    if args.apply and args.dry_run:
        parser.error("Choose either --apply or --dry-run, not both.")
    return args


def discover_project_name(target: Path) -> str:
    return target.name or "Project"


def exists_any(target: Path, patterns: Iterable[str]) -> bool:
    return any(target.glob(pattern) for pattern in patterns)


def infer_verification_commands(target: Path) -> list[str]:
    commands: list[str] = []
    if (target / "package.json").exists():
        commands.extend(["npm test", "npm run lint"])
    if exists_any(target, ["*.sln", "**/*.csproj"]):
        commands.append("dotnet test")
    if any((target / name).exists() for name in ["pyproject.toml", "pytest.ini", "setup.cfg"]):
        commands.append("pytest")
    return commands or ["Add project verification commands here."]


def infer_code_map(target: Path) -> list[str]:
    candidates = [
        "src",
        "app",
        "web",
        "server",
        "api",
        "frontend",
        "backend",
        "notebooks",
        "scripts",
    ]
    found = [f"- `{name}/`" for name in candidates if (target / name).is_dir()]
    return found or ["- Record source folders after project inspection."]


def infer_test_map(target: Path) -> list[str]:
    candidates = ["tests", "test", "spec", "e2e", "__tests__"]
    found = [f"- `{name}/`" for name in candidates if (target / name).is_dir()]
    return found or ["- Record test folders after project inspection."]


def infer_docs_map(target: Path) -> list[str]:
    found = []
    for name in ["README.md", "README.MD", "docs"]:
        if (target / name).exists():
            found.append(f"- `{name}`")
    return found or ["- Add documentation map after project inspection."]


def format_lines(values: Iterable[str], fallback: str) -> str:
    cleaned = [value.strip() for value in values if value and value.strip()]
    if not cleaned:
        cleaned = [fallback]
    lines = []
    for value in cleaned:
        lines.append(value if value.startswith("-") else f"- {value}")
    return "\n".join(lines)


def tier_notes(tier: str) -> str:
    if tier == "lightweight":
        return "\n".join(
            [
                "- Keep process light and bias toward useful project memory.",
                "- Use formal requirements only for non-trivial behavior or architecture changes.",
                "- Record assumptions plainly when a decision log would be too heavy.",
            ]
        )
    if tier == "strict":
        return "\n".join(
            [
                "- Do not infer completeness from existing code, docs, tests, or old status labels.",
                "- Require approved requirements for behavior changes and durable target decisions.",
                "- Treat readiness, security, and production claims as unverified without current evidence.",
                "- Fail closed for security-sensitive or externally dependent behavior when configuration or required calls are unavailable.",
            ]
        )
    return "\n".join(
        [
            "- Use requirements for meaningful behavior, architecture, or workflow changes.",
            "- Record decisions that affect target behavior, interfaces, deployment, security, or source-of-truth docs.",
            "- Match verification effort to risk and cite current evidence for durable claims.",
        ]
    )


def build_replacements(target: Path, args: argparse.Namespace) -> dict[str, str]:
    resource_mode = args.resource_mode
    if not resource_mode:
        resource_mode = "new-project" if args.mode == "new" else "existing-project"
    verification = args.verification_command or infer_verification_commands(target)
    source_docs = args.source_doc or ["README.md and docs discovered during inspection."]
    local_exclusions = args.local_tooling_exclusion or [
        ".codex/",
        ".agents/",
        ".vscode/",
        ".idea/",
        ".obsidian/",
        "node_modules/",
        "build outputs and caches",
    ]
    replacements = {
        "{PROJECT_NAME}": args.project_name or discover_project_name(target),
        "{PROJECT_DESCRIPTION}": args.project_description
        or "Project-specific AI resource workspace.",
        "{RESOURCE_MODE}": resource_mode,
        "{CURRENT_STATE}": args.current_state
        or "Unverified; inspect current code and docs before making durable claims.",
        "{GOVERNANCE_TIER}": args.tier,
        "{GOVERNANCE_TIER_NOTES}": tier_notes(args.tier),
        "{DECISION_AUTHORITY}": args.decision_authority or "Project maintainer",
        "{CODE_MAP}": args.code_map or "\n".join(infer_code_map(target)),
        "{TEST_MAP}": args.test_map or "\n".join(infer_test_map(target)),
        "{DOCS_MAP}": args.docs_map or "\n".join(infer_docs_map(target)),
        "{DEPLOYMENT_MAP}": args.deployment_map
        or "- Record deployment and operational paths after project inspection.",
        "{SOURCE_OF_TRUTH_DOCS}": format_lines(
            source_docs,
            "- Record source-of-truth docs after project inspection.",
        ),
        "{LOCAL_TOOLING_EXCLUSIONS}": format_lines(
            local_exclusions,
            "- Record local tooling exclusions after project inspection.",
        ),
        "{VERIFICATION_COMMANDS}": format_lines(
            verification,
            "- Add project verification commands here.",
        ),
    }
    return replacements


def render_template(path: Path, replacements: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def template_files() -> list[Path]:
    return sorted(
        path
        for path in TEMPLATE_ROOT.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    )


def ensure_dir(path: Path, apply: bool, actions: list[Action], root: Path) -> None:
    if path.exists():
        actions.append(Action("preserve-dir", path))
        return
    actions.append(Action("create-dir", path))
    if apply:
        path.mkdir(parents=True, exist_ok=True)


def write_file(
    path: Path,
    content: str,
    apply: bool,
    actions: list[Action],
    root: Path,
    kind: str = "create-file",
) -> bool:
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            existing = None
        if existing == content:
            detail = "already matches generated content"
            actions.append(Action("preserve-file", path, detail))
        else:
            detail = "existing file was not changed; review before merging generated guidance"
            actions.append(Action("conflict", path, detail))
        return False
    actions.append(Action(kind, path))
    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    return True


def marker_needed(target_dir: Path) -> bool:
    if not target_dir.exists():
        return True
    return not any(child.name != ".gitkeep" for child in target_dir.iterdir())


def ensure_memory_ignored(
    target: Path, apply: bool, actions: list[Action], root: Path
) -> bool:
    path = target / GITIGNORE_TEMPLATE
    template = (TEMPLATE_ROOT / GITIGNORE_TEMPLATE).read_text(encoding="utf-8")
    if not path.exists():
        return write_file(path, template, apply, actions, root)
    existing = path.read_text(encoding="utf-8")
    rules = {line.strip() for line in existing.splitlines()}
    missing = [rule for rule in REQUIRED_IGNORE_RULES if rule not in rules]
    obsolete_present = any(line.strip() in OBSOLETE_IGNORE_LINES for line in existing.splitlines())
    if not missing and not obsolete_present:
        actions.append(Action("preserve-file", path, "Agent Rails local state and Python caches are already ignored"))
        return False
    actions.append(Action("merge-file", path, "migrate Agent Rails local-state and Python cache ignore rules"))
    if apply:
        preserved_lines = [
            line for line in existing.splitlines()
            if line.strip() not in OBSOLETE_IGNORE_LINES
        ]
        preserved = "\n".join(preserved_lines).rstrip()
        addition = "# Agent Rails local runtime additions.\n" + "\n".join(missing)
        combined = (preserved + "\n" if preserved else "") + (addition + "\n" if missing else "")
        path.write_text(combined, encoding="utf-8", newline="\n")
    return True


def validate_rendered(rel: Path, content: str, actions: list[Action], root: Path) -> None:
    if rel != REQUEST_TEMPLATE:
        matches = PLACEHOLDER_RE.findall(content)
        if matches:
            actions.append(
                Action(
                    "validate",
                    root / rel,
                    f"unresolved placeholders: {', '.join(sorted(set(matches)))}",
                )
            )


def validate_structure(target: Path, actions: list[Action]) -> None:
    for rel in SCAFFOLD_DIRS:
        path = target / rel
        if not path.exists():
            actions.append(Action("validate", path, "missing scaffold directory"))
    for rel in MARKER_DIRS:
        marker = target / rel / ".gitkeep"
        directory = target / rel
        if directory.exists() and marker_needed(directory) and not marker.exists():
            actions.append(Action("validate", marker, "missing marker for empty directory"))


def generate(args: argparse.Namespace) -> tuple[list[Action], int]:
    target = Path(args.target).expanduser().resolve()
    apply = bool(args.apply)
    actions: list[Action] = []

    if not TEMPLATE_ROOT.exists():
        raise SystemExit(f"Template root not found: {TEMPLATE_ROOT}")

    if args.mode == "existing" and not target.exists():
        actions.append(Action("validate", target, "existing mode target does not exist"))
        return actions, 2

    ensure_dir(target, apply, actions, target)

    for rel in SCAFFOLD_DIRS:
        ensure_dir(target / rel, apply, actions, target)

    replacements = build_replacements(target, args)
    created_any = ensure_memory_ignored(target, apply, actions, target)

    for source in template_files():
        rel = source.relative_to(TEMPLATE_ROOT)
        if rel == GITIGNORE_TEMPLATE:
            continue
        destination = target / rel
        content = render_template(source, replacements)
        validate_rendered(rel, content, actions, target)
        created = write_file(destination, content, apply, actions, target)
        created_any = created_any or created

    for rel in MARKER_DIRS:
        directory = target / rel
        marker = directory / ".gitkeep"
        if marker_needed(directory):
            created = write_file(
                marker,
                "Preserves the AI resource scaffold directory.\n",
                apply,
                actions,
                target,
                kind="marker",
            )
            created_any = created_any or created

    if apply:
        validate_structure(target, actions)

    if not created_any:
        actions.append(Action("summary", target, "no files created; existing files preserved"))

    return actions, 0


def main() -> int:
    args = parse_args()
    actions, code = generate(args)
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode} agent-rails target={Path(args.target).resolve()}")
    for action in actions:
        print(action.line(Path(args.target).resolve()))
    if not args.apply:
        print("No files were written. Re-run with --apply to create missing resources.")
    return code


if __name__ == "__main__":
    sys.exit(main())
