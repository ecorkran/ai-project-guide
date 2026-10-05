---
name: csharp-rules
description: C# and .NET coding standards and conventions. Use when writing, modifying, or reviewing .cs files, .csproj files, or .NET build configuration.
paths:
  - "**/*.cs"
  - "**/*.csproj"
  - "**/Directory.Build.props"
  - "**/.editorconfig"
---

### C# Rules

#### General
- Target the current LTS .NET release unless the project states otherwise.
- `setup-ide` checks the analyzer and build settings below on every run and reports what is missing; `setup-ide <target> --write-lint` adds `.editorconfig` and `Directory.Build.props` when they are absent. Run `dotnet build` (which runs the analyzers) in the pre-commit hook and in CI so the analyzers enforce these rules, not the agent.

#### Required Analyzer and Build Settings
- Baselines: `ai-project-guide/project-guides/lint/csharp/.editorconfig` and `ai-project-guide/project-guides/lint/csharp/Directory.Build.props`.
- `CA1031` (do not catch general exception types) at error. This enforces the exception-handling rule in general.md.
- `CS4014` (unawaited async call) and `CA2016` (forward `CancellationToken`) at error.
- `<Nullable>enable</Nullable>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`, and `<AnalysisLevel>latest-recommended</AnalysisLevel>` for every project, set once in `Directory.Build.props`.

#### Exception Handling
- Catch specific exception types. Never `catch (Exception)` or a bare `catch` except in a documented top-level handler at a process boundary; suppress `CA1031` there with a justification comment.
- Never swallow an exception silently. Log with the exception object and rethrow, or handle a specific type with a comment explaining why swallowing is correct.
- Rethrow with `throw;`, never `throw ex;`, to keep the stack trace.
- Use exception filters (`catch (HttpRequestException ex) when (...)`) instead of catching and rethrowing conditionally.

#### Async
- Never use `async void` except for event handlers.
- Await every `Task`. If a fire-and-forget is intended, discard explicitly (`_ = DoWorkAsync();`) with a comment saying why.
- Accept and forward `CancellationToken` on every async method that does I/O.
- Do not block on async code with `.Result` or `.Wait()`.

#### Types and Nullability
- Treat nullable warnings as errors; do not silence them with `!` unless the comment says why the value cannot be null.
- Use `record` types for immutable data transfer objects.
- Prefer `sealed` classes unless designed for inheritance.

#### Testing
- Use xUnit unless the project already uses another framework.
- Test projects follow the same analyzer and nullable settings as production code.
