---
layer: tool-guide
tool: Flutter/iOS
docType: plugin-audit
description: How to audit pub.dev plugins and platform channels for iOS compatibility before migrating an Android Flutter app.
dateCreated: 20260628
dateUpdated: 20260628
---

# Flutter Android-to-iOS Migration — 01: Plugin & Platform Channel Audit

This guide covers Phase 1 of the migration: identifying and resolving every Android-specific dependency before writing any iOS-specific UI code.

---

## Step 1 — Run Diagnostic Commands

```bash
flutter doctor          # Confirms Xcode and iOS toolchain are connected
flutter pub outdated    # Flags plugins with newer versions (often with iOS fixes)
flutter pub deps        # Prints the full dependency tree
```

Run these before touching any code. Fix all `flutter doctor` warnings related to Xcode before proceeding.

---

## Step 2 — Check Each Plugin for iOS Support

For every plugin in `pubspec.yaml`, check its entry in `pubspec.yaml` (or on pub.dev):

```yaml
# In a plugin's own pubspec.yaml — look for ios: under platforms:
flutter:
  plugin:
    platforms:
      android:
        package: com.example.plugin
      ios:          # ← Must be present for iOS support
        pluginClass: ExamplePlugin
```

If the `ios:` key is absent, the plugin has no iOS implementation and will either fail silently or crash at runtime.

---

## Step 3 — The `_plus` Plugin Family

The most common fix for Android-only plugins is switching to the cross-platform `_plus` family, maintained by the Flutter and Dart community. These have full, tested iOS implementations:

| Replace this (Android-focused) | With this (`_plus` equivalent) |
|---|---|
| `device_info` | `device_info_plus` |
| `package_info` | `package_info_plus` |
| `share` | `share_plus` |
| `sensors` | `sensors_plus` |
| `battery` | `battery_plus` |
| `connectivity` | `connectivity_plus` |
| `path_provider` | `path_provider` (already cross-platform) |
| `image_picker` | `image_picker` (already cross-platform) |

After switching, run:

```bash
flutter pub get
cd ios && pod install
```

---

## Step 4 — Platform Channel Stubs

If your app uses `MethodChannel` calls for Android-specific APIs (e.g., `android.intent`, `android.media`, `android.telephony`), you must either:

**Option A — Add an iOS implementation** in `ios/Classes/YourPlugin.swift`:

```swift
// ios/Classes/YourPlugin.swift
import Flutter

public class YourPlugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "your_channel",
                                       binaryMessenger: registrar.messenger())
    let instance = YourPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "yourMethod":
      // iOS implementation here
      result("iOS response")
    default:
      result(FlutterMethodNotImplemented)
    }
  }
}
```

**Option B — Stub it out in Dart** using platform detection, so the feature gracefully degrades on iOS:

```dart
import 'package:flutter/foundation.dart';

Future<String?> callNativeFeature() async {
  if (defaultTargetPlatform == TargetPlatform.android) {
    return await _channel.invokeMethod('yourMethod');
  } else if (defaultTargetPlatform == TargetPlatform.iOS) {
    // Feature not available on iOS, return null or an iOS alternative
    return null;
  }
  return null;
}
```

**Critical rule**: Never use `Platform.isAndroid` as the *only* check without a corresponding iOS branch. Unhandled platforms produce runtime errors.

---

## Step 5 — Verify the Full Build

After resolving all plugin issues:

```bash
flutter build ios --no-codesign   # Dry-run build without needing a provisioning profile
```

This compiles the entire Dart + native iOS code and surfaces any remaining compilation errors without requiring an Apple Developer account. Fix all errors here before moving to **../setup/01-ios-design.md**.

---

## Version History

- **2026-06-28** — Initial guide
