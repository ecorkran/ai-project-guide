---
description: Testing standards and best practices. Use when writing, modifying, or reviewing tests. Covers test structure, naming, mocking patterns, assertion style, and coverage expectations.
paths: 
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/*.stories.*"
  - "src/stories/**/*"
---

### Testing Rules

#### General Testing Philosophy

- **Write tests as you go** - Create unit tests while completing tasks, not at the end
- **Not strict TDD** - AI development doesn't require test-first, but tests should accompany implementation
- **Focus on value** - Test critical paths, edge cases, and business logic; don't test trivial code

#### JavaScript/TypeScript Testing

##### Test Framework
- **Prefer Vitest** over Jest for new projects (faster, better ESM support, compatible API)
- Use `vitest` for unit and integration tests
- Use `@testing-library/react` for component testing

##### Test Organization
- Use a centralized `tests/` directory at the package level, not colocated `__tests__/` directories inside `src/`.

** Directory Structure Example**:
``` markdown
packages/my-package/
  src/
    index.ts
    services/
      myService.ts
  tests/
    services/
      myService.test.ts
    integration/
      serverLifecycle.test.ts
  package.json
  tsconfig.json
```

*Note: Ensure `tsconfig.json` includes `tests/` for type checking but excludes it from build output.*

##### Test File Naming
- Unit tests: `{module}.test.ts` — mirrors the source file name
- Integration tests: `{feature}.integration.test.ts` or grouped in `tests/integration/`
- Test fixtures: `tests/fixtures/` directory

##### What to Test
- **Critical paths**: User workflows, data transformations, business logic
- **Edge cases**: Null/undefined values, empty arrays, boundary conditions
- **Error states**: How code handles failures, invalid input, network errors
- **Not trivial**: Don't test framework code, getters/setters, or obvious pass-throughs

##### Test Coverage
- Aim for meaningful coverage, not 100% coverage
- Critical business logic: high coverage
- UI components: test interactions and state changes
- Utilities and helpers: comprehensive edge case coverage

#### Python Testing

##### Test Framework
- Use `pytest` (industry standard)
- Place tests in `tests/` directory or `test_*.py` files
- Use fixtures for test data and setup

##### Test Organization
```
project/
├── src/
│   └── module.py
└── tests/
    └── test_module.py
```

##### Assertions
- Use pytest assertions: `assert result == expected`
- Use pytest-parametrize for multiple test cases
- Mock external dependencies at boundaries

#### Best Practices

##### When to Write Tests
- ✅ **During implementation** - Write tests as you build features
- ✅ **After bug fixes** - Add tests to prevent regression
- ✅ **Before refactoring** - Tests verify behavior stays consistent
- ❌ **Not at the very end** - Waiting until feature is "done" leads to skipped tests

##### Test Quality
- **Arrange-Act-Assert** pattern: Set up → Execute → Verify
- **One concept per test**: Each test should verify one thing
- **Readable test names**: Test name should describe what's being tested
- **Avoid test interdependence**: Tests should run independently in any order

##### Mocking and Stubbing
- Mock external services (APIs, databases, file system)
- Don't mock internal business logic - test it directly
- Use dependency injection to make mocking easier

#### Running Tests

##### Commands
```bash
# JavaScript/TypeScript
pnpm test              # Run all tests
pnpm test:watch        # Watch mode
pnpm test:coverage     # Coverage report

# Python
pytest                 # Run all tests
pytest -v              # Verbose output
pytest --cov           # Coverage report
```

##### CI/CD Integration
- Tests should run automatically on commit/PR
- Build should fail if tests fail
- Don't skip failing tests - fix them or remove them

#### Storybook (Optional)

- **enabled**: false (by default)
- Use Storybook for component documentation and visual testing
- Place stories in `src/stories` with `.stories.tsx` extension
- One story file per component, showing variants and states
