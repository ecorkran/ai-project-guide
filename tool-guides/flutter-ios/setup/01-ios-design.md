---
layer: tool-guide
tool: Flutter/iOS
docType: ios-design
description: How to apply Apple Human Interface Guidelines and Cupertino widgets in a Flutter iOS app, including iPad adaptive layout. Used by both new (greenfield) apps and Android-to-iOS migrations.
dateCreated: 20260628
dateUpdated: 20260628
---

# Flutter on iOS — Design & Cupertino Widgets

This guide covers iOS design for a Flutter app: adopting Apple's Human Interface Guidelines (HIG) and the Flutter Cupertino widget library, while keeping the codebase cross-platform.

> **Greenfield vs migration.** The patterns here apply to any Flutter iOS app. If you are *migrating* an existing Android app, the Material→Cupertino mapping table below doubles as your conversion checklist; if you are building fresh, treat it as a catalog of the iOS-native widgets to reach for. Either way, business logic, data, and state are untouched — only the presentation layer is iOS-specific.

---

## The Adaptive Widget Strategy

To support both platforms from one codebase, detect the platform and swap key presentational widgets rather than maintaining separate UIs. Business logic, data, and state remain untouched. (For a migration, this also means you never rewrite working UI wholesale — you swap widgets in place.)

The recommended pattern is a helper function that returns the correct widget per platform:

```dart
import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';

Widget adaptiveSwitch(
  BuildContext context,
  bool value,
  ValueChanged<bool> onChanged,
) {
  if (Theme.of(context).platform == TargetPlatform.iOS) {
    return CupertinoSwitch(value: value, onChanged: onChanged);
  }
  return Switch(value: value, onChanged: onChanged);
}
```

Place these helpers in a shared `lib/widgets/adaptive/` directory so they are co-located and easy to find.

---

## Material → Cupertino Widget Mapping

| Android (Material) | iOS Equivalent (Cupertino) | Notes |
|---|---|---|
| `Scaffold` | `CupertinoPageScaffold` | iOS scaffold has no built-in FAB |
| `AppBar` | `CupertinoNavigationBar` | Use `CupertinoSliverNavigationBar` for large-title style |
| `BottomNavigationBar` | `CupertinoTabBar` + `CupertinoTabScaffold` | Required for Apple's tab-based nav pattern |
| `AlertDialog` | `CupertinoAlertDialog` | iOS dialogs have different button layout |
| `Switch` | `CupertinoSwitch` | Different animation and color |
| `Slider` | `CupertinoSlider` | |
| `TextField` | `CupertinoTextField` | Different cursor and selection handles |
| `CircularProgressIndicator` | `CupertinoActivityIndicator` | Spinning gear vs ring |
| `BottomSheet` (action menu) | `CupertinoActionSheet` | Apple's standard options menu |
| `ListTile` | `CupertinoListTile` | Available in Flutter 3.x+ |
| Pull-to-refresh | `CupertinoSliverRefreshControl` | |
| `Snackbar` | No direct iOS equivalent | Use brief overlay or banner (see HIG) |
| `MaterialPageRoute` | `CupertinoPageRoute` | Provides swipe-back gesture |

---

## Key iOS HIG Principles

### Navigation

- iOS users expect **swipe-back** (`CupertinoPageRoute` enables this automatically)
- Top-level navigation uses **bottom tabs** (`CupertinoTabBar`), not hamburger drawers
- Large-title navigation bars (`CupertinoSliverNavigationBar`) are standard for primary screens

```dart
CupertinoTabScaffold(
  tabBar: CupertinoTabBar(
    items: const [
      BottomNavigationBarItem(icon: Icon(CupertinoIcons.home), label: 'Home'),
      BottomNavigationBarItem(icon: Icon(CupertinoIcons.settings), label: 'Settings'),
    ],
  ),
  tabBuilder: (context, index) {
    return CupertinoTabView(
      builder: (context) => index == 0 ? const HomeScreen() : const SettingsScreen(),
    );
  },
)
```

### Safe Areas

Always wrap top-level content in `SafeArea`. This is non-negotiable on both iPhone and iPad — it respects the home indicator, notch, and Dynamic Island:

```dart
Scaffold(
  body: SafeArea(
    child: YourContent(),
  ),
)
```

### Typography & Color

- Use `CupertinoTextThemeData` for native iOS text styles
- Use `CupertinoDynamicColor` for colors that automatically adapt to Dark Mode:

```dart
const CupertinoDynamicColor adaptiveRed = CupertinoDynamicColor.withBrightness(
  color: CupertinoColors.systemRed,
  darkColor: CupertinoColors.systemRedDark,
);
```

### Action Menus

Replace Android `BottomSheet` action menus with `CupertinoActionSheet`:

```dart
showCupertinoModalPopup(
  context: context,
  builder: (_) => CupertinoActionSheet(
    title: const Text('Choose an action'),
    actions: [
      CupertinoActionSheetAction(
        child: const Text('Delete'),
        isDestructiveAction: true,
        onPressed: () { Navigator.pop(context); },
      ),
    ],
    cancelButton: CupertinoActionSheetAction(
      child: const Text('Cancel'),
      onPressed: () { Navigator.pop(context); },
    ),
  ),
);
```

---

## iPad Adaptive Layout

Flutter distinguishes *responsive* (fitting UI into available space) from *adaptive* (changing the UI paradigm for the space). iPads need both.

### Detecting a Tablet

```dart
bool isTablet(BuildContext context) =>
    MediaQuery.of(context).size.shortestSide >= 600;
```

### Two-Column / Master-Detail Layout

Apple recommends sidebar-based navigation on iPad. Use a `Row` with a fixed-width nav rail for large screens:

```dart
class AdaptiveLayout extends StatelessWidget {
  const AdaptiveLayout({super.key});

  @override
  Widget build(BuildContext context) {
    final tablet = isTablet(context);
    if (tablet) {
      return Row(
        children: [
          SizedBox(width: 320, child: const NavigationSidebar()),
          const VerticalDivider(width: 1),
          Expanded(child: const DetailView()),
        ],
      );
    }
    // Phone: single column with bottom tabs
    return const CupertinoTabScaffold(/* ... */);
  }
}
```

### LayoutBuilder for Fine-Grained Breakpoints

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth >= 900) return WideLayout();
    if (constraints.maxWidth >= 600) return MediumLayout();
    return NarrowLayout();
  },
)
```

### Split View & Slide Over

iPadOS allows two apps side-by-side. Your app may receive a compact horizontal size class even on an iPad. Always test at compact width — use `MediaQuery.of(context).size.width` rather than assuming "iPad = wide".

---

## Dark Mode

Verify your entire theme responds correctly by wrapping your app entry in a `CupertinoApp` (or using `theme` / `darkTheme` in `MaterialApp` with `CupertinoDynamicColor` values):

```dart
CupertinoApp(
  theme: const CupertinoThemeData(
    brightness: Brightness.light, // or use MediaQuery to auto-detect
  ),
  home: const MyHomePage(),
)
```

---

## Version History

- **2026-06-28** — Initial guide (as migration guide 02); reframed as a shared `setup/` design guide serving both greenfield and migration paths.
