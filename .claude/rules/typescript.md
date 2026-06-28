---
description:   TypeScript strict typing standards, idiomatic patterns, and project conventions. Use for all TypeScript files. Covers type annotations, generics, module patterns, and error handling.
paths: 
  - "**/*.ts"
  - "**/*.tsx"
---

### TypeScript Rules

#### Core Principles

TypeScript's type system is a **compile-time safety net**. The goal is to catch errors before runtime. Every `any` is a hole in that net. Every untyped function boundary is a place where bugs can hide. Write types that make illegal states unrepresentable.

#### Strict Mode & the `any` Ban

- **Strict mode is mandatory.** `tsconfig.json` must include `"strict": true`.
- **`any` is forbidden.** This is not a suggestion. Do not use `any` in type annotations, return types, generic parameters, or type assertions (`as any`).
  - If you are tempted to use `any`, stop and determine the actual type.
  - If the type is complex, define an interface or type alias.
  - If you are working with truly unknown data (e.g., parsing JSON, external API responses), use `unknown` and narrow with type guards.
  - If a library's types are incomplete, write a declaration file (`.d.ts`) rather than using `any`.
- **`as` type assertions are a code smell.** Prefer type guards, discriminated unions, or generics. If you must assert, document why in a comment.

##### When You Encounter `any` in Existing Code

If you encounter `any` in code you are modifying, **replace it** with a proper type as part of your change. Do not propagate `any` to new code. If the fix is non-trivial and outside the scope of your current task, add a `// TODO: Replace any — see [reason]` comment and flag it.

#### Type Design Patterns

##### Discriminated Unions Over String Checks

Use discriminated unions (tagged unions) instead of runtime string matching to distinguish between variants. The compiler enforces exhaustiveness.

```typescript
// GOOD — compiler-enforced, exhaustive
type TemplateExpression =
  | { kind: 'simple'; variableName: string }
  | { kind: 'pipe'; parts: string[] }
  | { kind: 'conditional'; variable: string; trueContent: string; falseContent: string };

function evaluate(expr: TemplateExpression): string {
  switch (expr.kind) {
    case 'simple': return lookupVariable(expr.variableName);
    case 'pipe': return processPipe(expr.parts);
    case 'conditional': return expr.variable ? expr.trueContent : expr.falseContent;
    // TypeScript errors if a case is missing
  }
}

// BAD — runtime guessing, no compiler help
function evaluate(expression: string): string {
  if (expression.includes(' | ')) { /* ... */ }
  else if (expression.startsWith('#if')) { /* ... */ }
  else { /* ... */ }
}
```

##### Use `unknown` Instead of `any` for Untyped Data

When data shape is not known at compile time, use `unknown` and narrow:

```typescript
// GOOD
function parseConfig(raw: unknown): ProjectConfig {
  if (typeof raw !== 'object' || raw === null) {
    throw new Error('Config must be an object');
  }
  // Narrow further or use a validation library (Zod, etc.)
}

// BAD
function parseConfig(raw: any): ProjectConfig {
  return raw; // no safety at all
}
```

##### Index Signatures and Record Types

When you need dynamic keys, be explicit about the value type:

```typescript
// GOOD — clear contract
type TemplateVariables = Record<string, string | number | boolean>;

// GOOD — when you need to distinguish known from dynamic keys
interface EnhancedContextData extends ContextData {
  [computedKey: string]: string | number | boolean | undefined;
}

// BAD — erases all type information
const data: any = { ...baseData };
```

##### Prefer Interfaces for Object Shapes, Type Aliases for Unions

```typescript
// Interfaces — extendable, good for object shapes
interface ProjectConfig {
  name: string;
  version: string;
}

// Type aliases — good for unions, intersections, mapped types
type BuildTarget = 'electron' | 'mcp-server' | 'core';
type Nullable<T> = T | null;
```

##### Const Assertions and Literal Types

Prefer `as const` objects over TypeScript enums:

```typescript
// GOOD
const LogLevel = {
  Debug: 'debug',
  Info: 'info',
  Warn: 'warn',
  Error: 'error',
} as const;

type LogLevel = (typeof LogLevel)[keyof typeof LogLevel];
// Result: 'debug' | 'info' | 'warn' | 'error'

// AVOID — TypeScript enums have runtime behavior and quirks
enum LogLevel { Debug, Info, Warn, Error }
```

#### Function Signatures

- **Always annotate return types on exported functions.** TypeScript can infer return types, but explicit annotations catch accidental changes and serve as documentation.
- **Use `readonly` for parameters that should not be mutated.**
- **Prefer named parameters (via object destructuring) when a function takes 3+ parameters.**

```typescript
// GOOD
export function buildContext(
  config: Readonly<ProjectConfig>,
  options: { includeMetadata: boolean; format: OutputFormat }
): ContextResult { /* ... */ }

// BAD — positional params are hard to read at call sites
export function buildContext(
  config: ProjectConfig, includeMetadata: boolean, format: string
) { /* ... */ }
```

#### Generics

Use generics to write reusable code without losing type information:

```typescript
// GOOD — caller gets back the type they put in
function getOrDefault<T>(map: Map<string, T>, key: string, fallback: T): T {
  return map.get(key) ?? fallback;
}

// BAD — type information lost
function getOrDefault(map: Map<string, any>, key: string, fallback: any): any {
  return map.get(key) ?? fallback;
}
```

Constrain generics when appropriate:

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

#### Error Handling

- Type your errors. Use discriminated unions for expected error cases rather than throwing strings.
- Use `Result` patterns for operations that can fail predictably:

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

- Catch blocks: the caught value is `unknown` in strict mode. Narrow before using:

```typescript
try { /* ... */ } catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  // ...
}
```

#### Project Structure Conventions

- Shared types go in `packages/core/src/types/` (for the monorepo) or `src/lib/types.ts` (for single-package projects).
- Use `tsx` scripts for migrations.
- Reusable logic in `src/lib/utils/shared.ts` or `src/lib/utils/server.ts`.

##### tRPC Routers (when enabled)

- Routers in `src/lib/api/routers`, composed in `src/lib/api/root.ts`.
- Use `publicProcedure` or `protectedProcedure` with Zod for input validation.
- Access from React via `@/lib/trpc/react`.

#### Naming Conventions

- **Types/Interfaces**: PascalCase (`ProjectConfig`, `TemplateExpression`)
- **Variables/Functions**: camelCase (`processTemplate`, `enhancedData`)
- **Constants**: UPPER_SNAKE_CASE for true constants, camelCase for const references
- **Type parameters**: Single uppercase letter for simple cases (`T`, `K`), descriptive PascalCase for complex ones (`TInput`, `TOutput`)
- **Files**: kebab-case (`template-processor.ts`, `context-data.ts`)

#### Advanced Patterns (Use When Appropriate)

These are powerful but add complexity. Use them when they genuinely improve safety or DX, not for their own sake.

##### Conditional Types

Extract or transform types based on conditions:

```typescript
// Extract only the string-valued keys from a type
type StringKeys<T> = {
  [K in keyof T]: T[K] extends string ? K : never;
}[keyof T];
```

##### Mapped Types

Transform all properties of a type systematically:

```typescript
// Make all properties optional and nullable
type Draft<T> = {
  [K in keyof T]?: T[K] | null;
};
```

##### Template Literal Types

Useful for string patterns:

```typescript
type EventName = `on${Capitalize<string>}`;
type CSSProperty = `--${string}`;
```

#### Quick Reference: What to Use Instead of `any`

| Situation | Use Instead |
|---|---|
| Unknown JSON data | `unknown` + type guard or Zod |
| Object with dynamic keys | `Record<string, ValueType>` |
| Function that works on multiple types | Generics (`<T>`) |
| Third-party lib with bad types | Declaration file (`.d.ts`) |
| Spread into a new shape | Define the target interface explicitly |
| Callback with unknown signature | `(...args: unknown[]) => unknown` |
| "I'll figure out the type later" | `// TODO:` with `unknown`, never `any` |
