# Overview
This document provides a reference for creating and maintaining DEVLOG.md. 
* File is always named DEVLOG.md
* File is always placed at project root.

**File structure:**
If DEVLOG.md does not exist, create it at project-root directory with the following structure. The frontmatter is required: tools that read the devlog fail when it is missing. Use the `devlog` schema from `file-naming-conventions`.

```yaml
---
docType: devlog
project: {project}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---
```

# Development Log
A lightweight, append-only record of development activity. Newest entries first.
Format: `## YYYYMMDD` followed by brief notes (1-3 lines per session). `## YYYY-MM-DD` headings are also accepted; use one style within a file. Update `dateUpdated` whenever you add an entry.
---

## YYYYMMDD
### Slice nnn: {Slice Name} — {Status}
- {concise session notes as described above}

# Archiving
DEVLOG.md grows without bound, and a very large file breaks agent tool-result buffers (a 1 MiB limit was hit at about 1.05 MB). Archiving is triggered by size, not by date.

* Archives live in `project-documents/user/archive/devlog/DEVLOG-YYYY-Qn.md`, for example `DEVLOG-2026-Q3.md`.
* Each section goes to the archive for the quarter in its own date heading, not the date of archiving.
* Archive files carry the same devlog frontmatter as DEVLOG.md and are ordered newest first.
* Config keys `devlog.max_bytes` and `devlog.target_bytes` set the limits. `cf check` warns when DEVLOG.md is over `devlog.max_bytes`, and `cf devlog archive` rolls older sections over into the archives. `devlog.target_bytes` is the size it archives down to.
* Archive headings may be `## YYYYMMDD`, `## YYYY-MM-DD`, or `## YYYY-MM` followed by trailing text.
