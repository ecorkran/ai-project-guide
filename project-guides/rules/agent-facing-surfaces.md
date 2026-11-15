---
name: agent-facing-surfaces-rules
description: "Required agent-facing metadata: every MCP server ships the instructions field, every public website ships llms.txt. Use when building or scaffolding an MCP server or a public site."
alwaysApply: true
---

### Agent-Facing Surfaces

- **MCP servers ship `instructions`.** Every MCP server sets the optional `instructions` field: returned from `initialize` on spec revisions through 2025-11-25, and from `server/discover` on 2026-07-28. Write cross-tool guidance only: tool ordering, limits, error recovery, when to use this server. Do not repeat what tool descriptions already say.
- **Public websites ship `llms.txt`.** Every public website serves `/llms.txt` in llmstxt.org format: an H1 with the site name, a short blockquote summary, then H2 sections of `[name](url)` links.
