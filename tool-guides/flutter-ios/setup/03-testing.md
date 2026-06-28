---
layer: tool-guide
tool: Flutter/iOS
docType: testing
description: How to run unit, widget, and integration tests on a physical iPad for a Flutter iOS app. Used by both new (greenfield) apps and Android-to-iOS migrations.
dateCreated: 20260628
dateUpdated: 20260628
---

# Flutter on iOS — Testing on iPad

This guide covers running automated tests and performing targeted manual checks on a physical iPad for a Flutter app. It applies to any Flutter iOS app — a brand-new one (including a basic app for testing) or one migrated from Android.

---

## Test Layer Overview

Flutter has three tiers of automated tests. Run all three before declaring the iOS build stable:

| Type | Command | What it tests | Speed |
|---|---|---|---|
| **Unit tests** | `flutter test test/` | Business logic, models, data layer | Fast |
| **Widget tests** | `flutter test test/` | Individual widget rendering and state | Fast |
| **Integration tests** | `flutter test integration_test/` on device | Full app flows on real hardware | Slow |

Integration tests on a physical iPad are the highest-confidence signal, as they exercise the real iOS runtime, GPU rendering, and native plugins.

---

## Step 1 — Connect the iPad

1. Connect the iPad to your Mac via USB
2. On the iPad, tap **Trust** when the "Trust This Computer?" dialog appears
3. In Xcode: **Window → Devices and Simulators** — confirm the iPad appears and shows "Connected"
4. If it shows "Disconnected" or a pairing error, run:

```bash
idevicepair pair        # from libimobiledevice (brew install libimobiledevice)
```

5. Verify Flutter sees the device:

```bash
flutter devices         # iPad should appear with its UDID
```

---

## Step 2 — Set Up Integration Tests

Integration tests live in a separate `integration_test/` directory at the project root.

**Add the dependency** (if not already present):

```yaml
# pubspec.yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
```

**Create `integration_test/app_test.dart`:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:your_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('App smoke tests', () {
    testWidgets('app launches and home screen renders', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Replace with a widget or text actually present on your home screen
      expect(find.byType(app.MyApp), findsOneWidget);
    });

    testWidgets('navigation to second screen works', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      await tester.tap(find.byKey(const Key('nav_to_detail')));
      await tester.pumpAndSettle();

      expect(find.byKey(const Key('detail_screen')), findsOneWidget);
    });
  });
}
```

---

## Step 3 — Run Tests on the Physical iPad

With the iPad connected:

```bash
flutter test integration_test/app_test.dart -d <device-id>
```

Or, if only one iOS device is connected:

```bash
flutter test integration_test/app_test.dart -d ios
```

Flutter automatically builds a debug IPA, installs it on the iPad, and runs the test suite. Results stream back to the terminal.

**iOS 14+ permission dialog**: On first launch, iOS shows a "Local Network" permission dialog. This is required for Flutter's DevTools connection. Tap **Allow**; it won't appear on subsequent runs.

---

## Step 4 — Running All Tests Together

To run unit, widget, and integration tests in a single pass:

```bash
# Unit + widget tests (no device needed)
flutter test test/

# Integration tests on iPad
flutter test integration_test/ -d ios
```

For CI pipelines, use `flutter drive` with a separate driver file if your CI infrastructure has a connected device or uses a cloud device farm (e.g., AWS Device Farm, Firebase Test Lab).

---

## Step 5 — Manual iPad-Specific Checks

Automated tests catch regressions; manual checks catch UX issues specific to the iPad form factor. Run through this checklist before every TestFlight release:

### Orientation

- [ ] Rotate to landscape: verify all screens reflow correctly using your `MediaQuery` / `LayoutBuilder` breakpoints
- [ ] No UI clipping, overlapping elements, or overflowing text in landscape

### Split View & Slide Over

- [ ] Open another app in Split View alongside your app
- [ ] Test your app at **compact width** (≤375pt) — it must be usable even in a narrow Slide Over panel
- [ ] Dismiss Split View and verify your app resumes correctly

### Keyboard

- [ ] Attach or display the software keyboard; confirm `Scrollable` widgets scroll to keep focused text fields visible
- [ ] Verify `resizeToAvoidBottomInset: true` is set (or handled) on all form screens
- [ ] Dismiss keyboard with the hardware key or swipe — verify no layout jump

### Safe Areas

- [ ] Check all screens on the iPad's display corners — no content hidden behind the rounded corners
- [ ] Verify `SafeArea` is applied on all top-level screens

### Dark Mode

- [ ] Switch iPadOS to Dark Mode in Settings → Display & Brightness
- [ ] Verify all screens use correct `CupertinoDynamicColor` values; no hardcoded hex colors that become unreadable in dark mode

### Apple Pencil / Pointer

- [ ] Test all tap targets — they should be at least 44×44pt per HIG minimum
- [ ] If your app has drag targets or drawing features, verify they respond to Pencil hover events

### Networking & Permissions

- [ ] Accept/deny location, camera, microphone, and notification permissions and verify graceful handling in each case
- [ ] Test on both Wi-Fi and (if possible) cellular to catch any hardcoded assumptions about network speed

---

## Step 6 — TestFlight Beta Testing

After passing automated and manual tests, distribute to a wider group via TestFlight:

1. Upload a new build: see **02-ios-build.md** — Step 7
2. In **App Store Connect → TestFlight**, invite testers by Apple ID or email
3. Testers install the **TestFlight** app (free on the App Store) and receive a build notification
4. Collect crash reports and feedback in App Store Connect → **Crashes** and **Feedback**
5. Each build expires after **90 days**; upload a new build with an incremented build number to extend the beta period

---

## Debugging Tools

| Tool | How to access | Use for |
|---|---|---|
| Flutter DevTools | `flutter run`, then open the URL printed in terminal | Widget inspector, performance, memory |
| Xcode Console | Xcode → **Window → Devices** → select device → open console | Native iOS logs, crash reports |
| Xcode Instruments | Xcode → **Open Developer Tool → Instruments** | Memory leaks, CPU profiling, Metal GPU |
| Crash logs on device | Settings → Privacy & Security → Analytics & Improvements → Analytics Data | Uncaught exceptions |

**Always test a release build** for performance profiling — debug builds have significant overhead:

```bash
flutter run --profile    # profile mode: release perf + DevTools attached
flutter run --release    # true release build
```

---

## Version History

- **2026-06-28** — Initial guide (as migration guide 04); reframed as a shared `setup/` testing guide serving both greenfield and migration paths.
