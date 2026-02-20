---
docType: changelog
scope: project-wide
---

# Changelog

All notable changes to the AI Project Guide system will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.11.5] - 2026-02-19

### Changed
- Phase 5 guide: added frequent commit strategy, specify DEVLOG.md location
- TypeScript rules: full overhaul

### Fixed


## [0.11.4] - 2026-02-17

### Added
- UI development rules file (`rules/ui-development.md`)

### Changed
- Phase 5 guide: added "test-with" principle for task breakdown
- Phase 6 guide: streamlined and updated to reflect 2026 practices
- Session State Summary prompt: updated for clarity

## [0.11.3] - 2026-02-17

### Added
- **Phase 5: Task Breakdown guide** (`guide.ai-project.005-task-breakdown.md`) — playbook for converting slice designs into granular task lists

### Fixed
- Minor consistency fixes across rules files and `setup-ide` agent validation

## [0.11.2] - 2026-02-17

### Added
- Session State Summary prompt in `prompt.ai-project.system.md` for DEVLOG entries at end of work sessions

### Changed
- Phase 7: Added Session State Summary step at end of each work session
- Phase 8: Added Session State Summary step for integration results and next planned slice

## [0.11.1] - 2026-02-16

### Fixed
- Standardize guide frontmatter; ensure `dateUpdated` present on all guide files

## [0.11.0] - 2026-02-15

### Added
- **Phase 2.5: Project HLD Creation** - Dedicated phase for high-level design before slice planning
  - New process guide section in `guide.ai-project.000-process.md`
  - New parameterized prompt in `prompt.ai-project.system.md`
  - HLD now created separately from slice planning, using next available index in 050-089
- **Phase 3.5: Architectural Component Design** - Design architectural initiatives spanning multiple slices
  - New prompt for creating `nnn-arch.{component-name}.md` documents
  - Architecture documents function as HLD for their scope
- **Standalone feature index range (750-799)** - Dedicated range for features not tied to a slice
  - Slice range narrowed from 100-799 to 100-749 (650 slots)
  - New naming convention: `nnn-feature.{feature-name}.md`
- **Migration guides directory** (`project-guides/migrations/`)
  - `20260121-migration-guide.md` - Consistency standards migration
  - Moved v0.10.0 migration guide here (marked obsolete)
  - Root `MIGRATION.md` now serves as index
- **DEVLOG.md** - Internal session log for development continuity
- **Electron tool guides** - Comprehensive guides (00-05) covering architecture, project structure, electron-vite, testing, and decision guide
- **MCP tool guide** (`tool-guides/mcp/`) - Overview of Model Context Protocol integration

### Changed
- **YAML date fields standardized** to `dateCreated`/`dateUpdated` (was `created`/`lastUpdated`)
  - All dates use YYYYMMDD format (no dashes)
  - Updated all 78+ markdown files and all YAML specs in prompts/guides
- **Phase 3 (Slice Planning) updated** for dual-context support
  - Now accepts either project specification or architecture document as parent
  - Architecture documents serve as HLD for their scope (no separate HLD needed)
  - Updated `guide.ai-project.003-slice-planning.md` with dual-context methodology
- **Phase 4 (Slice Design) updated** to reflect current standards
- **Index ranges restructured**
  - 100-749: Slices and slice-linked work
  - 750-799: Standalone features (new)
  - 800-899: Reserved
  - Updated `file-naming-conventions.md`, `directory-structure.md`, and all references
- **All task files in `user/tasks/` now require index prefix**
  - `inventory.index-migration.md` → `952-inventory.index-migration.md`
  - `report.index-migration.20250930.md` → `953-report.index-migration.md`
- **Project-guides readme** updated with Phase 2.5/3.5, migrations, agents/rules sections, and dateCreated/dateUpdated in author schema
- **YAML frontmatter** now required on all markdown files (was ~55% coverage, now 100%)

### Fixed
- Malformed frontmatter in `tool-guides/shadcn/setup.md`
- Removed empty/orphaned files: `900-slice.maintenance.md`, `guide.object-creation.complex.md`, `api-guides/usgs/`
- Corrected 800-range misuse (feature file moved to 105-slice/tasks)
- All date fields across project now use consistent `dateCreated`/`dateUpdated` naming

## [0.10.0] - 2025-10-08

### BREAKING CHANGES
- **Directory rename**: `project-documents/private/` → `project-documents/user/` for clarity
  - "private" was confusing (implied secrecy, but directory should be committed)
  - "user" clearly indicates "your project work"
  - See [MIGRATION.md](MIGRATION.md) for migration steps
- **Environment variable rename**: `ORG_PRIVATE_GUIDES_URL` → `EXTERNAL_PROJECT_DOC_URL`
  - More accurate naming (not just for organizations)
  - Update your environment variables and CI/CD configs

### Added
- **Migration script**: `scripts/migrate-private-to-user.sh` - automated migration for user projects
- **Migration guide**: `MIGRATION.md` - comprehensive migration documentation

### Changed
- All documentation updated to reference `user/` instead of `private/`
- Bootstrap script now creates `project-documents/user/` structure
- All guides and prompts updated for new naming

## [0.9.2] - 2025-10-08

### Added
- **External guides support**: Import guides from another repository via `EXTERNAL_PROJECT_DOC_URL`
- **Bootstrap auto-setup**: Automatically creates update scripts for npm/pnpm and Python projects

### Fixed
- **setup-ide**: CLAUDE.md now created in project root instead of submodule directory
- **update-guides**: Script always runs from submodule (no manual copying needed)

### Changed
- **One-time upgrade required**: Existing projects need package.json update (see readme)

## [0.9.0] - 2025-10-06

### Changed
- **Git submodule architecture**: Migrated from git subtree to git submodule for cleaner separation
  - Framework guides now in `project-documents/ai-project-guide/` submodule
  - User work stays in `project-documents/private/` (parent repo)
  - Simplified updates: `git submodule update --remote`
  - Works for npm and non-npm projects (Python, Go, Rust, etc.)
- **Directory structure**: Finalized `user/` subdirectories
  - Added: `project-guides/` for project-specific customizations
  - Renamed: `code-reviews/` → `reviews/`
  - Removed: `maintenance/` directory (use `950-tasks.maintenance.md` instead)
  - Order: `analysis/, architecture/, features/, project-guides/, reviews/, slices/, tasks/`
- **Bootstrap scripts**: Universal setup for any project type
  - `bootstrap.sh` and `bootstrap.py` for one-command setup
  - Template stub scripts download from GitHub (single source of truth)
  - Auto-detects git repository root for safety

### Added
- **Template stub scripts** in `scripts/template-stubs/`
  - Minimal 3-line stubs for templates
  - Downloads full bootstrap scripts from ai-project-guide
  - Preserves `npx degit` simplicity

### Fixed
- `setup-ide` script now uses correct submodule paths
- Bootstrap scripts prevent running in wrong directory
- All path references updated for submodule structure

## [0.8.0] - 2025-01-04

### Added
- **3-digit index system (nnn)**: Migrated from 2-digit (nn) to 3-digit (nnn) indexing with semantic range allocation
  - **000-009**: Core process guides
  - **010-049**: Extended process documentation
  - **050-089**: Architecture and system design
  - **090-099**: Specialized guides
  - **100-799**: Active work (slices, tasks) - 700 slots for massive scalability
  - **800-899**: Feature documents
  - **900-939**: Code review tasks (40 slots)
  - **940-949**: Codebase analysis tasks (10 slots)
  - **950-999**: Maintenance tasks (50 slots)
- **File size management**: Documented 350-line limit for non-architecture files with systematic splitting procedure
- **Monorepo context initialization**: Separate dedicated prompt for monorepo vs standard project contexts

### Changed
- **HLD standardization**: Moved to `architecture/050-arch.hld-{project}.md` with consistent naming
- **Directory structure**: Consolidated `maintenance/` into tasks, renamed `code-reviews/` to `reviews/`, ordered by workflow
- **Simplified naming**: Removed redundant slice names from features - index number creates the link (DRY principle)
- **Path consistency**: Standardized to `user/{subdir}/...` pattern for all project-specific files

### Fixed
- Updated analysis, maintenance, and feature prompts for consistency with new structure
- Corrected path references, YAML fields, and various typos throughout documentation

## [0.7.0] - 2025-08-18

### Added
- **Slice-based development methodology**: Complete overhaul of project workflow to use vertical slices
  - **Phase 3: High-Level Design & Slice Planning** - Break projects into manageable vertical slices
  - **Phase 4: Slice Design (Low-Level Design)** - Create detailed technical designs for individual slices
  - **Phase 5: Slice Task Breakdown** - Convert slice designs into granular tasks with context headers
  - **Phase 6: Task Enhancement and Expansion** - Enhance slice tasks for reliable AI execution
  - **Phase 7: Slice Execution** - Implement individual slices with proper context management
  - **Phase 8: Slice Integration & Iteration** - Integrate completed slices and plan next iterations
- **New comprehensive guides**:
  - `guide.ai-project.03-slice-planning.md` - Complete guide for breaking projects into slices
  - `guide.ai-project.04-slice-design.md` - Detailed slice design methodology with templates
  - `guide.ai-project.06-task-expansion.md` - Updated task expansion for slice-based work
- **Legacy project migration**: 
  - `guide.ai-project.91-legacy-task-migration.md` - Systematic migration from legacy to slice-based approach
  - Comprehensive migration prompt for converting existing projects
- **Enhanced context management**:
  - YAML front matter for all slice task files with project state, dependencies, and metadata
  - Context summary sections to enable AI restart capability
  - Slice-specific file organization with `nn-slice.{slice-name}.md` naming convention
- **Improved file organization**:
  - `user/slices/` directory for slice-specific low-level designs
  - Sequential indexing for all slice and task files (01, 02, 03, etc.)
  - Clear separation between foundation work, feature slices, and integration work

### Changed
- **Project workflow**: Shifted from monolithic project approach to slice-based development
  - Projects now treated as "collections of slices" rather than single large entities
  - Each slice follows its own design → task → implementation → integration cycle
  - Better context management and reduced AI hallucination through smaller, focused work units
- **Guide numbering and organization**:
  - Moved code review guide to `guide.ai-project.90-code-review.md` (supplemental guides 90+)
  - Updated task expansion guide to Phase 6: `guide.ai-project.06-task-expansion.md`
  - Established clear distinction between core workflow phases (1-8) and supplemental guides (90+)
- **Prompt templates**: Complete overhaul of all prompt templates for slice-based workflow
  - New slice-specific prompts for planning, design, task breakdown, and implementation
  - Updated context refresh prompts to work with slice-based projects
  - Legacy prompts moved to deprecated section with migration guidance
- **Task file structure**:
  - Enhanced with YAML front matter including slice metadata and project state
  - Context summary sections for better AI restart capability
  - Updated naming convention: `nn-tasks.{slice-name}.md`
- **Documentation structure**:
  - Updated README.md with complete phase mapping table (1-8)
  - Added supplemental guides section and development approach guidance
  - Clarified when to use slice-based vs traditional approaches

### Fixed
- **Context management issues**: Slice-based approach significantly reduces "lost in the middle" problems
- **Guide references**: Updated all cross-references to use correct guide numbering
- **File naming consistency**: Established clear patterns for slice designs and task files

### Technical Details
- **Backward compatibility**: Legacy project support maintained with migration path
- **Agent integration**: Updated for better compatibility with Claude Code, Cline, and other AI agents
- **Scalability**: Slice-based approach enables future parallelization of development work
- **Quality assurance**: Enhanced task granularity reduces AI hallucination and improves success rates

### Migration Notes
- Existing projects can be migrated using the legacy migration guide
- Traditional approach still available for simple projects and single features
- All legacy prompts preserved in deprecated sections

## [0.6.0] - 2025-08-15

### Added
- **Claude Code support**: Added `claude` option to `setup-ide` script to generate `CLAUDE.md` file
  - Compiles all rules into single Claude-friendly format
  - Proper heading hierarchy (H1 → H2 → H3 → H4)
  - General Development Rules listed first, other categories alphabetically
  - Automatic frontmatter stripping and heading level adjustment

### Changed
- **Directory structure clarification**: Resolved ambiguity between directory concepts:
  - `project-documents/user/` for regular development (template instances)
  - `project-artifacts/` for monorepo template development
  - Deprecated `{template}/examples/our-project/` with migration path
- **Feature file naming convention**: Updated from `{feature}-feature.md` to `nn-feature.{feature}.md` format
- **Task file naming convention**: Updated from `{section}-tasks-phase-4.md` to `nn-tasks-{section}.md` format
  - Added sequential index prefix (01, 02, 03, etc.) for better organization
  - Removed confusing '-phase-4' suffix from task file names
  - Updated all prompt templates and guides to use new naming pattern
  - Streamlined and updated system prompts.
- **File naming documentation**: Updated `file-naming-conventions.md` with new task file patterns and documented legacy formats
- **Documentation updates**: Updated README.md to include Claude setup instructions

## [0.5.2] - 2025-07-26

### Added
- **Project document phase numbering**: Implemented `XX-name.{project}.md` naming convention for project-specific documents
- **Consistent ordering**: Project documents now follow the same phase-based ordering as guides
- **Setup Script**: setup scripts for Windsurf and Cursor rules/ and agents/.

### Changed
- **Project document names**: Updated project-specific document naming to use phase numbers:
  - `concept.{project}.md` → `01-concept.{project}.md`
  - `spec.{project}.md` → `02-spec.{project}.md`
  - `notes.{project}.md` → `03-notes.{project}.md`
- **Guide output locations**: Updated all guides to reference new phase-numbered document names
- **Directory structure**: Updated structure diagrams to reflect new naming convention

## [0.5.1] - 2025-07-24

### Added
- **Phase numbering system**: Implemented `guide.ai-project.XX-name.md` naming convention for all project guides
- **Clear phase progression**: Files now alphabetize correctly while showing clear phase order (00-process, 01-concept, 02-spec, 04-task-expansion, 05-code-review)

### Changed
- **Guide file names**: Renamed all project guides to use phase numbers:
- **Prompt file names**: Renamed prompt files for better clarity:
  - `template.ai-project.prompts.md` → `prompt.ai-project.system.md`
  - `guide.ai-project.05-code-review-crawler.md` → `prompt.code-review-crawler.md`
  - `guide.ai-project.process.md` → `guide.ai-project.00-process.md`
  - `guide.ai-project.concept.md` → `guide.ai-project.01-concept.md`
  - `guide.ai-project.spec.md` → `guide.ai-project.02-spec.md`
  - `guide.ai-project.task-expansion.md` → `guide.ai-project.04-task-expansion.md`
  - `guide.code-review.ai.md` → `guide.ai-project.05-code-review.md`
  - `guide.code-review-2.ai.md` → `guide.ai-project.05-code-review-2.md` (consolidated into main code review guide)
  - `guide.code-review-crawler.md` → `prompt.code-review-crawler.md`
- **Internal references**: Updated all cross-references between guides to use new naming convention
- **Template prompts**: Updated all prompt templates to reference new guide names
- **Rules consistency**: Updated `rules/general.md` to use `user/` instead of `our-project/`

### Removed
- **`project-guides/coderules.md`**: Completely removed deprecated file, replaced by `project-guides/rules/general.md`
- **`project-guides/guide.ai-project.05-code-review-2.md`**: Consolidated duplicate content into main code review guide

### Fixed
- **File organization**: All guides now follow consistent phase-based naming
- **Cross-references**: All internal links and dependencies updated to new structure

## [0.5.0] - 2025-07-24

### Added
- **New modular rules system**: Replaced monolithic `coderules.md` with organized `project-guides/rules/` directory
- **Agent configurations**: Added `project-guides/agents/` directory for IDE-specific agent configurations
- **IDE integration guide**: Added instructions for copying rules and agents to `.cursor/` and `.windsurf/` directories
- **Migration documentation**: Added comprehensive migration guide from `our-project/` to `user/` structure

### Changed
- **Directory structure**: Migrated from `our-project/` to `user/` throughout all guides
- **File organization**: Established flat structure under `user/` with dedicated folders for tasks, code-reviews, maintenance, ui
- **Task file naming**: Updated to consistent hyphen-separated naming (`{section}-tasks.md`)
- **Code review paths**: Updated all review guides to use `user/code-reviews/`
- **Template prompts**: Updated all prompt templates to reference new `user/` structure

### Deprecated
- **`project-guides/coderules.md`**: Marked as deprecated, replaced by modular `rules/` system
- **`our-project/` directory**: Replaced by `user/` directory (with migration path provided)

### Fixed
- **Directory structure**: Clarified distinction between `user/` (regular development) and deprecated `our-project/` structure
- **File naming consistency**: Updated examples in `file-naming-conventions.md` to use `user/`
- **Link references**: Fixed broken links in `project-guides/readme.md`

### Technical Details
- Updated 13 files to use new `user/` structure
- Added migration instructions for existing projects
- Maintained backward compatibility for legacy `coderules.md`
- Established clear separation between shared methodology and project-specific work

## [0.4.0] - Previous Release

### Added
- Initial AI project guide system
- 6-phase project methodology
- Tool-specific guides and framework documentation
- Code review processes and templates