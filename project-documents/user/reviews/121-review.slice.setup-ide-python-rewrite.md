---
docType: review
layer: project
reviewType: slice
slice: setup-ide-python-rewrite
targetKind: slice
rulesSource: project
project: ai-project-guide
verdict: CONCERNS
verdictSource: stated
sourceDocument: project-documents/user/slices/121-slice.setup-ide-python-rewrite.md
aiModel: claude-opus-5-5
aiProfile: sdk
status: complete
dateCreated: 20261011
dateUpdated: 20261011
reviewedSha: 82fe724b37a80af2f173783090523c16005489ac
toolsGiven: [read_file, list_files, grep]
toolCallsMade: 6
durationSeconds: 67.6
squadronVersion: 0.21.4
findings:
  - id: F001
    severity: pass
    category: architecture
    summary: "Aligned with the architecture's design goals and cf contract"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md#interfaces-required"
  - id: F002
    severity: pass
    category: scope
    summary: "Scope discipline"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md#technical-scope"
  - id: F003
    severity: concern
    category: error-handling
    summary: "Wrapper sketch breaks when invoked by bare filename"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md:155"
  - id: F004
    severity: concern
    category: error-handling
    summary: "Failure modes for the new process and I/O paths are not enumerated"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md#patterns-and-conventions"
  - id: F005
    severity: concern
    category: integration
    summary: "Manifest sort order differs from bash in user locales, and the suite can't detect it"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md:107"
  - id: F006
    severity: note
    category: documentation
    summary: "The isolated-mode explanation is version-dependent"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md:120"
  - id: F007
    severity: note
    category: integration
    summary: "stdout/stderr interleaving under pipes"
    location: "project-documents/user/slices/121-slice.setup-ide-python-rewrite.md:123"
  - id: F008
    severity: note
    category: architecture
    summary: "Slice 122 is not in the architecture's slice list"
    location: "project-documents/user/architecture/120-arch.guide-tooling.md#anticipated-slices"
  - id: F009
    severity: pass
    category: nfr
    summary: "NFR coverage"
    location: "project-documents/user/architecture/120-arch.guide-tooling.md"
---

# Review: slice — slice 121

**Verdict:** CONCERNS
**Model:** claude-opus-5-5

## Findings

### [PASS] Aligned with the architecture's design goals and cf contract

The slice covers everything the architecture's Constraints section asks for:
- `scripts/setup-ide` stays a bash wrapper at the same path.
- `--capabilities` still prints `dry-run write-lint root` and exits 0.
- The `--dry-run` and `--write-lint` literals stay in the wrapper text.
- The minimum is Python 3.9, with a clear error and no fallback to the old bash code.
- The runtime is standard library only, with no install step.
- Merging is gated on all 76 slice 120 tests passing with no snapshot changed.

Dependencies point the right way: the package depends only on cf and the standard library, and the tests depend on the package.

### [PASS] Scope discipline

"Port, not redesign" is enforced well:
- The known quirks (#38, #40) are reproduced and tagged for later `fix:` commits.
- #37 and #39, checksum adoption and Linux CI are explicitly excluded.
- argparse is rejected for a concrete compatibility reason, not by preference.

The module list maps to the bash function groups. That is about the right amount of structure: it makes a side-by-side review practical without over-engineering.

### [CONCERN] Wrapper sketch breaks when invoked by bare filename

The sketch computes `SCRIPT_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)"`. The current script (`scripts/setup-ide:17`) uses `dirname`, which handles this correctly.

If the script is run as `cd scripts && bash setup-ide claude`, then `BASH_SOURCE[0]` is `setup-ide`. `%/*` strips nothing, so the `cd` targets a file and fails. `SCRIPT_DIR` ends up empty, and the wrapper execs `python3 … /setup_ide/__main__.py`, giving a confusing Python "can't open file" error.

cf passes an absolute path, so cf is unaffected, but this is a regression for anyone running the script by hand. Two things to fix:
- Keep the `dirname` form, or handle the no-slash case. `dirname` is an external command, but it is only needed once Python is known to be present. Alternatively, run the `command -v python3` check first.
- Fail explicitly if `SCRIPT_DIR` resolution fails.

Even though the doc says "shape only", the wrapper is the entire cf-facing surface and should be correct in the design.

### [CONCERN] Failure modes for the new process and I/O paths are not enumerated

The doc defines `SetupError` and a single top-level handler. It doesn't say how these paths fail:

- **cf subprocess** (`subprocess.run`):
  - **Process errors:** bash maps exec failures to exit codes (126/127 → "other = hard error"). Python's `subprocess.run` raises `OSError`/`PermissionError` instead. State that these map to the same hard-error message and exit 1, rather than a traceback.
  - **Hangs:** state whether there is a timeout. "None, matching bash" is acceptable, but it should be written down, not implicit.
- **Dry-run sandbox:** bash removes the sandbox and log explicitly (`scripts/setup-ide:1542`). State that the Python uses `tempfile.TemporaryDirectory` (or try/finally), so the sandbox is cleaned up on `SetupError`, on unexpected exceptions and on Ctrl-C.
- **KeyboardInterrupt:** Python prints a traceback, which bash doesn't. Specify the handling, for example exit 130 with no traceback, and note it as a process-boundary handler.
- **macOS `/usr/bin/python3` stub without the command line tools:** this is the architecture's "Python missing on a fresh machine" risk. The stub opens an install dialog and exits non-zero, and the wrapper's `$(python3 --version)` in the error message runs the stub a second time. Describe this case and the message the user gets, and add it to the wrapper tests if possible.

### [CONCERN] Manifest sort order differs from bash in user locales, and the suite can't detect it

The doc says the manifest is sorted "the way `sort -k3` sorts it under `LC_ALL=C`, i.e. by byte order". But bash runs `sort -k3` at `scripts/setup-ide:346` under the caller's locale. `LC_ALL=C` is only set locally in the dry-run diff (line 1559).

The test harness forces `LC_ALL=C` (`tests/setup_ide/harness.py:111`), so the suite can't see the difference. In a UTF-8 locale, bash-written manifests can use locale collation order, while the Python will write byte order.

Reading manifests is order-independent, so this is probably harmless. Still, it contradicts "identical format" and could create diff noise in projects that commit `.context-forge/`. Either:
- record it as a deliberate, documented deviation (byte order is the better rule), or
- note it in the CHANGELOG entry.

Don't claim parity here.

### [NOTE] The isolated-mode explanation is version-dependent

"Isolated mode doesn't add the script directory" is only true from Python 3.11, where `-I` implies `-P`. On 3.9 and 3.10, `scripts/setup_ide/` is still put at `sys.path[0]`, so the package modules are also importable as top-level modules (`cli`, `context`, …). The design still works, since `__main__.py` adds `scripts/` itself. Two clarifications would help:
- Correct the rationale.
- Require package-qualified imports (`from setup_ide import …`), so no module gets imported twice under two names.

Running `__main__.py` by path rather than with `-m setup_ide` is fine for this.

### [NOTE] stdout/stderr interleaving under pipes

Bash writes each line immediately. Python block-buffers stdout when it isn't a TTY, so when cf or a user merges the streams (`2>&1`), warnings can appear in a different order than they do today. Since `cli.main` already reconfigures the streams, consider adding `line_buffering=True` (or flushing in `Reporter`) to keep the order the same.

### [NOTE] Slice 122 is not in the architecture's slice list

The slice declares `interfaces: [122]`. Slice 122 is defined in the slice plan (`120-slices.guide-tooling.md:32`), but the architecture's Anticipated Slices section and its `relatedSlices` field list only 120 and 121. This doesn't block the slice. The architecture doc should be updated to match.

### [PASS] NFR coverage

The architecture sets no latency or throughput targets. Its correctness goals (no behavior drift, same manifest format, no install step) are restated in the slice as testable success criteria, together with a verification walkthrough.

### Run Digest

- Response length: 7669 chars
- Response is newline-free: no
- Tool calls made: 6
- Tool calls failed: 0
- Stop reason: end_turn
- Output budget: backend default
- System prompt: preset+append
- Settings sources: project
- Reasoning characters: 0
- Effort: backend default
- Turns: not computed
- Tokens — prompt / cached / completion / reasoning: not computed / not computed / not computed / not computed
- Duration: 67.6 s
- `## Summary` located: yes
- `## Findings` located: yes
- Finding-shaped matches — whole response: 9
- Finding-shaped matches — inside fences: 0
- Finding-shaped matches — in findings section: 9
- Finding-shaped matches — surviving validation: 9
