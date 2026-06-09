# Changes

## 2026-06-09

- Guarded Twitter login navigation so failed or cancelled TwitterKit logins do
  not enter the main profile flow or log auth details.
- Added static checker coverage for the login session guard.
- Guarded swipe-card profile data, profile image URL construction, decoded
  image assignment, and embedded tweet rendering before using remote Twitter
  data.
- Added static checker coverage for swipe-card remote-data guardrails.

## 2026-06-08

- Replaced Core Data failure `abort()` paths with non-crashing log messages and
  static checker coverage.
- Guarded profile-card image URL creation and image decoding before assigning
  downloaded profile images.
- Added canonical `docs/plans` coverage to the static iOS contract checker.
- Added `make verify` and `make check` static gates for plist, storyboard, asset, CocoaPods lock, and Twitter JSON parsing contracts.
- Guarded profile image JSON parsing in `TweepPicture` instead of force-unwrapping the parsed response.
- Guarded timeline and friends-list JSON parsing in `API.swift` before reading tweet IDs and profile image URLs.
- Documented the verification command for non-Xcode hosts.
