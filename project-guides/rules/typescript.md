---
description: TypeScript syntax rules, tRPC router guidelines, and strict typing standards
globs: ["**/*.ts", "**/*.tsx", "src/lib/api/**/*"]
alwaysApply: false
---

# TypeScript Rules

## TypeScript & Syntax
- Strict mode. Avoid `any`.
- Use optional chaining, union types (no TS enums — prefer `as const` objects or string literal unions).

## Structure
- Use `tsx` scripts for migrations.
- Reusable logic in `src/lib/utils/shared.ts` or `src/lib/utils/server.ts`.
- Shared types in `src/lib/types.ts`.

## tRPC Routers
- **enabled**: as needed
- Routers in `src/lib/api/routers`, compose in `src/lib/api/root.ts`.
- `publicProcedure` or `protectedProcedure` with Zod.
- Access from React via `@/lib/trpc/react`. 