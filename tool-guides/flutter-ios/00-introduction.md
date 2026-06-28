---
layer: tool-guide
tool: Flutter/iOS
docType: introduction
description: Entry point for building and shipping a Flutter app on iOS. Read this first to choose between the greenfield setup path and the Android-to-iOS migration path.
dateCreated: 20260628
dateUpdated: 20260628
---

# Flutter on iOS — Introduction

This is the entry point for getting a Flutter/Dart app building, running, and shipping on iOS (iPhone and iPad). It assumes a **Flutter codebase** — for native Swift/Objective-C work without Flutter, this is not the right guide.

There are two starting situations. Pick yours, then read only the guides that path points to — do not load everything into context.

## Which path are you on?

| Your situation | Start here |
|---|---|
| **Greenfield** — creating a new iOS Flutter app, or adding iOS to a project that has no Android baggage (e.g. a basic app for testing) | `setup/` — read **setup/01-ios-design.md** → **setup/02-ios-build.md** → **setup/03-testing.md** |
| **Migration** — you have an existing Android-targeted Flutter app and need it to also build and run on iOS | `migration/00-android-to-ios.md` first, then it routes you (it reuses the `setup/` guides plus a plugin audit) |

Both paths share the same delivery core: configuring Xcode, designing for iOS, and testing on a device live in `setup/`. The migration path adds one migration-only concern — auditing an existing Android plugin/platform-channel set (`migration/01-plugin-audit.md`) — and frames the shared guides in migration order.

## Directory map

```
flutter-ios/
  00-introduction.md          ← you are here (path selector)
  setup/                      ← shared delivery core, needed by BOTH paths
    01-ios-design.md          ← Cupertino widgets, HIG, iPad adaptive layout
    02-ios-build.md           ← Xcode, signing, icons, privacy manifest, IPA, TestFlight
    03-testing.md             ← unit/widget/integration tests + on-device iPad checks
  migration/                  ← migration-only
    00-android-to-ios.md      ← migration overview, philosophy, phase order
    01-plugin-audit.md        ← auditing an existing Android plugin set for iOS support
```

### For AI Agents: which guide to load

You should rarely need more than one guide per task.

- **Creating a basic iOS app from scratch / for testing**: start at **setup/02-ios-build.md** (Xcode + signing + run on device); pull in **setup/01-ios-design.md** if you need iOS-native UI and **setup/03-testing.md** to validate it.
- **Adding or fixing iOS-specific UI**: **setup/01-ios-design.md** (Cupertino mapping, adaptive iPad layout).
- **Build errors, Xcode config, signing, IPA, TestFlight**: **setup/02-ios-build.md**.
- **Writing or running tests / on-device iPad checks**: **setup/03-testing.md**.
- **Migrating an existing Android app**: **migration/00-android-to-ios.md** first.
- **A plugin or platform channel fails on iOS in a migration**: **migration/01-plugin-audit.md**.

## Prerequisites (both paths)

- A **Mac with Xcode** (latest stable) — Apple's toolchain is required; no substitute exists for iOS builds.
- An **Apple Developer Program account** ($99/year) for signing and distribution. (Not needed for a `--no-codesign` dry-run build or simulator runs.)
- **CocoaPods** installed: `sudo gem install cocoapods`.
- A Flutter project passing `flutter doctor` with no critical warnings.

Flutter's iOS support is enabled by default in any Flutter project — no separate SDK is needed.

## Resources

- [Flutter iOS deployment docs](https://docs.flutter.dev/deployment/ios)
- [Flutter Cupertino widget catalog](https://docs.flutter.dev/ui/widgets/cupertino)
- [Flutter adaptive & responsive design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Flutter integration testing](https://docs.flutter.dev/testing/integration-tests)
- [Apple Human Interface Guidelines — iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios)
- [Apple Human Interface Guidelines — iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados)

## Version History

- **2026-06-28** — Restructured from the original `ios/` migration-only guide set into a path-selecting introduction over a shared `setup/` core and a `migration/` path.
