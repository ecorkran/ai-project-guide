# Overview
This document provides a reference for creating and maintaining CHANGELOG.md. 
* File is always named CHANGELOG.md
* File is always placed at project root.

**File structure:**

```yaml
---
docType: changelog
scope: project-wide
---
```

# Changelog
All notable changes to the AI Project Guide system will be documented in this file.  Entries should be concise, ideally 1-2 lines.  Current changes not yet pushed and tagged will accumulate in [Unreleased]

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Entry Format**
## [Version]
### Added
### Changed
### Fixed

**Example**
## [0.13.20] - 20260320
### Added
- Commands: agent_quickstart.md added to improve adoption by AI agents.
### Changed
- Prompts: Phase 6 now specifies `workflow_check`/`cf check` with fix parameter as post-implementation step
### Fixed
- cf build --json now correctly outputs json for use in pipelines.
