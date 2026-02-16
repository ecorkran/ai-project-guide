<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# I need to provide AI with good guidance on MCP creation.  I'd like to use Anthropic's guidelines, and potentially material from its MCP course.  If needed I could find code samples.

Focus on Python, Node, Typescript, and the available transport methods.  Unless otherwise specified, focus on MCP servers that can be run locally.

Here's a comprehensive MCP server creation guide synthesized from Anthropic's official documentation, their MCP course curriculum, the SDK repositories, and their engineering blog posts on tool design.

## What This Guide Covers

The document above is a complete reference you can feed to any AI assistant as context for MCP server development. Here's a walkthrough of the key sections:

## Architecture \& Primitives

MCP uses a **host → client → server** architecture over JSON-RPC. The three core primitives each serve a distinct role in the interaction model:[^1_1][^1_2][^1_3]

- **Tools** — model-controlled functions the AI decides when to invoke (e.g., `search_logs`, `create_issue`)
- **Resources** — application-controlled data the client decides how to surface (e.g., file contents, DB schemas)
- **Prompts** — user-controlled templates invoked via slash commands or menus (e.g., `/review-code`)

Understanding *who controls* each primitive is fundamental to designing a good server.

## Transport Methods

The current spec (2025-11-25) defines two official transports:[^1_4]


| Transport | Use Case | How It Works |
| :-- | :-- | :-- |
| **stdio** | Local servers (recommended) | Client spawns server as subprocess; JSON-RPC over stdin/stdout |
| **Streamable HTTP** | Remote/network servers | HTTP POST/GET with optional SSE streaming; supports auth and sessions |
| ~~SSE~~ | ~~Deprecated~~ | Replaced by Streamable HTTP as of 2025-03-26 |

For local development, **stdio is almost always what you want**. The critical rule for Python stdio servers: **never use `print()` to stdout** — it corrupts the JSON-RPC message stream.[^1_5][^1_6][^1_7]

## Python (FastMCP)

The Python SDK uses a decorator-based approach via `FastMCP` that auto-generates tool definitions from type hints and docstrings:[^1_7][^1_8]

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("my-server")

@mcp.tool()
async def search_docs(query: str, max_results: int = 5) -> str:
    """Search documentation for relevant articles."""
    ...

@mcp.resource("config://app")
def get_config() -> str:
    """Current application configuration."""
    ...

@mcp.prompt()
def review_code(code: str, language: str = "python") -> str:
    """Review code for bugs and best practices."""
    ...

mcp.run(transport="stdio")
```

Setup uses `uv` as the package manager: `uv add "mcp[cli]" httpx`.[^1_7]

## TypeScript/Node

The TypeScript SDK uses `McpServer` with explicit `registerTool`, `registerResource`, and `registerPrompt` methods, and Zod for schema validation:[^1_9]

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.registerTool("search_docs", {
    title: "Search Docs",
    description: "Search documentation",
    inputSchema: { query: z.string(), maxResults: z.number().default(5) },
    annotations: { readOnlyHint: true, openWorldHint: true },
}, async ({ query, maxResults }) => { ... });

const transport = new StdioServerTransport();
await server.connect(transport);
```

Note the `registerTool` API is the newer recommended approach over the older `server.tool()` method.[^1_9]

## Tool Annotations

These are behavioral hints that help clients (Claude, ChatGPT, etc.) understand tool safety profiles:[^1_10][^1_11]


| Annotation | Default | When to Set |
| :-- | :-- | :-- |
| `readOnlyHint` | `false` | `true` for queries, searches, reads |
| `destructiveHint` | `true` | `false` for additive-only operations (create, append) |
| `idempotentHint` | `false` | `true` for operations safe to retry (PUT-like semantics) |
| `openWorldHint` | `true` | `false` for local-only operations |

ChatGPT skips confirmation prompts for read-only tools, and Claude uses these hints for execution decisions.[^1_10]

## Anthropic's Engineering Best Practices

From Anthropic's "Writing Effective Tools for Agents" blog post — arguably the most important section:[^1_12]

1. **Design for workflows, not CRUD wrappers** — Instead of `list_users` + `list_events` + `create_event`, build a `schedule_event` tool that handles the full workflow
2. **Namespace tools clearly** — Use prefixes like `github_search_issues`, `jira_create_ticket` so agents can disambiguate across dozens of servers
3. **Return meaningful context** — Resolve UUIDs to human-readable names; agents perform dramatically better with semantic identifiers
4. **Optimize for token efficiency** — Implement pagination, filtering, truncation with sensible defaults; consider a `response_format` parameter for "concise" vs "detailed"
5. **Prompt-engineer your tool descriptions** — Treat them like onboarding docs for a new hire; make implicit context explicit
6. **Write helpful error messages** — "User not found. Try `search_users(name='...')`" beats "Error: 404"

## Testing

The **MCP Inspector** is the primary testing tool:[^1_13]

```bash
npx @modelcontextprotocol/inspector
```

It lets you browse all three primitive types, execute tools, read resources, and generate prompts interactively — essential before connecting to a real host.

## Recent Spec Updates

The November 2025 spec revision added several notable features:[^1_14]

- **Tasks** — experimental primitive for long-running async workflows ("call now, fetch later")
- **Sampling with Tools** — servers can initiate LLM sampling requests with tool definitions, enabling server-side agentic loops
- **Standardized tool-name format** — canonical naming for cross-SDK interoperability

The guide document covers all of this with complete, runnable code examples in both Python and TypeScript. You can use it directly as context when asking an AI to help you build MCP servers.
<span style="display:none">[^1_15][^1_16][^1_17][^1_18][^1_19][^1_20][^1_21][^1_22][^1_23][^1_24][^1_25][^1_26][^1_27][^1_28][^1_29][^1_30][^1_31][^1_32][^1_33][^1_34][^1_35][^1_36][^1_37][^1_38][^1_39][^1_40][^1_41][^1_42][^1_43][^1_44][^1_45][^1_46][^1_47][^1_48][^1_49][^1_50][^1_51][^1_52][^1_53][^1_54][^1_55][^1_56][^1_57]</span>

<div align="center">⁂</div>

[^1_1]: https://datasciencedojo.com/blog/guide-to-model-context-protocol/

[^1_2]: https://opencv.org/model-context-protocol/

[^1_3]: https://devcenter.upsun.com/posts/mcp-interaction-types-article/

[^1_4]: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports

[^1_5]: https://mcp-framework.com/docs/Transports/transports-overview/

[^1_6]: https://fly.io/docs/mcp/transports/

[^1_7]: https://modelcontextprotocol.io/docs/develop/build-server

[^1_8]: https://composio.dev/blog/how-to-effectively-use-prompts-resources-and-tools-in-mcp

[^1_9]: https://github.com/modelcontextprotocol/typescript-sdk

[^1_10]: https://gofastmcp.com/servers/tools

[^1_11]: https://modelcontextprotocol.io/legacy/concepts/tools

[^1_12]: https://www.anthropic.com/engineering/writing-tools-for-agents

[^1_13]: https://blog.fka.dev/blog/2025-03-22-building-hello-world-mcp-server/

[^1_14]: https://workos.com/blog/mcp-2025-11-25-spec-update

[^1_15]: https://www.freecodecamp.org/news/how-to-build-a-custom-mcp-server-with-typescript-a-handbook-for-developers/

[^1_16]: https://www.youtube.com/watch?v=kXuRJXEzrE0

[^1_17]: https://cnb.cool/baibaiyaonuli/mcp-for-beginners/-/blob/main/03-GettingStarted/05-stdio-server/README.md

[^1_18]: https://www.anthropic.com/news/model-context-protocol

[^1_19]: https://www.linkedin.com/posts/rahul-shetty-venkatesh_build-your-own-mcp-servers-with-typescript-activity-7393564614279458816-5MA2

[^1_20]: https://anthropic.skilljar.com/introduction-to-model-context-protocol

[^1_21]: https://www.anthropic.com/learn/build-with-claude

[^1_22]: https://www.anthropic.com/engineering/code-execution-with-mcp

[^1_23]: https://huggingface.co/learn/mcp-course/en/unit0/introduction

[^1_24]: https://www.reddit.com/r/modelcontextprotocol/comments/1k0doby/which_mcp_server_transport_is_better_comparing/

[^1_25]: https://www.firemcp.com/tutorials.html

[^1_26]: https://modelcontextprotocol.io/docs/develop/build-client

[^1_27]: https://modelcontextprotocol.info/docs/quickstart/quickstart/

[^1_28]: https://www.youtube.com/watch?v=gKkTpVeqdcY

[^1_29]: https://arthurchiao.art/blog/but-what-is-mcp/

[^1_30]: https://www.mintmcp.com/blog/enterprise-development-guide-ai-agents

[^1_31]: https://www.youtube.com/watch?v=oq3dkNm51qc

[^1_32]: https://hackteam.io/blog/build-your-first-mcp-server-with-typescript-in-under-10-minutes/

[^1_33]: https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/1567

[^1_34]: https://modelcontextprotocol.io/specification/2025-03-26

[^1_35]: https://code.visualstudio.com/blogs/2025/06/12/full-mcp-spec-support

[^1_36]: https://gpt-trainer.com/blog/anthropic+model+context+protocol+mcp

[^1_37]: https://modelcontextprotocol.info/docs/concepts/prompts/

[^1_38]: https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/

[^1_39]: https://codesignal.com/learn/courses/developing-and-integrating-a-mcp-server-in-python/lessons/exploring-and-exposing-mcp-server-capabilities-tools-resources-and-prompts

[^1_40]: https://dev.to/alexmercedcoder/building-a-basic-mcp-server-with-python-5ci7

[^1_41]: https://gofastmcp.com/servers/prompts

[^1_42]: https://oneuptime.com/blog/post/2025-12-17-build-mcp-server-nodejs/view

[^1_43]: https://github.com/modelcontextprotocol/docs/issues/165

[^1_44]: https://dev.to/kevin-uehara/building-your-first-mcp-server-a-beginners-guide-59ml

[^1_45]: https://github.com/EnkrateiaLucca/mcp-course

[^1_46]: https://www.reddit.com/r/mcp/comments/1lkd0sw/got_my_first_full_mcp_stack_tools_prompts/

[^1_47]: https://obot.ai/resources/learning-center/mcp-anthropic/

[^1_48]: https://gofastmcp.com/python-sdk/fastmcp-resources-template

[^1_49]: https://www.reddit.com/r/mcp/comments/1pj6okz/lessons_from_anthropic_how_to_design_tools_agents/

[^1_50]: https://advanced-mcp-features.epicai.pro/01

[^1_51]: https://gofastmcp.com/servers/resources

[^1_52]: https://docs.quarkiverse.io/quarkus-mcp-server/dev/reference-annotations.html

[^1_53]: https://gofastmcp.com/tutorials/create-mcp-server

[^1_54]: https://modelcontextprotocol.info/docs/tutorials/writing-effective-tools/

[^1_55]: https://blog.marcnuri.com/mcp-tool-annotations-introduction

[^1_56]: https://redandgreen.co.uk/building-dynamic-mcp-resources-with-templates/ai-ml/

[^1_57]: https://github.com/fastmcp-me/fastmcp-python

