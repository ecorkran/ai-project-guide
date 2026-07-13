---
description: Flutter application development standards and conventions. Use when writing, modifying, or reviewing Flutter widget files, state management code, navigation, or build configuration.
paths:
  - "**/*.dart"
  - "**/pubspec.yaml"
  - "**/analysis_options.yaml"
  - "android/**"
  - "ios/**"
---

### Flutter Rules

#### General

* Target the latest stable Flutter release. Check `flutter --version` when joining or auditing a project; update if more than one major stable behind.
* All projects must include `flutter_lints` in `dev_dependencies` and an `analysis_options.yaml` that extends it (see the Dart rules for the full baseline configuration).
* Address every build warning on each PR. Deprecated API usage and broken constraints become breaking changes in future Flutter releases.

#### Architecture

Follow the Flutter team's recommended layered architecture:

- **UI layer**: Widgets + ViewModels (MVVM). Widgets are "dumb" — they observe ViewModel state and dispatch user events. No business logic in widgets.
- **Data layer**: Repositories + Services. Repositories are the single source of truth for all app data; Services encapsulate external API or platform calls.
- **Domain layer (optional)**: Use-cases. Add only in large apps with complex logic shared across multiple ViewModels.

Unidirectional data flow is mandatory: data flows down from repository → ViewModel → widget; user events flow up from widget → ViewModel → repository.

```
lib/
  features/
    auth/
      data/          # repository, service, API models
      domain/        # use-cases (if needed)
      presentation/  # screens, view models, widgets
  shared/
    widgets/
    utils/
    constants/
  main.dart
```

Organize by **feature**, not by type (`screens/`, `models/`, `controllers/`). Feature-first keeps related code colocated and simplifies deletion of entire features.

#### Widgets

- Prefer `StatelessWidget` and `const` constructors. Reserve `StatefulWidget` for local UI-only state (animations, focus, text controllers).
- Extract reusable pieces into named widget classes, not private methods returning `Widget`. Widget classes benefit from Flutter's element rebuild optimization; method calls do not.
- Always use `const` where possible — it short-circuits the rebuild comparison and reduces garbage collection pressure.
- Pass `Key`s when widgets of the same type appear in lists or when the widget tree conditionally swaps between widget types of the same class.
- Never put navigation, dialogs, or snackbars in ViewModels or business logic. These are UI concerns that belong in the widget or a router callback.

#### State Management

Choose based on project scale:

| Scale | Recommended | Notes |
|---|---|---|
| Small (<10 screens) | `ChangeNotifier` + `provider` | Simple; ships in SDK |
| Medium (10–30 screens) | `riverpod` (Riverpod 3+) | Compile-time safety, no `BuildContext` dependency |
| Large / enterprise | `bloc` / `cubit` | Explicit state transitions; strong separation of concerns |

- In Riverpod: use `Notifier` and `AsyncNotifier` (not legacy `StateNotifierProvider` or `ChangeNotifierProvider`).
- Providers must only emit state. No navigation, dialogs, or snackbar calls inside providers.
- In BLoC: use `Cubit` for simple state; use `Bloc` only when explicit event objects add clarity.

#### Navigation

- Use `go_router` for navigation in all new projects. It supports deep linking, URL-based routing, and nested navigation out of the box.
- Define all routes in a central router file; never call `Navigator.push` directly in widget code.
- Use `ShellRoute` for persistent bottom navigation bars or drawers.
- Guard protected routes with `redirect` callbacks in the router, not ad-hoc checks in widgets.

#### Data & Immutability

- Use immutable data models. Generate `copyWith`, `==`, `hashCode`, and `toString` using `freezed` or `built_value`. Do not write these by hand.
- Use `json_serializable` or `freezed` for JSON serialization. Never manually write `fromJson`/`toJson` for complex models.
- Validate all data at the boundary (API response, user input) before it enters the domain layer.
- Use `Drift` (type-safe SQLite) for local persistence in offline-first apps. Avoid raw `sqflite` unless Drift is unsuitable.

#### Performance

- Use `const` constructors everywhere possible.
- Avoid rebuilding large subtrees: scope `Consumer`, `BlocBuilder`, or `Selector` to the smallest widget that needs the update.
- Use `ListView.builder` and `GridView.builder` for long lists — never `ListView(children: [...])` with many items.
- Avoid heavy computation on the main isolate. Move CPU-intensive work (JSON parsing, image processing) to a background isolate using `compute()` or `Isolate.spawn`.
- Profile with Flutter DevTools before optimizing. Don't guess; measure.
- Use `RepaintBoundary` to isolate frequently animating widgets from the rest of the tree.

#### Error Handling

Never let raw exceptions surface to the UI. Use a typed result pattern at the repository boundary:

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

- Wrap the entire app in a top-level `FlutterError.onError` handler and `PlatformDispatcher.instance.onError` for uncaught async errors.
- Report errors to a crash analytics service (e.g., Firebase Crashlytics, Sentry) in production.

#### Dependency Injection

- Use `get_it` (service locator) or `riverpod` providers for dependency injection. Never use globally accessible singleton objects.
- Register dependencies at app startup; pass them down via constructor injection or provider scope.
- Use abstract repository interfaces to allow swapping real implementations with fakes in tests.

#### Testing

Three required test layers:

1. **Unit tests** — every ViewModel, repository, and service class. No Flutter SDK dependency.
2. **Widget tests** — every screen and significant UI component. Use `WidgetTester`; mock all data dependencies.
3. **Integration tests** — critical user flows (auth, checkout, onboarding) running on a real device or emulator via `integration_test`.

Target ≥70% coverage on the domain and data layers. Use `flutter test --coverage` and fail CI when coverage drops below the established baseline.

#### CI/CD

Standard pipeline:

1. `flutter analyze` — zero errors is a merge blocker.
2. `dart format --output=none --set-exit-if-changed .` — enforce formatting.
3. `flutter test` — all unit and widget tests must pass.
4. Build release APK and IPA.
5. Upload to Firebase App Distribution or TestFlight for QA.
6. On release tag, submit to stores via Fastlane.

#### Dependency Selection (pub.dev)

When evaluating a package:

- Prefer packages with a **pub.dev "Flutter Favorite"** badge or high popularity score.
- Verify the package supports the current Dart / Flutter SDK constraint in your project.
- Check open issues for crashes or breaking-change warnings before adopting.
- Avoid packages with no release activity in >12 months unless they are intentionally stable and minimal.
- For small utilities, copy the relevant code directly rather than adding a full package dependency.

#### Naming Conventions

| Entity | Convention | Example |
|---|---|---|
| Files & directories | `snake_case` | `user_profile_screen.dart` |
| Classes, enums, typedefs | `UpperCamelCase` | `UserProfileViewModel` |
| Variables, parameters, methods | `lowerCamelCase` | `fetchUserProfile()` |
| Constants | `lowerCamelCase` (const) | `const defaultTimeout` |
| Screens | `*Screen` suffix | `LoginScreen` |
| ViewModels | `*ViewModel` suffix | `LoginViewModel` |
| Repositories | `*Repository` suffix | `UserRepository` |
| Services | `*Service` suffix | `AuthService` |
