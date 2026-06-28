---
layer: tool-guide
tool: Flutter/iOS
docType: ios-build
description: How to configure Xcode, signing, icons, and produce an IPA for a Flutter iOS app. Used by both new (greenfield) apps and Android-to-iOS migrations.
dateCreated: 20260628
dateUpdated: 20260628
---

# Flutter on iOS — Build Configuration

This guide covers configuring Xcode and Apple's toolchain to produce a signed, distributable iOS build from a Flutter app. It applies whether you are shipping a brand-new app (including a basic app for testing) or one migrated from Android — the Xcode, signing, icon, privacy-manifest, and IPA steps are the same.

---

## Step 1 — Open the Correct Workspace

```bash
open ios/Runner.xcworkspace
```

**Always open `.xcworkspace`, never `.xcodeproj`.** The workspace includes CocoaPods-managed dependencies. Opening the project file directly bypasses them, causing build failures.

---

## Step 2 — Set Project Identity (Runner Target → General Tab)

In Xcode, select the **Runner** target in the project navigator, then open the **General** tab:

| Field | What to set |
|---|---|
| **Display Name** | Your app's user-facing name |
| **Bundle Identifier** | Must match App Store Connect (e.g., `com.yourcompany.appname`) |
| **iOS Deployment Target** | Flutter 3.x requires **iOS 13.0** or later as the minimum |
| **Version** | User-facing version (e.g., `1.0.0`) — driven by `pubspec.yaml` |
| **Build** | Build number (e.g., `1`) — must be unique per App Store Connect upload |

**Canonical source of truth for version numbers is `pubspec.yaml`:**

```yaml
version: 1.0.0+1   # format: version_name+build_number
```

Flutter maps `version_name` → `CFBundleShortVersionString` and `build_number` → `CFBundleVersion`. Increment the build number before every upload to TestFlight or App Store.

---

## Step 3 — Signing & Capabilities

In Xcode → **Runner** target → **Signing & Capabilities** tab:

1. Check **Automatically manage signing**
2. Select your **Team** from the Apple Developer Program
3. Xcode will generate a provisioning profile and certificate automatically

For manual signing (CI/CD pipelines), use `fastlane match` to manage certificates and profiles in a git repository.

---

## Step 4 — App Icons

Replace Flutter's placeholder icons:

1. In Xcode's Project Navigator, select **Assets.xcassets** → **AppIcon**
2. Provide all required sizes. The only required upload to App Store Connect is **1024×1024 px** (no alpha channel, PNG or JPEG). Xcode generates device variants automatically if you use a single image.
3. Use a tool like [App Icon Generator](https://www.appicon.co) or the `flutter_launcher_icons` pub package to automate all sizes.

**Using `flutter_launcher_icons`:**

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_launcher_icons: ^0.14.0

flutter_launcher_icons:
  ios: true
  android: true
  image_path: "assets/icon/app_icon.png"
  min_ios_version: 13.0
```

```bash
dart run flutter_launcher_icons
```

---

## Step 5 — Launch Screen

Update `ios/Runner/Base.lproj/LaunchScreen.storyboard` for the splash screen. The default Flutter launch screen is a plain white screen with the Flutter logo — replace it with your brand.

Changes to the launch screen require a **full restart** (not hot reload) to appear, since iOS caches the launch screen aggressively.

---

## Step 6 — Privacy Manifest (Required Since 2024)

Apple requires a `PrivacyInfo.xcprivacy` file for any app using certain APIs (network access, file timestamps, `UserDefaults`, etc.). Without it, App Store submission will be rejected.

**To add it in Xcode:**
1. **File → New File → App Privacy** (search "privacy")
2. Add the file to the `Runner` target
3. Declare each API category your app uses and provide a reason code

Common entries:

```xml
<!-- PrivacyInfo.xcprivacy (XML excerpt) -->
<key>NSPrivacyAccessedAPITypes</key>
<array>
  <dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
      <string>CA92.1</string>
    </array>
  </dict>
</array>
```

Refer to [Apple's privacy manifest docs](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files) for the full list of API categories and reason codes.

---

## Step 7 — Build the App

### Development build (for iPad testing, no App Store)

```bash
flutter build ios --debug
```

Or install directly to a connected device:

```bash
flutter run --release     # builds and installs to connected device
```

### Ad-hoc / Development IPA

```bash
flutter build ipa --export-method development
```

The IPA is written to `build/ios/ipa/`. Install it to your iPad via Xcode → **Window → Devices and Simulators**, or via `ios-deploy`.

### App Store / TestFlight IPA

```bash
flutter build ipa --obfuscate --split-debug-info=symbols/
```

- `--obfuscate` renames Dart symbols to hinder reverse engineering
- `--split-debug-info` writes debug symbols separately (needed for crash symbolication)

The archive is in `build/ios/archive/MyApp.xcarchive`. Open it in Xcode Organizer → **Distribute App** → **App Store Connect** to upload.

### Command-Line Upload (CI/CD)

```bash
xcrun altool --upload-app \
  --type ios \
  -f build/ios/ipa/*.ipa \
  --apiKey YOUR_KEY_ID \
  --apiIssuer YOUR_ISSUER_ID
```

---

## Step 8 — TestFlight

After uploading a build:

1. Open **App Store Connect → TestFlight**
2. Select your build and add internal testers (e.g., your iPad's Apple ID)
3. Testers install the TestFlight app on the iPad and accept the invite
4. Builds expire after 90 days; upload a new build (incrementing build number) to extend testing

---

## Build Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `No provisioning profile` | Missing or expired profile | Enable "Automatically manage signing" and re-select Team |
| `Pod install failed` | CocoaPods version mismatch | `sudo gem update cocoapods && cd ios && pod install` |
| `Multiple commands produce ...` | Duplicate file reference in Xcode | Remove duplicate in Build Phases → Copy Bundle Resources |
| `The iOS Simulator deployment target is set to X.X` | Plugin has old minimum target | Set `IPHONEOS_DEPLOYMENT_TARGET = 13.0` in `ios/Podfile` |
| Archive succeeds but upload fails | Binary not signed for distribution | Use "App Store Connect" export method, not "Development" |

**Common `Podfile` fix for deployment target warnings:**

```ruby
# ios/Podfile — add inside post_install block
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '13.0'
    end
  end
end
```

---

## Version History

- **2026-06-28** — Initial guide (as migration guide 03); reframed as a shared `setup/` build guide serving both greenfield and migration paths.
