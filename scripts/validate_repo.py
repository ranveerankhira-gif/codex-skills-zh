#!/usr/bin/env python3
"""Validate public repository structure, metadata, privacy, and invocation policy."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
HIGH = {
    "ai-output-renamer", "conversation-handoff", "main-account-takeover", "cross-device-project-sync",
    "diannao-kongzhi", "zhuomian-zhengli", "windows-storage-cleanup", "dryad-data-fetcher",
    "resource-fetcher-router", "web-tool-router", "framepack-video", "video-project-library-maintainer",
    "codex-task-renamer", "wechat-cli", "wechat-intelligence-hub",
}
REQUIRED_ROOT = {"README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "catalog.json"}
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "OpenAI key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
}
RUNTIME_STATE_NAMES = {"state", "__pycache__", ".pytest_cache", "logs", "cache"}
RUNTIME_FILE_NAMES = {"write.lock", ".rename-in-progress.json"}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED_ROOT:
        if not (ROOT / name).is_file():
            fail(f"missing root file: {name}", errors)
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    rows = catalog.get("skills") or []
    names = [row.get("name") for row in rows]
    directories = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    if not rows or len(set(names)) != len(rows):
        fail("catalog must contain at least one Skill and all names must be unique", errors)
    if sorted(names) != directories:
        fail("catalog and skills directory differ", errors)
    required_fields = {"name", "display_name_zh", "purpose_zh", "release", "platforms", "risk_level", "permissions", "dependencies", "invocation_policy", "license", "version", "archive_sha256"}
    for row in rows:
        name = row.get("name")
        if set(row) != required_fields:
            fail(f"catalog fields differ for {name}", errors)
        root = ROOT / "skills" / str(name)
        skill_md = root / "SKILL.md"
        yaml = root / "agents" / "openai.yaml"
        if not skill_md.is_file() or not yaml.is_file():
            fail(f"missing SKILL.md or agents/openai.yaml: {name}", errors)
            continue
        skill_text = skill_md.read_text(encoding="utf-8")
        if not skill_text.startswith("---\n") or not re.search(rf"(?m)^name:\s*[\"']?{re.escape(str(name))}[\"']?\s*$", skill_text):
            fail(f"frontmatter name mismatch: {name}", errors)
        yaml_text = yaml.read_text(encoding="utf-8")
        if name in HIGH:
            if "allow_implicit_invocation: false" not in yaml_text:
                fail(f"high-permission skill is not explicit-only: {name}", errors)
            security = root / "references" / "security-and-permissions.md"
            if not security.is_file() or "security-and-permissions.md" not in skill_text:
                fail(f"missing linked permission disclosure: {name}", errors)
        for path in root.rglob("*"):
            relative_parts = path.relative_to(root).parts
            if any(part.casefold() in RUNTIME_STATE_NAMES for part in relative_parts):
                fail(f"runtime state directory is not allowed: {path.relative_to(ROOT)}", errors)
                continue
            if path.name.casefold() in RUNTIME_FILE_NAMES:
                fail(f"runtime state file is not allowed: {path.relative_to(ROOT)}", errors)
            if path.is_symlink():
                fail(f"symlink is not allowed: {path.relative_to(ROOT)}", errors)
            if path.is_file():
                if path.suffix.lower() in {".pyc", ".pyo"} or "__pycache__" in path.parts:
                    fail(f"compiled cache is not allowed: {path.relative_to(ROOT)}", errors)
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    fail(f"file is not UTF-8 text: {path.relative_to(ROOT)}", errors)
                    continue
                for line_number, line in enumerate(text.splitlines(), 1):
                    if "PUBLICATION-SECRET-FIXTURE" in line:
                        continue
                    for label, pattern in SECRET_PATTERNS.items():
                        if pattern.search(line):
                            fail(f"{label} pattern in {path.relative_to(ROOT)}:{line_number}", errors)

    denylist_path = os.environ.get("PUBLICATION_DENYLIST_FILE")
    if denylist_path:
        terms = [line.strip() for line in Path(denylist_path).read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.name == "catalog.json" and False:
                continue
            try:
                folded = path.read_text(encoding="utf-8").casefold()
            except (UnicodeDecodeError, OSError):
                continue
            for term in terms:
                if term.casefold() in folded:
                    fail(f"external denylist term found in {path.relative_to(ROOT)}", errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    high_count = sum(name in HIGH for name in names)
    print(f"PASS: {len(rows)} skills, {high_count} explicit-only high-permission skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

