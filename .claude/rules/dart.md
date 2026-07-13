---
description: Dart language coding standards and conventions. Use when writing, modifying, or reviewing .dart files or pubspec.yaml.
paths:
  - "**/*.dart"
  - "**/pubspec.yaml"
  - "**/analysis_options.yaml"
---

### Dart Rules

#### General

* Target Dart 3.x (required for sound null safety and pattern matching). Never use the `// @dart=2.x` version comment to opt out of null safety.
* All code must be soundly null safe — Dart 3 does not support mixed-version programs with unsound null safety.
* When starting or auditing a Dart project, verify that `analysis_options.yaml` is present and that the required linting configuration (defined in this guide) is active. If missing, add it before proceeding.

#### Typing & Null Safety

- **Sound null safety is mandatory.** Never use `!` (null assertion) unless you can prove the value is non-null at that point; add an inline comment explaining why.
- Use `?` to express nullable types; use `late` only when a field is genuinely initialized before first use and cannot be set in the constructor.
- Prefer `Type?` over non-null with `late` unless deferred initialization is truly required.
- Use `required` for named parameters that have no sensible default.
- Avoid implicit dynamic — every variable, parameter, and return type should be explicitly typed or unambiguously inferred.
- Use `final` for variables that are not reassigned; use `const` for compile-time constants.

#### Code Style & Structure

- Follow [Effective Dart](https://dart.dev/effective-dart) style conventions.
- Formatter: Run `dart format` on all Dart files. Line length defaults to 80; adjust in `analysis_options.yaml` only if your team has a documented reason.
- Naming:
  - `UpperCamelCase` for classes, enums, typedefs, and type parameters.
  - `lowerCamelCase` for variables, parameters, and named constructors.
  - `lowercase_with_underscores` for libraries, packages, directories, and source files.
  - `SCREAMING_CAPS` is discouraged; prefer `const lowerCamelCase` for constants.
- One class (or closely related set of top-level declarations) per file.
- Order file members: constructors → named constructors → factory constructors → fields → getters/setters → methods → overrides → static members.

#### Static Analysis Configuration

Every project MUST include an `analysis_options.yaml`. Minimum baseline:

```yaml
include: package:lints/recommended.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    missing_required_param: error
    missing_return: error
    dead_code: warning

linter:
  rules:
    - always_declare_return_types
    - avoid_dynamic_calls
    - avoid_empty_else
    - avoid_print
    - avoid_relative_lib_imports
    - avoid_returning_null_for_future
    - avoid_slow_async_io
    - avoid_type_to_string
    - cancel_subscriptions
    - close_sinks
    - collection_methods_unrelated_type
    - discarded_futures
    - literal_only_boolean_expressions
    - no_adjacent_strings_in_list
    - prefer_const_constructors
    - prefer_const_declarations
    - prefer_final_fields
    - prefer_final_locals
    - unawaited_futures
    - unnecessary_statements
    - use_string_buffers
```

Add `dart_code_linter` as a dev dependency for cyclomatic complexity enforcement:

```yaml
dart_code_linter:
  metrics:
    cyclomatic-complexity: 20
    number-of-parameters: 4
    maximum-nesting-level: 5
  rules:
    - avoid-dynamic
    - avoid-passing-async-when-sync-expected
    - avoid-redundant-async
    - avoid-unnecessary-type-assertions
    - avoid-unnecessary-type-casts
    - avoid-unused-parameters
    - prefer-trailing-comma
```

#### Functions & Error Handling

- Small, single-purpose functions (prefer ≤ 20 lines).
- Use early returns (guard clauses) to reduce nesting depth.
- Never swallow exceptions silently. Every `catch` block must either re-throw, log and re-throw, or explicitly justify why swallowing is correct with an inline comment.
- Catch specific exception types; avoid bare `catch (e)` unless it's a top-level error boundary.
- Prefer typed `Result` patterns (using `sealed` classes) for operations that fail predictably, rather than throwing exceptions for control flow:

```dart
sealed class Result<T> {
  const Result();
}

final class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}

final class Failure<T> extends Result<T> {
  final String message;
  const Failure(this.message);
}
```

#### Modern Dart Patterns

- Use `switch` expressions and `pattern matching` (Dart 3+) for exhaustive handling of sealed classes and records.
- Use `records` for lightweight, anonymous data bundles with a fixed number of typed fields.
- Use `sealed` classes for exhaustive, compiler-enforced type hierarchies (replaces manual `is`-chain checks).
- Prefer `extension` methods for adding behavior to existing types without subclassing.
- Use `Iterable` lazy methods (`map`, `where`, `fold`) over imperative loops where the intent is clear; avoid chaining more than 3–4 transformations without assigning intermediates.
- Use `StringBuffer` for building strings in loops; avoid `+` concatenation inside loops.
- Prefer `List.generate`, `Map.fromEntries`, and `Set.from` constructors over imperative population patterns.

#### Asynchronous Code

- Always `await` Futures or assign them intentionally; `unawaited_futures` lint catches accidental fire-and-forget.
- Mark fire-and-forget calls explicitly with `unawaited()` (from `dart:async`) so intent is documented and the lint is satisfied.
- Use `Stream` for continuous data; use `Future` for one-shot async results.
- Avoid `async` on a function that only returns a value — omit `async` if no `await` is needed.
- Cancel `StreamSubscription`s and close `StreamController`s in `dispose()` or equivalent cleanup.

#### Testing & Quality

- Write tests alongside implementation under the `test/` directory, mirroring the `lib/` structure.
- Use the `test` package exclusively; the `flutter_test` wrapper re-exports it for Flutter projects.
- Prefer small, focused unit tests. Integration tests go in `integration_test/`.
- Use `group()` to organize related tests; keep test file names matching the file under test with a `_test.dart` suffix.
- Use `mockito` or `mocktail` for mocking; prefer `mocktail` in new code (no code generation required for basic mocks).
- Static analysis is a merge blocker: zero `dart analyze` errors before merging. Treat warnings as errors in CI.

#### Dependencies & Imports

- Manage dependencies with `dart pub` (for pure Dart) or `flutter pub` (for Flutter).
- Pin direct dependency versions in `pubspec.yaml`; use `^` ranges only when automated upgrade PRs are in place.
- Group imports: Dart SDK (`dart:`) → Flutter/third-party (`package:`) → relative (`../`). Use `dart format` or an IDE plugin to enforce order automatically.
- No wildcard imports (`import 'package:foo/foo.dart' show everything`). Import only what you need, or use the library's top-level import.
- Use `show` or `hide` to resolve name collisions rather than aliasing the entire import.
