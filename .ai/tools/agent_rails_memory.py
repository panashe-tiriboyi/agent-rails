#!/usr/bin/env python3
"""Dependency-free, repository-local Agent Rails memory engine."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
MIN_PYTHON = (3, 11)
DEFAULT_LIMIT = 3
MAX_CANDIDATES = 50
MAX_RETRIEVED_TOKENS = 900
MAX_CHUNK_TOKENS = 300
CONFIDENCE_THRESHOLD = 0.55
ALLOWED_KINDS = {
    "decision",
    "fix",
    "architecture",
    "constraint",
    "workflow",
    "lesson",
    "preference",
}
ALLOWED_EVIDENCE = {"Confirmed", "Likely", "Unclear", "Missing", "Contradiction", "Assumption"}
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
    "i", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "was", "we", "were", "what", "when", "where", "which", "who", "why", "with",
}
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.I)),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("github-token", re.compile(r"\bgh[opusr]_[A-Za-z0-9_]{30,}\b")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("credential-uri", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:]+:[^\s/@]+@", re.I)),
    (
        "secret-assignment",
        re.compile(
            r"\b(?:api[_-]?key|client[_-]?secret|password|passwd|access[_-]?token|auth[_-]?token)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9+/_.-]{12,}",
            re.I,
        ),
    ),
)
TOKEN_RE = re.compile(r"[\w./\\:-]+", re.UNICODE)
WORD_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


class MemoryEngineError(Exception):
    """An expected engine failure with a stable process exit code."""

    def __init__(self, message: str, code: int = 5, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


def repo_root_from_script() -> Path:
    override = os.environ.get("AGENT_RAILS_REPO_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def runtime_paths(root: Path) -> dict[str, Path]:
    runtime = root / ".ai"
    memory = runtime / "memory"
    return {
        "root": root,
        "runtime": runtime,
        "venv": runtime / "runtime" / "venv",
        "memory": memory,
        "logs": memory / "logs",
        "db": memory / "memory.sqlite3",
    }


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def in_virtual_environment() -> bool:
    return sys.prefix != sys.base_prefix


def expected_virtual_environment(root: Path) -> bool:
    expected = runtime_paths(root)["venv"]
    try:
        return Path(sys.prefix).resolve() == expected.resolve()
    except OSError:
        return False


def ensure_runtime_environment(root: Path) -> None:
    if sys.version_info < MIN_PYTHON:
        raise MemoryEngineError("Python 3.11 or newer is required.", 3)
    if not in_virtual_environment() or not expected_virtual_environment(root):
        raise MemoryEngineError(
            "Run memory through .ai/tools/memory.cmd on Windows or .ai/tools/memory.sh on macOS/Linux.",
            3,
            {"expected_venv": str(runtime_paths(root)["venv"].relative_to(root))},
        )


def sqlite_has_fts5() -> bool:
    try:
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE VIRTUAL TABLE fts_probe USING fts5(content)")
        conn.close()
        return True
    except sqlite3.Error:
        return False


def connect_database(root: Path, create_parent: bool = True) -> sqlite3.Connection:
    paths = runtime_paths(root)
    if create_parent:
        paths["memory"].mkdir(parents=True, exist_ok=True)
        paths["logs"].mkdir(parents=True, exist_ok=True)
    if not sqlite_has_fts5():
        raise MemoryEngineError("This Python SQLite build does not support FTS5.", 3)
    conn = sqlite3.connect(paths["db"], timeout=5.0)
    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout = 5000")
        conn.execute("PRAGMA foreign_keys = ON")
        for attempt in range(8):
            try:
                mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
                if str(mode).casefold() != "wal":
                    conn.execute("PRAGMA journal_mode = WAL")
                break
            except sqlite3.OperationalError as exc:
                if "locked" not in str(exc).casefold() or attempt == 7:
                    raise
                time.sleep(min(0.05 * (2**attempt), 0.5))
        return conn
    except Exception:
        conn.close()
        raise


def initialize_schema(conn: sqlite3.Connection) -> None:
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    if version not in (0, SCHEMA_VERSION):
        raise MemoryEngineError(
            f"Unsupported memory schema version {version}; expected {SCHEMA_VERSION}.", 5
        )
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            kind TEXT NOT NULL,
            tags TEXT NOT NULL,
            related_paths TEXT NOT NULL,
            evidence TEXT NOT NULL,
            sources TEXT NOT NULL,
            platform TEXT,
            task_ref TEXT,
            created_at TEXT NOT NULL,
            source_path TEXT NOT NULL UNIQUE,
            approx_tokens INTEGER NOT NULL,
            content_hash TEXT NOT NULL UNIQUE
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
            title,
            summary,
            tags,
            related_paths,
            content='chunks',
            content_rowid='rowid',
            tokenize='unicode61'
        );

        CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
            INSERT INTO chunks_fts(rowid, title, summary, tags, related_paths)
            VALUES (new.rowid, new.title, new.summary, new.tags, new.related_paths);
        END;

        CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
            INSERT INTO chunks_fts(chunks_fts, rowid, title, summary, tags, related_paths)
            VALUES ('delete', old.rowid, old.title, old.summary, old.tags, old.related_paths);
        END;

        CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
            INSERT INTO chunks_fts(chunks_fts, rowid, title, summary, tags, related_paths)
            VALUES ('delete', old.rowid, old.title, old.summary, old.tags, old.related_paths);
            INSERT INTO chunks_fts(rowid, title, summary, tags, related_paths)
            VALUES (new.rowid, new.title, new.summary, new.tags, new.related_paths);
        END;
        """
    )
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    conn.commit()


def approximate_tokens(text: str) -> int:
    return len(WORD_RE.findall(text))


def normalize_string_list(value: Any, field: str, maximum: int = 30) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise MemoryEngineError(f"{field} must be an array of strings.", 2)
    cleaned = []
    seen = set()
    for item in value:
        item = " ".join(item.strip().split())
        if item and item.casefold() not in seen:
            cleaned.append(item)
            seen.add(item.casefold())
    if len(cleaned) > maximum:
        raise MemoryEngineError(f"{field} may contain at most {maximum} entries.", 2)
    return cleaned


def secret_rule(text: str) -> str | None:
    for name, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            return name
    return None


def validate_record(raw: Any, scan_secrets: bool = True) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise MemoryEngineError("Memory input must be a JSON object.", 2)
    if raw.get("schema_version", 1) != 1:
        raise MemoryEngineError("Memory input schema_version must be 1.", 2)
    title = " ".join(str(raw.get("title", "")).strip().split())
    summary = str(raw.get("summary", "")).strip()
    kind = str(raw.get("kind", "")).strip().lower()
    evidence = str(raw.get("evidence", "Unclear")).strip()
    if not title or len(title) > 200:
        raise MemoryEngineError("title is required and must not exceed 200 characters.", 2)
    if not summary:
        raise MemoryEngineError("summary is required.", 2)
    tokens = approximate_tokens(summary)
    if tokens > MAX_CHUNK_TOKENS:
        raise MemoryEngineError(
            f"summary is approximately {tokens} tokens; the maximum is {MAX_CHUNK_TOKENS}.", 2
        )
    if kind not in ALLOWED_KINDS:
        raise MemoryEngineError(f"kind must be one of: {', '.join(sorted(ALLOWED_KINDS))}.", 2)
    if evidence not in ALLOWED_EVIDENCE:
        raise MemoryEngineError(f"evidence must be one of: {', '.join(sorted(ALLOWED_EVIDENCE))}.", 2)
    tags = normalize_string_list(raw.get("tags"), "tags")
    related_paths = normalize_string_list(raw.get("related_paths"), "related_paths")
    sources = normalize_string_list(raw.get("sources"), "sources")
    platform = str(raw.get("platform", "")).strip() or None
    task_ref = str(raw.get("task_ref", "")).strip() or None
    combined = "\n".join([title, summary, *tags, *related_paths, *sources])
    if scan_secrets:
        rule = secret_rule(combined)
        if rule:
            raise MemoryEngineError(
                "Memory write rejected because the proposed record resembles sensitive credential material.",
                4,
                {"rule": rule, "stored": 0},
            )
    normalized = {
        "schema_version": 1,
        "title": title,
        "summary": summary,
        "kind": kind,
        "tags": tags,
        "related_paths": related_paths,
        "evidence": evidence,
        "sources": sources,
        "platform": platform,
        "task_ref": task_ref,
        "approx_tokens": tokens,
    }
    digest_input = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    normalized["content_hash"] = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
    return normalized


def markdown_for_record(record: dict[str, Any]) -> str:
    metadata = {key: value for key, value in record.items() if key != "summary"}
    return (
        "<!-- agent-rails-memory\n"
        + json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n-->\n\n# "
        + record["title"]
        + "\n\n"
        + record["summary"].rstrip()
        + "\n"
    )


def parse_markdown(path: Path, root: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    prefix = "<!-- agent-rails-memory\n"
    if not text.startswith(prefix) or "\n-->\n" not in text:
        raise MemoryEngineError("Missing Agent Rails memory metadata block.", 2)
    raw_metadata, body = text[len(prefix):].split("\n-->\n", 1)
    try:
        metadata = json.loads(raw_metadata)
    except json.JSONDecodeError as exc:
        raise MemoryEngineError(f"Invalid memory metadata JSON: {exc.msg}.", 2) from exc
    body = body.lstrip("\n")
    if not body.startswith("# ") or "\n\n" not in body:
        raise MemoryEngineError("Memory body must contain a level-one title and summary.", 2)
    title_line, summary = body.split("\n\n", 1)
    metadata["title"] = title_line[2:].strip()
    metadata["summary"] = summary.strip()
    validated = validate_record(metadata)
    validated.update(
        {
            "id": str(metadata.get("id", "")).strip(),
            "created_at": str(metadata.get("created_at", "")).strip(),
            "source_path": path.resolve().relative_to(root.resolve()).as_posix(),
        }
    )
    if not validated["id"] or not validated["created_at"]:
        raise MemoryEngineError("Memory metadata requires id and created_at.", 2)
    return validated


def database_values(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record["id"], record["title"], record["summary"], record["kind"],
        json.dumps(record["tags"], ensure_ascii=False),
        json.dumps(record["related_paths"], ensure_ascii=False),
        record["evidence"], json.dumps(record["sources"], ensure_ascii=False),
        record.get("platform"), record.get("task_ref"), record["created_at"],
        record["source_path"], record["approx_tokens"], record["content_hash"],
    )


INSERT_SQL = """
INSERT INTO chunks (
    id, title, summary, kind, tags, related_paths, evidence, sources,
    platform, task_ref, created_at, source_path, approx_tokens, content_hash
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def init_store(root: Path) -> dict[str, Any]:
    conn = connect_database(root)
    initialize_schema(conn)
    count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()
    return {
        "ok": True,
        "command": "init",
        "schema_version": SCHEMA_VERSION,
        "chunks": count,
        "store": runtime_paths(root)["memory"].relative_to(root).as_posix(),
    }


def add_record(root: Path, raw: Any) -> dict[str, Any]:
    record = validate_record(raw)
    conn = connect_database(root)
    initialize_schema(conn)
    duplicate = conn.execute(
        "SELECT id, source_path FROM chunks WHERE content_hash = ?", (record["content_hash"],)
    ).fetchone()
    if duplicate:
        conn.close()
        return {
            "ok": True,
            "command": "add",
            "status": "duplicate",
            "stored": 0,
            "id": duplicate["id"],
            "source": duplicate["source_path"],
            "indicator": f'[agent-rails-memory: Active | Stored 0 | Duplicate "{duplicate["source_path"]}"]',
        }
    now = datetime.now(timezone.utc)
    chunk_id = uuid.uuid4().hex[:12]
    created_at = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    log_dir = runtime_paths(root)["logs"] / now.strftime("%Y") / now.strftime("%m")
    log_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{chunk_id}.md"
    final_path = log_dir / filename
    record.update(
        {
            "id": chunk_id,
            "created_at": created_at,
            "source_path": final_path.relative_to(root).as_posix(),
        }
    )
    fd, temp_name = tempfile.mkstemp(prefix=".memory-", suffix=".tmp", dir=log_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(markdown_for_record(record))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, final_path)
        try:
            conn.execute(INSERT_SQL, database_values(record))
            conn.commit()
        except Exception:
            final_path.unlink(missing_ok=True)
            raise
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
        conn.close()
    warning = None
    if record["approx_tokens"] < 150:
        warning = "Summary is below the 150-token target but was retained as a concise durable memory."
    result = {
        "ok": True,
        "command": "add",
        "status": "stored",
        "stored": 1,
        "id": chunk_id,
        "source": record["source_path"],
        "approx_tokens": record["approx_tokens"],
        "indicator": f'[agent-rails-memory: Active | Stored 1 | Source "{record["source_path"]}"]',
    }
    if warning:
        result["warning"] = warning
    return result


def query_terms(query: str) -> list[str]:
    terms = []
    seen = set()
    for token in TOKEN_RE.findall(query.casefold()):
        token = token.strip("./\\:-_")
        if len(token) < 2 or token in STOP_WORDS or token in seen:
            continue
        seen.add(token)
        terms.append(token)
    return terms[:24]


def fts_expression(terms: Iterable[str]) -> str:
    quoted = []
    for term in terms:
        safe = term.replace('"', '""')
        quoted.append(f'"{safe}"')
    return " OR ".join(quoted)


def parse_created_at(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.fromtimestamp(0, timezone.utc)


def rank_candidates(rows: list[sqlite3.Row], terms: list[str]) -> list[dict[str, Any]]:
    ranked = []
    total = max(len(rows), 1)
    now = datetime.now(timezone.utc)
    for index, row in enumerate(rows):
        title = row["title"]
        summary = row["summary"]
        tags = json.loads(row["tags"])
        related_paths = json.loads(row["related_paths"])
        searchable = " ".join([title, summary, *tags, *related_paths]).casefold()
        matched = sum(1 for term in terms if term in searchable)
        coverage = matched / max(len(terms), 1)
        rank_score = (total - index) / total
        metadata_text = " ".join([*tags, *related_paths]).casefold()
        metadata_signal = 1.0 if any(term in metadata_text for term in terms) else 0.0
        age_days = max((now - parse_created_at(row["created_at"])).total_seconds() / 86400, 0.0)
        recency = math.pow(0.5, age_days / 180.0)
        score = 0.70 * coverage + 0.20 * rank_score + 0.05 * metadata_signal + 0.05 * recency
        ranked.append(
            {
                "id": row["id"],
                "title": title,
                "summary": summary,
                "kind": row["kind"],
                "tags": tags,
                "related_paths": related_paths,
                "evidence": row["evidence"],
                "sources": json.loads(row["sources"]),
                "created_at": row["created_at"],
                "source": row["source_path"],
                "approx_tokens": row["approx_tokens"],
                "bm25": row["bm25"],
                "score": round(score, 6),
            }
        )
    return sorted(ranked, key=lambda item: (-item["score"], item["source"]))


def search_records(root: Path, query: str, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
    if limit < 1 or limit > 10:
        raise MemoryEngineError("limit must be between 1 and 10.", 2)
    paths = runtime_paths(root)
    if not paths["db"].exists():
        return {
            "ok": True, "command": "search", "query": query, "corpus_count": 0,
            "candidate_count": 0, "retrieved_count": 0, "confidence": "none",
            "results": [], "native_fallback_allowed": True,
            "indicator": "[agent-rails-memory: Active | Searched 0 chunks | Retrieved 0 | Native fallback: Allowed (local store empty)]",
        }
    conn = connect_database(root)
    initialize_schema(conn)
    corpus_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    terms = query_terms(query)
    rows: list[sqlite3.Row] = []
    if terms:
        rows = conn.execute(
            """
            SELECT c.*, bm25(chunks_fts) AS bm25
            FROM chunks_fts
            JOIN chunks AS c ON c.rowid = chunks_fts.rowid
            WHERE chunks_fts MATCH ?
            ORDER BY bm25
            LIMIT ?
            """,
            (fts_expression(terms), MAX_CANDIDATES),
        ).fetchall()
    conn.close()
    ranked = rank_candidates(rows, terms)
    selected = []
    token_total = 0
    for item in ranked:
        if len(selected) >= limit:
            break
        if selected and token_total + item["approx_tokens"] > MAX_RETRIEVED_TOKENS:
            continue
        selected.append(item)
        token_total += item["approx_tokens"]
    top_score = selected[0]["score"] if selected else 0.0
    confidence = "high" if top_score >= CONFIDENCE_THRESHOLD else ("low" if selected else "none")
    fallback = confidence != "high"
    source_text = ", ".join(f'"{item["source"]}"' for item in selected)
    indicator = f"[agent-rails-memory: Active | Searched {corpus_count} chunks | Retrieved {len(selected)}"
    if source_text:
        indicator += f" | Sources {source_text}"
    if fallback:
        reason = "local confidence low" if selected else "no local results"
        indicator += f" | Native fallback: Allowed ({reason})"
    indicator += "]"
    return {
        "ok": True,
        "command": "search",
        "query": query,
        "corpus_count": corpus_count,
        "candidate_count": len(rows),
        "retrieved_count": len(selected),
        "retrieved_tokens": token_total,
        "confidence": confidence,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "native_fallback_allowed": fallback,
        "results": selected,
        "indicator": indicator,
    }


def status_store(root: Path) -> dict[str, Any]:
    paths = runtime_paths(root)
    if not paths["db"].exists():
        return {
            "ok": True, "command": "status", "initialized": False, "chunks": 0,
            "schema_version": None, "store": paths["memory"].relative_to(root).as_posix(),
        }
    conn = connect_database(root, create_parent=False)
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0] if version else 0
    conn.close()
    return {
        "ok": True, "command": "status", "initialized": bool(version), "chunks": chunks,
        "schema_version": version, "store": paths["memory"].relative_to(root).as_posix(),
    }


def reindex_store(root: Path) -> dict[str, Any]:
    paths = runtime_paths(root)
    recovered_backup = None
    try:
        conn = connect_database(root)
        initialize_schema(conn)
    except sqlite3.DatabaseError:
        try:
            conn.close()
        except (NameError, sqlite3.Error):
            pass
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        if paths["db"].exists():
            backup = paths["db"].with_name(f"memory.sqlite3.corrupt-{timestamp}")
            os.replace(paths["db"], backup)
            recovered_backup = backup.relative_to(root).as_posix()
        for suffix in ("-wal", "-shm"):
            Path(str(paths["db"]) + suffix).unlink(missing_ok=True)
        conn = connect_database(root)
        initialize_schema(conn)
    conn.execute("DELETE FROM chunks")
    conn.commit()
    indexed = 0
    errors = []
    for path in sorted(runtime_paths(root)["logs"].rglob("*.md")):
        try:
            record = parse_markdown(path, root)
            conn.execute(INSERT_SQL, database_values(record))
            indexed += 1
        except (MemoryEngineError, sqlite3.Error) as exc:
            errors.append({"source": path.relative_to(root).as_posix(), "error": str(exc)})
    conn.commit()
    conn.close()
    return {
        "ok": not errors,
        "command": "reindex",
        "indexed": indexed,
        "invalid": len(errors),
        "errors": errors,
        "recovered_backup": recovered_backup,
        "indicator": f"[agent-rails-memory: Active | Reindexed {indexed} chunks | Invalid {len(errors)}]",
    }


def parse_date_boundary(value: str, end_of_day: bool = False) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise MemoryEngineError("Date filters must use ISO-8601 format.", 2) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    if end_of_day and len(value) == 10:
        parsed = parsed.replace(hour=23, minute=59, second=59)
    return parsed.astimezone(timezone.utc)


def forget_records(
    root: Path,
    chunk_id: str | None,
    source: str | None,
    before: str | None,
    after: str | None,
    all_records: bool,
    confirmed: bool,
) -> dict[str, Any]:
    if not confirmed:
        raise MemoryEngineError("forget requires --confirm.", 2)
    if not any([chunk_id, source, before, after, all_records]):
        raise MemoryEngineError("forget requires an id, source, date range, or --all.", 2)
    conn = connect_database(root)
    initialize_schema(conn)
    rows = conn.execute("SELECT id, source_path, created_at FROM chunks").fetchall()
    before_dt = parse_date_boundary(before, end_of_day=True) if before else None
    after_dt = parse_date_boundary(after) if after else None
    selected = []
    for row in rows:
        created = parse_created_at(row["created_at"])
        matches = all_records
        matches = matches or bool(chunk_id and row["id"] == chunk_id)
        matches = matches or bool(source and row["source_path"] == source.replace("\\", "/"))
        if before_dt or after_dt:
            in_range = (before_dt is None or created <= before_dt) and (after_dt is None or created >= after_dt)
            matches = matches or in_range
        if matches:
            selected.append(row)
    file_errors = []
    with conn:
        for row in selected:
            conn.execute("DELETE FROM chunks WHERE id = ?", (row["id"],))
    conn.close()
    for row in selected:
        path = root / row["source_path"]
        try:
            path.unlink(missing_ok=True)
        except OSError:
            file_errors.append(row["source_path"])
    return {
        "ok": not file_errors,
        "command": "forget",
        "forgotten": len(selected),
        "file_errors": file_errors,
        "indicator": f"[agent-rails-memory: Active | Forgotten {len(selected)} chunks]",
    }


def doctor(root: Path) -> dict[str, Any]:
    paths = runtime_paths(root)
    checks = {
        "python_version": {
            "ok": sys.version_info >= MIN_PYTHON,
            "value": ".".join(map(str, sys.version_info[:3])),
            "remediation": "Install Python 3.11 or newer." if sys.version_info < MIN_PYTHON else None,
        },
        "virtual_environment": {
            "ok": in_virtual_environment() and expected_virtual_environment(root),
            "value": str(Path(sys.prefix)),
            "remediation": "Run .ai/tools/memory.cmd or .ai/tools/memory.sh." if not expected_virtual_environment(root) else None,
        },
        "sqlite_fts5": {
            "ok": sqlite_has_fts5(),
            "value": sqlite3.sqlite_version,
            "remediation": "Install a Python 3.11+ build whose sqlite3 module includes FTS5." if not sqlite_has_fts5() else None,
        },
        "store_parent_writable": {
            "ok": os.access(root, os.W_OK),
            "value": paths["memory"].relative_to(root).as_posix(),
            "remediation": "Grant the current user write access to the repository." if not os.access(root, os.W_OK) else None,
        },
    }
    try:
        store_status = status_store(root)
        checks["schema"] = {
            "ok": not store_status["initialized"] or store_status["schema_version"] == SCHEMA_VERSION,
            "value": store_status["schema_version"],
            "remediation": None,
        }
    except Exception as exc:
        checks["schema"] = {"ok": False, "value": None, "remediation": str(exc)}
    return {
        "ok": all(check["ok"] for check in checks.values()),
        "command": "doctor",
        "python_executable": sys.executable,
        "checks": checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent Rails local SQLite memory engine")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Initialize the local memory store.")
    add = subparsers.add_parser("add", help="Add one structured memory record.")
    add.add_argument("--stdin", action="store_true", required=True, help="Read JSON from standard input.")
    search = subparsers.add_parser("search", help="Search local memory first.")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    subparsers.add_parser("reindex", help="Rebuild SQLite from Markdown records.")
    subparsers.add_parser("status", help="Report local memory status.")
    subparsers.add_parser("doctor", help="Validate runtime and store prerequisites.")
    forget = subparsers.add_parser("forget", help="Explicitly remove memory records.")
    forget.add_argument("--id", dest="chunk_id")
    forget.add_argument("--source")
    forget.add_argument("--before")
    forget.add_argument("--after")
    forget.add_argument("--all", action="store_true", dest="all_records")
    forget.add_argument("--confirm", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    root = repo_root_from_script()
    try:
        ensure_runtime_environment(root)
        args = build_parser().parse_args(argv)
        if args.command == "init":
            result = init_store(root)
        elif args.command == "add":
            try:
                raw = json.load(sys.stdin)
            except json.JSONDecodeError as exc:
                raise MemoryEngineError(f"Invalid JSON input: {exc.msg}.", 2) from exc
            result = add_record(root, raw)
        elif args.command == "search":
            result = search_records(root, args.query, args.limit)
        elif args.command == "reindex":
            result = reindex_store(root)
        elif args.command == "status":
            result = status_store(root)
        elif args.command == "doctor":
            result = doctor(root)
        elif args.command == "forget":
            result = forget_records(
                root, args.chunk_id, args.source, args.before, args.after,
                args.all_records, args.confirm,
            )
        else:
            raise MemoryEngineError("Unknown command.", 2)
        json_print(result)
        return 0 if result.get("ok", False) else 5
    except MemoryEngineError as exc:
        payload = {"ok": False, "error": str(exc), **exc.details}
        if exc.code == 4:
            payload["indicator"] = "[agent-rails-memory: Active | Write rejected | Stored 0]"
        elif exc.code in (3, 5):
            payload["indicator"] = f"[agent-rails-memory: Error | {str(exc)}]"
        json_print(payload)
        return exc.code
    except (OSError, sqlite3.Error) as exc:
        json_print(
            {
                "ok": False,
                "error": f"Memory storage failure: {exc}",
                "indicator": "[agent-rails-memory: Error | Local storage unavailable]",
            }
        )
        return 5


if __name__ == "__main__":
    sys.exit(main())
