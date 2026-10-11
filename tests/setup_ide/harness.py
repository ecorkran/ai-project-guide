"""Black-box harness for scripts/setup-ide.

Builds a throwaway guide and project, runs setup-ide as a subprocess, and turns
the result into a snapshot text block. Nothing here imports setup-ide code, so
the same suite checks the bash version and its Python replacement.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Union

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_GUIDE = Path(__file__).resolve().parent / "fixture_guide"

BASH = "/bin/bash"
SYSTEM_PATH = "/usr/bin:/bin"

# Paths setup-ide writes or prunes (INSTALL_PATHS and LINT_WRITE_PATHS in the
# script). The snapshot lists every file under these, including files the
# project created itself, so "left alone" is visible too.
INSTALL_PATHS = (
    "CLAUDE.md",
    "CLAUDE.md.pre-context-forge",
    "AGENTS.md",
    "AGENTS.md.pre-context-forge",
    ".claude",
    ".cursor",
    ".github",
    ".agents",
    ".context-forge",
    "ruff.toml",
    "analysis_options.yaml",
    "eslint.config.mjs",
    ".editorconfig",
    "Directory.Build.props",
)

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
NO_FINAL_NEWLINE = "<no final newline>"

FileContent = Union[str, bytes]


@dataclass
class RunResult:
    """One setup-ide invocation: raw output plus what normalization needs."""

    args: tuple[str, ...]
    code: int
    stdout: str
    stderr: str
    guide: Path


def make_guide(dest: Path, guides: Path = FIXTURE_GUIDE) -> Path:
    """Copy the repo's scripts/ and a project-guides tree into dest.

    `guides` is the fixture guide by default; the smoke test passes the real
    project-guides/ instead.
    """
    ignore = shutil.ignore_patterns("__pycache__")
    shutil.copytree(REPO_ROOT / "scripts", dest / "scripts", ignore=ignore)
    shutil.copytree(guides, dest / "project-guides", ignore=ignore)
    return dest


def make_project(tmp_path: Path, guides: Path = FIXTURE_GUIDE) -> tuple[Path, Path]:
    """Create <tmp>/project with the guide at project-documents/ai-project-guide."""
    project = tmp_path / "project"
    guide = project / "project-documents" / "ai-project-guide"
    guide.mkdir(parents=True)
    make_guide(guide, guides)
    return project, guide


def write_files(root: Path, files: dict[str, FileContent]) -> None:
    """Write {relpath: content} under root. bytes content is written as is."""
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode() if isinstance(content, str) else content
        path.write_bytes(data)


def stub_dir(guide: Path) -> Path:
    """Directory placed first on PATH; tests drop a stub `cf` here."""
    path = guide / ".stubs"
    path.mkdir(exist_ok=True)
    return path


def run(
    guide: Path,
    args: Sequence[str],
    cwd: Path,
    env_extra: dict[str, str] | None = None,
) -> RunResult:
    """Run `bash <guide>/scripts/setup-ide *args` in a fixed, minimal environment."""
    stubs = stub_dir(guide)
    home = stubs / "home"
    home.mkdir(exist_ok=True)
    env = {
        "PATH": f"{stubs}:{SYSTEM_PATH}",
        "LC_ALL": "C",
        "HOME": str(home),
    }
    env.update(env_extra or {})
    proc = subprocess.run(
        [BASH, str(guide / "scripts" / "setup-ide"), *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    return RunResult(tuple(args), proc.returncode, proc.stdout, proc.stderr, guide)


def _path_variants(path: Path) -> list[str]:
    """The path as given, resolved, and with macOS's /private prefix added or
    removed, longest first so nested paths are replaced before their parents."""
    variants = {str(path), str(path.resolve())}
    for text in list(variants):
        if text.startswith("/private/"):
            variants.add(text[len("/private") :])
        else:
            variants.add("/private" + text)
    return sorted(variants, key=len, reverse=True)


def _temp_bases() -> list[str]:
    bases = {tempfile.gettempdir(), str(Path(tempfile.gettempdir()).resolve())}
    bases.update({"/tmp", "/private/tmp", "/var/folders", "/private/var/folders"})
    return sorted(bases, key=len, reverse=True)


def normalize(text: str, root: Path, guide: Path) -> str:
    """Strip ANSI codes; replace the guide, project root and other temp paths."""
    text = ANSI_RE.sub("", text)
    for variant in _path_variants(guide):
        text = text.replace(variant, "<GUIDE>")
    for variant in _path_variants(root):
        text = text.replace(variant, "<ROOT>")
    for base in _temp_bases():
        text = re.sub(re.escape(base) + r"[^\s'\"):,]*", "<TMP>", text)
    return text


def _render_file(path: Path) -> str:
    """File contents as UTF-8 text with CR shown as \\r, flagging a missing
    final newline so it shows up in diffs."""
    text = path.read_bytes().decode("utf-8").replace("\r", "\\r")
    if text and not text.endswith("\n"):
        text += "\n" + NO_FINAL_NEWLINE + "\n"
    return text


def _install_entries(root: Path) -> list[tuple[str, Path | None]]:
    """(relative path, file or None for an empty directory), sorted by path."""
    entries: dict[str, Path | None] = {}
    for name in INSTALL_PATHS:
        top = root / name
        if top.is_file():
            entries[name] = top
        elif top.is_dir():
            if not any(top.iterdir()):
                entries[name + "/"] = None
            for path in top.rglob("*"):
                rel = path.relative_to(root).as_posix()
                if path.is_file():
                    entries[rel] = path
                elif path.is_dir() and not any(path.iterdir()):
                    entries[rel + "/"] = None
    return sorted(entries.items())


def install_files(project_root: Path) -> dict[str, bytes]:
    """Content of every file under the install paths, keyed by relative path."""
    return {
        rel: path.read_bytes()
        for rel, path in _install_entries(project_root)
        if path is not None
    }


def snapshot(project_root: Path, runs: Sequence[RunResult]) -> str:
    """Snapshot text: every run (label, exit code, output), then install files."""
    out: list[str] = []
    for number, result in enumerate(runs, start=1):
        label = normalize(
            " ".join(("setup-ide", *result.args)), project_root, result.guide
        )
        out.append(f"== run {number}: {label}")
        out.append(f"exit: {result.code}")
        for stream, text in (("stdout", result.stdout), ("stderr", result.stderr)):
            out.append(f"-- {stream}")
            body = normalize(text, project_root, result.guide)
            if body:
                out.append(body.rstrip("\n"))
    out.append("== files")
    for rel, path in _install_entries(project_root):
        if path is None:
            out.append(f"--- {rel} (empty directory)")
            continue
        out.append(f"--- {rel}")
        out.append(_render_file(path).rstrip("\n"))
    return "\n".join(out) + "\n"


def tree(root: Path) -> dict[str, bytes]:
    """Every file and empty directory under root, for before/after asserts."""
    result: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_file():
            result[rel] = path.read_bytes()
        elif path.is_dir() and not any(path.iterdir()):
            result[rel + "/"] = b""
    return result
