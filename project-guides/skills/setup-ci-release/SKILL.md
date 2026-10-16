---
name: setup-ci-release
description: Set up CI and a release process for a project. Detects the stack, writes .github/workflows/ci.yml from the guide's baseline and generates the project's own .claude/skills/release/SKILL.md. Use when the user says "set up CI", "add a release process", "set up releases", or when a project has no .github/workflows/ci.yml or release skill.
---

# Set up CI and release

Run from the project root. Detect first, ask only about what can't be detected, then write two files. Both belong to the project afterward and are edited by hand. This skill does not maintain them.

Baselines live in the guide at `project-documents/ai-project-guide/project-guides/ci/<lang>/ci.yml` (python, typescript). If the stack is another language, say there is no baseline yet and stop. Do not improvise one.

If `.github/workflows/ci.yml` or `.claude/skills/release/SKILL.md` already exists, show what exists and ask before overwriting either.

## 1. Detect

| Slot | How |
|---|---|
| Language | `pyproject.toml` means python; `package.json` plus `tsconfig.json` means typescript |
| Version files | Grep the current version string in `pyproject.toml`, `package.json`, `__init__.py`/`_version.py`, and any other tracked file. List every hit. |
| Lock refresh | python: `uv lock` if `uv.lock` exists. npm: `npm install --package-lock-only`; pnpm: `pnpm install --lockfile-only`. None if no lockfile. |
| Tag format | `git tag --sort=-creatordate \| head`. Copy the pattern (`v1.2.3`, `1.2.3`). No tags: `vX.Y.Z`. |
| Changelog | `CHANGELOG.md` (check the root, then `docs/`). Note whether it has `## [Unreleased]`. None: the release skill skips the changelog step. |
| Devlog | `DEVLOG.md`. None: skip that step. |
| Publish target | An existing publish job in a workflow, else the manifest: python `[project]` name means PyPI; package.json without `"private": true` means npm. Private or no manifest name: none. |
| Package name | `name` from the manifest. It can differ from the repo name. |
| Registry check | PyPI: `https://pypi.org/pypi/<pkg>/<ver>/json`. npm: `npm view <pkg>@<ver> version`. None: the release stops at green CI. |
| Python versions | Parse `requires-python` and list the supported minors (e.g. `[">=3.12"]` means 3.12 and 3.13). |
| Node versions | `engines.node`, else ask. |
| Check commands | python: `ruff check`, `ruff format --check`, `pyright` (or the project's type checker), `pytest`. typescript: the `lint`, `typecheck`, `test`, `build` scripts in package.json. Fill `__*_SCRIPT__` only with scripts that exist. If one is missing, say so and drop that step rather than inventing it. |
| Integration branch | `cf config get git.integration_branch`, only to fill the CI trigger branches (`main`, plus this value if set). Never bake it into the release skill. |
| cf project | Does `cf` exist and does `project-documents/` exist? Decides whether the release skill keeps the cf steps. |

Ask the user only about what is still unknown. The publish target is the usual one. Present everything detected in one short list and let the user correct it before writing.

## 2. Write ci.yml

Copy the baseline for the language to `.github/workflows/ci.yml` and replace every `__SLOT__`. Then:

- No publish target: delete the block between `BEGIN PUBLISH` and `END PUBLISH`, and the manual-step note at the top that refers to it.
- Keep the `needs:` list on `publish` equal to every test job in the file.
- Remove comment-only OPTIONAL blocks the project doesn't want. Leave them if unsure.
- Grep the result for `__` to confirm no slot is left unfilled. A leftover slot is an error, not something to guess.

Tell the user the one-time manual step for the publish target (PyPI trusted publishing, or an `NPM_TOKEN` secret). The first tag fails without it.

## 3. Write the release skill

Write the template below to `.claude/skills/release/SKILL.md`, with these changes:

- Fill the `<...>` slots from step 1.
- Steps marked `[cf]` stay only if cf is present. Steps marked `[changelog]`, `[devlog]`, `[registry]` stay only if that thing exists. Remove the markers.
- In step 4, the check commands are exactly the commands in the ci.yml just written, so the two cannot drift.
- Renumber after removals.
- Keep the integration-branch read as a command to run at release time. Do not write its value into the skill.

### Template

````markdown
---
name: release
description: Cut a <project> release — bump the version, update the changelog, tag, push, then watch CI and <registry> until the publish lands. Use when the user says "release", "cut a release", "ship it", or "bump and tag".
---

# Release <project>

Run from the repo root. Stop and report on any failed command; don't work around it.

## 1. Check cf state [cf]

Run `cf next`. If it reports something unfinished (open review gate, unchecked tasks, failing check), stop and show it. Otherwise continue.

## 2. Merge [cf]

Read the target with `cf config get git.integration_branch` (empty means `main`). If the current branch is a slice branch not yet merged into the target, follow the merge steps in CLAUDE.md (Git Rules). If already on the target with the work merged, skip this.

The working tree must be clean before continuing.

## 3. Pick the version

Current version: `<version file>`. Read the unreleased changes ([changelog] `## [Unreleased]` in <changelog path>; otherwise `git log` since the last tag).

- **Patch** is the default: fixes, refinements, and new flags, options, parameters, config keys or checks. A non-empty changelog, or entries under `### Added`, does not make a release minor.
- **Minor** only for a new user-facing feature or a significant new AI capability. Propose it in one line with the reason and wait for the user to confirm before changing any files.
- **Major** only when the user explicitly asks for it.

For a patch, state the chosen version in one line and proceed.

## 4. Bump and document

1. Set the version in <each version file>, then run <lock refresh command>.
2. [changelog] In <changelog path>, insert `## [X.Y.Z] - YYYYMMDD` directly under `## [Unreleased]`, so the unreleased entries sit under the new version and `[Unreleased]` is empty. Entries stay short and user-facing.
3. [devlog] In <devlog path>, under today's heading (create it at the top if missing), add `### Release X.Y.Z` with a one-line contents summary.
4. Run <check commands from ci.yml>. Any failure stops the release; CI would block the publish anyway.
5. Commit: `<commit type>: bump version to X.Y.Z`.

## 5. Tag and push

Invoking this skill is the user's request to push.

```
git tag -a <tag format> -m "<tag format>"
git push
git push --tags
```

## 6. Watch CI [registry] and <registry>

The `publish` job in `.github/workflows/ci.yml` runs only on the tag and needs every test job to pass. A red test job means nothing publishes, silently. The release is not done until the registry shows the new version. A tag alone is not a release.

Start a loop via the `loop` skill with a 5 minute interval and this check:

1. `gh run list --workflow ci.yml --branch <tag> --json databaseId,status,conclusion,headSha` — match `headSha` to the tagged commit. (`--commit` is unreliable right after a push.)
2. Still running: report status and wait for the next tick.
3. Failed: pull the log (`gh run view <id> --log-failed`), report the actual error, stop the loop.
4. Passed: [registry] confirm with `<registry check command>`. If it returns, report "X.Y.Z live on <registry>" and stop the loop. If not yet, wait for the next tick. [no registry] Report green CI and stop the loop.

Always stop the loop yourself when it resolves either way.
````

## 4. Report

Print the two paths written, the detected values the user should double-check (version files, tag format), and the one-time manual step. Do not commit unless the user asks.
