# Overview
This document provides a reference for creating and maintaining DEVLOG.md. 
* File is always named DEVLOG.md
* File is always placed at project root.

**File structure:**
If DEVLOG.md does not exist, create it at project-root directory with the following structure:

```yaml
---
docType: devlog
scope: project-wide
description: Internal session log for development work and project context
---
```

# Development Log
A lightweight, append-only record of development activity. Newest entries first.
Format: `## YYYYMMDD` followed by brief notes (1-3 lines per session).
---

## YYYYMMDD
### Slice nnn: {Slice Name} — {Status}
- {concise session notes as described above}