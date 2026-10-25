---
name: setup-ci
description: "Set up CI for a project, and offer to generate its own /release skill. Detects the stack, writes .github/workflows/ci.yml from the guide's baseline and generates the project's own .claude/skills/release/SKILL.md (release process: version bump, tag, CI watch, registry check). Use when the user says \"set up CI\", \"add a release skill\", \"add a release process\", \"set up releases\", or when a project has no .github/workflows/ci.yml or release skill."
---

# Set up CI and release

Run from the project root. Detect first, ask only about what can't be detected, then write two files. Both belong to the project afterward and are edited by hand. This skill does not maintain them.

Baselines live in the guide at `project-documents/ai-project-guide/project-guides/ci/<lang>/ci.yml` (python, typescript). If the stack is another language, say there is no baseline yet and stop. Do not improvise one.

If `.github/workflows/ci.yml` or `.claude/skills/release/SKILL.md` already exists, show what exists and ask before overwriting either.

## 0. Prepare the project

**No manifest.** No `pyproject.toml` and no `package.json` is normal right after onboarding. Offer to create a minimal skeleton and continue with step 1 once it is committed. If the user declines, stop.

Python (uv):
1. Ask for the package name and the minimum Python version. Do not pick either.
2. `uv init --package --name <pkg> --python <floor> --vcs none .`
3. Replace the placeholder `description`. Remove the hello-world `[project.scripts]` entry and the generated `main()`.
4. `uv add --dev ruff pyright pytest`
5. Copy the guide's `project-guides/lint/python/ruff.toml` to the project root as is. In `pyproject.toml`, add the `[tool.pyright]` block from `rules/python.md` with `pythonVersion` set to the floor, and `[tool.pytest.ini_options]` with `testpaths = ["tests"]`.
6. Add one smoke test in `tests/` that imports the package.
7. Run `ruff check`, `ruff format --check`, `pyright` and `pytest`, then commit the skeleton on its own (`chore: add project skeleton`).

TypeScript (ESM, Vitest):
1. Ask for the package name, the minimum Node major, and the package manager (npm or pnpm). Do not pick any of them. The `target` below needs Node 18 or newer; if the floor is lower, ask.
2. `npm init -y` (npm) or `pnpm init` (pnpm), then in `package.json` set `name`, `"type": "module"`, `engines.node` to `>=<floor>`, `"exports": "./dist/index.js"` and `"files": ["dist"]`. For pnpm also set `"packageManager": "pnpm@<version>"` from `pnpm --version`. Replace the placeholder `description` and the default `test` script, and remove `main`.
3. `npm i -D` (npm) or `pnpm add -D` (pnpm) with `typescript vitest eslint @eslint/js typescript-eslint @types/node`
4. Write `tsconfig.json` with `"strict": true`, `"target": "ES2022"`, `"module": "NodeNext"`, `"outDir": "dist"` and `"include": ["src", "tests"]`. Write `tsconfig.build.json` that extends it, sets `"rootDir": "src"` (TypeScript 6 requires it, and it keeps `dist/index.js` flat), and includes only `src`. Lint needs the first to cover the tests.
5. Copy the guide's `project-guides/lint/typescript/eslint.config.mjs` to the project root as is.
6. Set the scripts: `lint` is `eslint .`, `typecheck` is `tsc --noEmit`, `test` is `vitest run`, `build` is `tsc -p tsconfig.build.json`. The CI baseline runs these four.
7. Add `src/index.ts` containing `export {};` and `tests/smoke.test.ts` that imports it. NodeNext requires the `.js` extension on relative imports even in `.ts` files (`../src/index.js`); that is correct, so leave a comment saying so.
8. Run the four scripts with the chosen package manager, then commit the skeleton on its own (`chore: add project skeleton`).

**.gitignore.** If `.gitignore` is missing, or lacks the stack's basics (python: `.venv/`, `__pycache__/`, `.env`; typescript: `node_modules/`, `dist/`, `.env`), offer the standard template for the stack from github/gitignore (`Python.gitignore` or `Node.gitignore`), plus `.env`. Merge into an existing file; never drop the user's own lines.

## 1. Detect

| Slot | How |
|---|---|
| Language | `pyproject.toml` means python; `package.json` plus `tsconfig.json` means typescript |
| Version files | Grep the current version string in `pyproject.toml`, `package.json`, `__init__.py`/`_version.py`, and the project's other manifests and source files. Skip the changelog, the devlog and `project-documents/`: they record versions rather than define them. List every remaining hit. |
| Lock refresh | python: `uv lock` if `uv.lock` exists. npm: `npm install --package-lock-only`; pnpm: `pnpm install --lockfile-only`. None if no lockfile. |
| Package manager | typescript only. `pnpm-lock.yaml` or a `packageManager` field starting `pnpm@` means pnpm; `package-lock.json` means npm. Both or neither: ask. |
| Tag format | `git tag --sort=-creatordate \| head`. Copy the pattern (`v1.2.3`, `1.2.3`). No tags: `vX.Y.Z`. |
| Tag | `<tag>` in the release skill: the tag format written with the literal placeholder `X.Y.Z` (so `vX.Y.Z` or `X.Y.Z`). The release fills in the real number at release time. |
| Changelog | `CHANGELOG.md` (check the root, then `docs/`). Note whether it has `## [Unreleased]`. None: the release skill skips the changelog step. |
| Devlog | `DEVLOG.md` at the root only. Ignore any other devlog, including `project-documents/DEVLOG.md`. None at the root: skip the devlog step without asking. |
| Publish target | Always ask: PyPI, npm or none. A manifest name does not mean the project is published. If a workflow already has a publish job, offer its target as the default. |
| Package name | `name` from the manifest. It can differ from the repo name. |
| Project | `<project>` in the release skill: the package name, or the repo directory name when there is none. |
| Registry | `<registry>` in the release skill: `PyPI` or `npm`, from the publish target. None: the `[registry]` text is removed. |
| Registry check | PyPI: `https://pypi.org/pypi/<pkg>/<ver>/json`. npm: `npm view <pkg>@<ver> version`. None: the release stops at green CI. |
| Python versions | Every minor listed in the `Programming Language :: Python :: 3.N` trove classifiers, as a quoted YAML list. No classifiers: every minor from the `requires-python` floor through its upper bound. No upper bound, or no `requires-python`: ask, offering the interpreters from `uv python list --only-installed` as the choices. Never fill the top of the range from memory. |
| Node versions | The majors `engines.node` allows, as a quoted YAML list. If `engines.node` is missing or has no upper bound, ask which majors to test. Never fill the range from memory. |
| Publish runtime | `__PUBLISH_PYTHON_VERSION__` / `__PUBLISH_NODE_VERSION__`: the lowest version in the matrix. |
| Tag glob | `__TAG_GLOB__`, derived from the tag format: `v*` for v-prefixed tags, `[0-9]*` for bare ones. |
| Commit type | `<commit type>` in the release skill: `package` if the project uses the guide's commit types, else `chore`. |
| Check commands | python: `ruff check`, `ruff format --check`, `pyright` (or the project's type checker), `pytest`. typescript: the `lint`, `typecheck`, `test`, `build` scripts in package.json. Fill `__*_SCRIPT__` only with scripts that exist. If one is missing, say so and drop that step rather than inventing it. |
| Integration branch | `cf config get git.integration_branch`, only to fill the CI trigger branches (`main`, plus this value if set). Never bake it into the release skill. |
| cf project | Does `cf` exist and does `project-documents/` exist? Decides whether the release skill keeps the cf steps. |
| Frontmatter block | Enable the OPTIONAL cf block in ci.yml when `project-documents/` exists and its markdown files carry YAML frontmatter. Otherwise remove it. |
| Fetch main | Enable the OPTIONAL `git fetch origin main:main` line when any test file reads `main` from the project's own checkout: `origin/main`, a `main..` range, or `--diff main` and similar ref arguments. A branch named `main` in a temporary repo the test creates itself (`git init -b main`) does not count. Tag builds go red without it. No such reference: remove it. Unsure: ask. |

Ask the user only about what is still unknown, plus the publish target, which is always asked. Present everything detected in one short list and let the user correct it before writing.

## 2. Write ci.yml

Copy the baseline for the language to `.github/workflows/ci.yml` and replace every `__SLOT__`. Then:

- No publish target: delete the block between `BEGIN PUBLISH` and `END PUBLISH`, and the manual-step note at the top that refers to it.
- TypeScript with pnpm: in both jobs, add `- uses: pnpm/action-setup@v4` before each `actions/setup-node` step (it reads the version from `packageManager`), change `cache: npm` to `cache: pnpm`, replace `npm ci` with `pnpm install --frozen-lockfile` and `npm run` with `pnpm run`. Leave `npm publish` as is; the runner has npm.
- TypeScript: drop `--access public` from the publish step when the manifest's `publishConfig.access` is `restricted`.
- Keep the `needs:` list on `publish` equal to every test job in the file.
- Each OPTIONAL block is decided by its probe in step 1: uncomment it when the probe says enable, delete it otherwise. Do not leave commented blocks behind.
- Grep the result for `__[A-Z]` to confirm no slot is left unfilled. A leftover slot is an error, not something to guess.

Tell the user the one-time manual step for the publish target (PyPI trusted publishing, or an `NPM_TOKEN` secret). The first tag fails without it.

## 3. Write the release skill

Write the template below to `.claude/skills/release/SKILL.md`, with these changes:

- Fill the `<...>` slots from step 1.
- Markers are `[cf]`, `[changelog]`, `[devlog]`, `[registry]`, and the inverse form `[no X]` for each (`[no registry]`, `[no changelog]`). A marker on a heading governs the whole step; an inline marker governs everything after it up to the next marker or the end of that list item or paragraph. Keep the marked text only if that thing exists (cf present, file present, registry present; `[no registry]` is kept only when there is none). Remove the markers themselves.
- In step 4, the check commands are exactly the commands in the ci.yml just written, so the two cannot drift. They stay check-only (`ruff format --check`, not `ruff format`): the release commit touches version files and nothing else.
- Renumber after removals.
- Keep the integration-branch read as a command to run at release time. Do not write its value into the skill.

### Template

````markdown
---
name: release
description: Cut a <project> release — bump the version, update the changelog, tag, push, then watch CI until it is green [registry] and <registry> shows the new version. Use when the user says "release", "cut a release", "ship it", or "bump and tag".
---

# Release <project>

Run from the repo root. Stop and report on any failed command; don't work around it.

## 1. Check cf state [cf]

Run `cf next`. If it reports something unfinished (open review gate, unchecked tasks, failing check), stop and show it. Otherwise continue.

## 2. Merge [cf]

Read the target with `cf config get git.integration_branch` (empty means `main`). If the current branch is a slice branch not yet merged into the target, follow the merge steps in CLAUDE.md (Git Rules). If already on the target with the work merged, skip this.

## 3. Pick the version

The working tree must be clean before continuing; if it isn't, stop and show `git status`.

Current version: `<version file>`. Read the unreleased changes. [changelog] Use `## [Unreleased]` in <changelog path>. [no changelog] Use `git log` since the last tag.

- **Patch** is the default: fixes, refinements, and new flags, options, parameters, config keys or checks. A non-empty changelog, or entries under `### Added`, does not make a release minor.
- **Minor** only for a new user-facing feature or a significant new AI capability. Propose it in one line with the reason and wait for the user to confirm before changing any files.
- **Major** only when the user explicitly asks for it.

For a patch, state the chosen version in one line and proceed.

## 4. Bump and document

1. Set the version in <each version file>, then run <lock refresh command>.
2. [changelog] In <changelog path>, insert `## [X.Y.Z] - YYYYMMDD` directly under `## [Unreleased]`, so the unreleased entries sit under the new version and `[Unreleased]` is empty. Entries stay short and user-facing.
3. [devlog] In <devlog path>, under today's heading (create it at the top if missing), add `### Release X.Y.Z` with a one-line contents summary.
4. Run <check commands from ci.yml>. Any failure stops the release; CI would block the publish anyway. These only check: if formatting or lint fails, stop, fix it in its own commit, and start the release again.
5. Commit: `<commit type>: bump version to X.Y.Z`.

## 5. Tag and push

Invoking this skill is the user's request to push.

```
git tag -a <tag> -m "<tag>"
git push
git push --tags
```

## 6. Watch CI

[registry] The `publish` job in `.github/workflows/ci.yml` runs only on the tag and needs every test job to pass. A red test job means nothing publishes, silently. A tag alone is not a release: it is not done until <registry> shows the new version.
[no registry] CI must be green on the tagged commit.

Start a loop via the `loop` skill with a 5 minute interval and this check:

1. `gh run list --workflow ci.yml --branch <tag> --json databaseId,status,conclusion,headSha` — match `headSha` to the tagged commit. (`--commit` is unreliable right after a push.)
2. Still running: report status and wait for the next tick.
3. Failed: pull the log (`gh run view <id> --log-failed`), report the actual error, stop the loop.
4. Passed: [registry] confirm with `<registry check command>`. If it returns, report "X.Y.Z live on <registry>" and stop the loop. If not yet, wait for the next tick. [no registry] Report green CI and stop the loop.

Always stop the loop yourself when it resolves either way.
````

## 4. Report

Print the two paths written, the detected values the user should double-check (version files, tag format), and the one-time manual step. If the integration branch was added to the CI triggers, say that it was copied in at generation time: if `git.integration_branch` changes later, the `branches:` lists in `ci.yml` must be updated by hand. Do not commit unless the user asks.
