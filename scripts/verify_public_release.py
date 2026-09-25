#!/usr/bin/env python3
"""Validate that this fresh-history toolkit stays generic and synthetic."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

SKILL_NAME = "build-governed-webex-assistant"
IGNORED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
}
BLOCKED_SUFFIXES = {
    ".db",
    ".gz",
    ".key",
    ".log",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".tgz",
    ".zip",
}
TEXT_SUFFIXES = {
    "",
    ".example",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
ALLOWED_URL_HOSTS = {"developer.webex.com", "example.invalid", "www.apache.org"}
ALLOWED_EMAIL_HOSTS = {"example.com", "example.invalid"}

EMAIL_RE = re.compile(
    r"(?<![\w.+-])([A-Z0-9._%+-]+)@([A-Z0-9.-]+\.[A-Z]{2,})(?![\w.-])", re.IGNORECASE
)
URL_RE = re.compile(r"https?://[^\s<>\])}`\"']+", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [^-]*" + "PRI" + r"VATE KEY-----", re.IGNORECASE),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"(?im)^[ \t]*(?:WEBEX_BOT_TOKEN|WEBEX_WEBHOOK_SECRET)[ \t]*=[ \t]*"
        r"(?:['\"])?([^\s'\"]{12,})(?:['\"])?\s*$"
    ),
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    message: str

    def render(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root)
        except ValueError:
            display = self.path
        return f"{display}:{self.line}: {self.message}"


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() or path.is_symlink():
            files.append(path)
    return sorted(files)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def scan_text(
    path: Path, text: str, external_denylist: tuple[str, ...] = ()
) -> list[Finding]:
    findings: list[Finding] = []
    lowered = text.casefold()

    for fragment in external_denylist:
        start = 0
        while True:
            offset = lowered.find(fragment.casefold(), start)
            if offset < 0:
                break
            findings.append(
                Finding(
                    path,
                    line_number(text, offset),
                    "marker from external denylist detected",
                )
            )
            start = offset + len(fragment)

    local_markers = (
        "/" + "Users" + "/",
        "C:" + "\\Users\\",
    )
    for marker in local_markers:
        offset = text.find(marker)
        if offset >= 0:
            findings.append(
                Finding(
                    path,
                    line_number(text, offset),
                    "absolute user path is not public-safe",
                )
            )

    for match in EMAIL_RE.finditer(text):
        host = match.group(2).lower()
        if host not in ALLOWED_EMAIL_HOSTS:
            findings.append(
                Finding(
                    path,
                    line_number(text, match.start()),
                    f"non-example email address: {match.group(0)!r}",
                )
            )

    for match in URL_RE.finditer(text):
        raw_url = match.group(0).rstrip(".,;:")
        host = (urlparse(raw_url).hostname or "").lower()
        if host not in ALLOWED_URL_HOSTS:
            findings.append(
                Finding(
                    path,
                    line_number(text, match.start()),
                    f"URL host is not allowlisted: {host or raw_url!r}",
                )
            )

    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                Finding(
                    path,
                    line_number(text, match.start()),
                    "credential-like value detected",
                )
            )

    return findings


def scan_files(
    root: Path, external_denylist: tuple[str, ...] = ()
) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    scanned = 0

    for path in iter_files(root):
        scanned += 1
        relative = path.relative_to(root)

        if path.is_symlink():
            findings.append(
                Finding(
                    path, 1, "symbolic links are not allowed in the release candidate"
                )
            )
            continue
        if path.name == ".DS_Store":
            findings.append(
                Finding(path, 1, "operating-system metadata is not allowed")
            )
        if path.name == ".env" or path.suffix.lower() in BLOCKED_SUFFIXES:
            findings.append(
                Finding(
                    path,
                    1,
                    "runtime, credential, database, log, or archive artifact is not allowed",
                )
            )
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            "Makefile",
            "VERSION",
        }:
            findings.append(
                Finding(
                    path,
                    1,
                    f"unreviewed binary or file type: {path.suffix or path.name!r}",
                )
            )
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding(path, 1, "file is not valid UTF-8 text"))
            continue

        findings.extend(scan_text(path, text, external_denylist))
        if (
            relative.parts
            and relative.parts[0] == ".github"
            and "self-hosted" in text.lower()
        ):
            findings.append(
                Finding(
                    path, 1, "workflow must use a generally available hosted runner"
                )
            )

    return findings, scanned


def validate_json_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*.json")):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            findings.append(
                Finding(path, getattr(exc, "lineno", 1), f"invalid JSON: {exc}")
            )
            continue

        if path.name != "sample-records.json":
            continue
        records = value.get("records") if isinstance(value, dict) else None
        if not isinstance(records, list) or not records:
            findings.append(Finding(path, 1, "sample records must be a non-empty list"))
            continue
        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                findings.append(Finding(path, 1, f"record {index} is not an object"))
                continue
            record_id = record.get("record_id")
            source_class = record.get("source_class")
            if not isinstance(record_id, str) or not record_id.startswith("synthetic-"):
                findings.append(
                    Finding(path, 1, f"record {index} must use a synthetic identifier")
                )
            if source_class in {"candidate", "restricted-audit"}:
                if (
                    record.get("answerable") is not False
                    or record.get("citable") is not False
                ):
                    findings.append(
                        Finding(
                            path,
                            1,
                            f"record {index} has a non-answerable class but permissive policy",
                        )
                    )
            elif source_class != "synthetic":
                findings.append(
                    Finding(
                        path,
                        1,
                        f"record {index} uses a non-synthetic public example class",
                    )
                )
            canonical_url = record.get("canonical_url")
            if canonical_url:
                host = (urlparse(canonical_url).hostname or "").lower()
                if host not in ALLOWED_URL_HOSTS:
                    findings.append(
                        Finding(
                            path, 1, f"record {index} has a non-example citation host"
                        )
                    )
    return findings


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[Finding]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    findings: list[Finding] = []
    if not lines or lines[0] != "---":
        return {}, [Finding(path, 1, "skill must begin with YAML frontmatter")]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [Finding(path, 1, "skill frontmatter is not closed")]
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            findings.append(Finding(path, 1, f"unsupported frontmatter line: {line!r}"))
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, findings


def validate_skill(root: Path) -> list[Finding]:
    skill = root / "skills" / SKILL_NAME
    entry = skill / "SKILL.md"
    findings: list[Finding] = []
    if not entry.is_file():
        return [Finding(entry, 1, "required skill entrypoint is missing")]

    metadata, frontmatter_findings = parse_frontmatter(entry)
    findings.extend(frontmatter_findings)
    if metadata.get("name") != SKILL_NAME:
        findings.append(Finding(entry, 1, "skill name must match its directory"))
    description = metadata.get("description", "")
    if not 80 <= len(description) <= 500:
        findings.append(
            Finding(
                entry,
                1,
                "skill description must be discriminating and 80-500 characters",
            )
        )
    if "Do not use" not in description:
        findings.append(
            Finding(entry, 1, "skill description must include a near-miss boundary")
        )

    text = entry.read_text(encoding="utf-8")
    for target in re.findall(r"\]\((references/[^)#]+\.md)(?:#[^)]+)?\)", text):
        reference = skill / unquote(target)
        if not reference.is_file():
            findings.append(
                Finding(entry, 1, f"referenced skill file is missing: {target}")
            )

    version = skill / "VERSION"
    if not version.is_file() or not SEMVER_RE.fullmatch(
        version.read_text(encoding="utf-8").strip()
    ):
        findings.append(
            Finding(version, 1, "VERSION must contain semantic version x.y.z")
        )

    agent_file = skill / "agents" / "openai.yaml"
    if not agent_file.is_file():
        findings.append(Finding(agent_file, 1, "skill UI metadata is missing"))
    else:
        agent_text = agent_file.read_text(encoding="utf-8")
        if f"${SKILL_NAME}" not in agent_text:
            findings.append(
                Finding(agent_file, 1, "default prompt must name the skill explicitly")
            )
        match = re.search(
            r'^\s*short_description:\s*"([^"]+)"\s*$', agent_text, re.MULTILINE
        )
        if not match or not 25 <= len(match.group(1)) <= 64:
            findings.append(
                Finding(agent_file, 1, "short description must be 25-64 characters")
            )

    return findings


def validate_markdown_links(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*.md")):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            target = raw_target.split()[0].strip("<>")
            if not target or target.startswith(("#", "mailto:")):
                continue
            if urlparse(target).scheme in {"http", "https"}:
                continue
            decoded = unquote(target.split("#", 1)[0])
            if Path(decoded).is_absolute():
                findings.append(
                    Finding(
                        path,
                        line_number(text, match.start()),
                        "absolute local Markdown link",
                    )
                )
                continue
            resolved = (path.parent / decoded).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                findings.append(
                    Finding(
                        path,
                        line_number(text, match.start()),
                        "Markdown link escapes repository",
                    )
                )
                continue
            if not resolved.exists():
                findings.append(
                    Finding(
                        path,
                        line_number(text, match.start()),
                        f"broken local Markdown link: {target}",
                    )
                )
    return findings


def verify_repository(
    root: Path,
    require_license: bool = False,
    external_denylist: tuple[str, ...] = (),
) -> tuple[list[Finding], int]:
    root = root.resolve()
    findings: list[Finding] = []
    if not root.is_dir():
        return [Finding(root, 1, "repository path is not a directory")], 0
    if require_license and not (root / "LICENSE").is_file():
        findings.append(
            Finding(root / "LICENSE", 1, "approved license is required for publication")
        )

    scan_findings, scanned = scan_files(root, external_denylist)
    findings.extend(scan_findings)
    findings.extend(validate_json_files(root))
    findings.extend(validate_skill(root))
    findings.extend(validate_markdown_links(root))
    return findings, scanned


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--require-license",
        action="store_true",
        help="also require an approved LICENSE file for the final publication gate",
    )
    parser.add_argument(
        "--denylist-file",
        type=Path,
        help="read additional case-insensitive markers from an untracked file outside the repository",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    external_denylist: tuple[str, ...] = ()
    if args.denylist_file:
        denylist_path = args.denylist_file.resolve()
        try:
            denylist_path.relative_to(root)
        except ValueError:
            pass
        else:
            parser.error("--denylist-file must be outside the repository")
        if not denylist_path.is_file():
            parser.error("--denylist-file must name a readable file")
        external_denylist = tuple(
            line.strip()
            for line in denylist_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
        if any(len(marker) < 3 for marker in external_denylist):
            parser.error("denylist markers must contain at least three characters")

    findings, scanned = verify_repository(
        root,
        require_license=args.require_license,
        external_denylist=external_denylist,
    )
    if findings:
        print(
            f"Public-release verification failed with {len(findings)} finding(s):",
            file=sys.stderr,
        )
        for finding in sorted(
            findings, key=lambda item: (str(item.path), item.line, item.message)
        ):
            print(f"- {finding.render(root)}", file=sys.stderr)
        return 1

    print(f"Public-release verification passed: {scanned} files scanned.")
    if not args.require_license:
        print("License gate not requested; use --require-license for a release check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
