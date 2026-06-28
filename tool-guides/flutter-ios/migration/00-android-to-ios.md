---
layer: tool-guide
tool: Flutter/iOS
docType: migration-overview
description: Overview and entry point for migrating an existing Android-targeted Flutter app to also build and run on iOS. Read this first to determine which guide you need.
dateCreated: 20260628
dateUpdated: 20260628
---

# Flutter Android-to-iOS Migration — Overview

This is the entry point for migrating an existing Android-targeted Flutter/Dart app to also build and run on iOS, **retaining the cross-platform codebase as much as possible**. Read the guide selection table below to find the right document for your task, rather than loading all guides into context.

> **Greenfield, not migrating?** If you are creating a new iOS app (e.g. a basic app for testing) rather than migrating an existing Android one, skip this file. Read `../setup/` directly — you only need the migration-specific plugin audit (below) when you have an existing Android plugin set to reconcile.

The migration reuses the shared delivery guides under `../setup/` (design, build, test) and adds one migration-only concern: auditing your existing Android plugins and platform channels for iOS support.

## Guide Selection

| I need to... | Read this guide |
|---|---|
| Understand the overall migration process and code-sharing philosophy | **This file** (sections below) |
| Audit plugins, platform channels, and cross-platform code | **01-plugin-audit.md** (migration-only) |
| Apply iOS HIG design principles and Cupertino widgets | **../setup/01-ios-design.md** |
| Configure Xcode, signing, icons, and build the IPA | **../setup/02-ios-build.md** |
| Test on a physical iPad (unit, widget, integration, manual) | **../setup/03-testing.md** |

### For AI Agents: Which Guide to Load

- **Plugin or platform channel fails on iOS**: Load **01-plugin-audit.md** (compatibility audit, `_plus` family, channel stubs) — the only migration-specific guide
- **Adding a feature that needs iOS-specific UI**: Load **../setup/01-ios-design.md** (Cupertino widget mapping, adaptive iPad layout)
- **Build errors, Xcode configuration, signing**: Load **../setup/02-ios-build.md** (workspace setup, provisioning, IPA export)
- **Writing or running tests on iPad**: Load **../setup/03-testing.md** (integration test setup, iPad-specific manual checks)
- **Starting the migration from scratch**: Read **this file** first, then proceed in order: plugin audit (01) → design (`../setup/01`) → build (`../setup/02`) → test (`../setup/03`)

You should rarely need more than one guide per task. This overview provides the foundational knowledge and code-sharing philosophy that all other guides assume.

---

## Cross-Platform Code Preservation Philosophy

Flutter's architecture means roughly **95% of your Dart code is reused without modification**. The following layers are entirely untouched during an iOS migration:

- All business logic, state management (Bloc, Riverpod, Provider, etc.), and domain models
- All Dart-only packages (no native code)
- Network, storage, and API layers
- Navigation routing logic — only the *animation style* changes (`CupertinoPageRoute` vs `MaterialPageRoute`)

The only code that diverges is:

1. **UI widget selection** — swapping Material widgets for Cupertino equivalents at the presentation layer
2. **Platform channel implementations** — adding Swift/Objective-C counterparts for Android-only native calls

Using a widget abstraction layer (a factory function or `Platform.isIOS` checks) keeps even this divergence minimal and co-located. See **../setup/01-ios-design.md** for the recommended pattern.

---

## Migration Phases Overview

```
Phase 1 — Audit        Phase 2 — Design       Phase 3 — Build        Phase 4 — Test
─────────────────      ─────────────────      ─────────────────      ─────────────────
• Plugin iOS compat    • Cupertino widgets    • Xcode workspace      • Unit / widget
• Platform channels    • HIG compliance       • Signing & certs      • Integration tests
• flutter doctor       • Adaptive iPad UI     • Icons & launch         on iPad
                       • SafeArea / themes    • IPA export           • Manual iPad checks
                                                                     • TestFlight beta
```

---

## Prerequisites

Before starting Phase 1, ensure you have:

- A **Mac with Xcode** (latest stable) — Apple's toolchain is required; no substitute exists for iOS builds
- An **Apple Developer Program account** ($99/year) for signing and distribution
- **CocoaPods** installed: `sudo gem install cocoapods`
- Your existing Flutter project open and passing `flutter doctor` with no critical warnings

Flutter's iOS support is enabled by default in any existing Flutter project — no separate SDK is needed.

---

## Common Pitfalls (Quick Reference)

| Pitfall | Problem | Fix |
|---|---|---|
| Opening `.xcodeproj` instead of `.xcworkspace` | CocoaPods dependencies not loaded | Always open `ios/Runner.xcworkspace` |
| Skipping `pod install` after adding plugins | Build errors on native dependencies | Run `cd ios && pod install` after `flutter pub get` |
| Android-only plugins with no iOS entry | Silent failure or crash at runtime | Audit `pubspec.yaml`; switch to `_plus` variants (see **01-plugin-audit.md**) |
| Omitting `SafeArea` wrapper | UI clipped by notch or home indicator | Wrap all top-level content in `SafeArea` |
| Missing `PrivacyInfo.xcprivacy` | App Store rejection (required since 2024) | Add privacy manifest in Xcode (see **../setup/02-ios-build.md**) |
| Using `Platform.isAndroid` without iOS branch | Feature silently disabled on iOS | Always pair with an `else if (Platform.isIOS)` or stub |
| Not incrementing build number | TestFlight / App Store upload rejected | Bump `version` in `pubspec.yaml` before each upload |
| Testing only in portrait on iPad | UI breaks on rotation or Split View | Test all orientations and window sizes (see **../setup/03-testing.md**) |

---

## Resources

- [Flutter iOS deployment docs](https://docs.flutter.dev/deployment/ios)
- [Flutter Cupertino widget catalog](https://docs.flutter.dev/ui/widgets/cupertino)
- [Flutter adaptive & responsive design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Flutter integration testing](https://docs.flutter.dev/testing/integration-tests)
- [Apple Human Interface Guidelines — iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios)
- [Apple Human Interface Guidelines — iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados)

---

## Version History

- **2026-06-28** — Initial guide created from Android-to-iOS Flutter migration research; restructured to reference the shared `../setup/` core (design, build, test) and retain only the plugin audit as migration-specific.
