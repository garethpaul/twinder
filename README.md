# twinder

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/twinder` is an Apple platform application or Objective-C/Swift sample. A simple application that showcases Fabric + Cocoapods

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (24), Swift (23), Objective-C (1).

## Repository Contents

- `README.md` - project overview and local usage notes
- `Podfile` - Apple platform dependency metadata
- `Fabric.framework` - source or example code
- `Podfile.lock` - Apple platform dependency metadata
- `SECURITY.md` - security reporting and disclosure guidance
- `Twinder` - source or example code
- `Twinder.xcodeproj` - Xcode project file
- `TwinderTests` - source or example code
- `TwitterKit.framework` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: Fabric.framework, Twinder, TwinderTests, TwitterKit.framework
- Dependency and build manifests: Podfile, Podfile.lock
- Entry points or build surfaces: Twinder.xcodeproj
- Test-looking files: TwinderTests/Info.plist, TwinderTests/TwinderTests.swift

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- CocoaPods if dependencies need to be installed

### Setup

```bash
git clone https://github.com/garethpaul/twinder.git
cd twinder
pod install
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `Twinder.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- Run `make check` for static project and Twitter API parsing checks. The build
  step runs Xcode only on hosts where `xcodebuild` is installed.

## Testing and Verification

- `make check` runs plist, storyboard, asset, CocoaPods lock, Twitter API JSON
  parsing, profile-image loading, swipe-card remote-data, login session, and
  Core Data failure-path contract checks.
- Completed maintenance plans live under `docs/plans` and are checked by
  `make check`.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and destination on macOS

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include Twinder/API.swift, Twinder/AppDelegate.swift, Twinder/LoginController.swift, Twinder/PersonController.swift, and 6 more.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include Fabric.framework/Versions/A/Headers/Fabric.h, Fabric.framework/Versions/A/Resources/Info.plist, Twinder/API.swift, Twinder/AppDelegate.swift, and 6 more.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include Fabric.framework/Versions/A/Resources/Info.plist, Twinder/API.swift, Twinder/Info.plist, Twinder/TweepPicture.swift, and 6 more.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include TwitterKit.framework/Versions/A/Headers/TWTRConstants.h.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include Fabric.framework/Versions/A/Resources/Info.plist, Twinder/API.swift, Twinder/Info.plist, Twinder/PersonController.swift, and 6 more.
- Review changes touching database, model, or persistence code; examples from the scan include Twinder/AppDelegate.swift, TwitterKit.framework/Versions/A/Headers/TWTRTweetTableViewCell.h, TwitterKit.framework/Versions/A/Headers/TWTRTweetViewDelegate.h.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-twinder-baseline.md` for the current static
  verification baseline.
- See `docs/plans/2026-06-08-profile-image-loading-guards.md` for profile-card
  image URL and decode guard coverage.
- See `docs/plans/2026-06-08-core-data-failure-guards.md` for non-crashing
  Core Data failure-path coverage.
- See `docs/plans/2026-06-09-swipe-card-remote-data-guards.md` for swipe-card
  remote profile and tweet rendering guard coverage.
- See `docs/plans/2026-06-09-login-session-guard.md` for TwitterKit login
  navigation guard coverage without logging auth details.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
