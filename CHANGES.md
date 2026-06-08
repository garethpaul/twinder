# Changes

## 2026-06-08

- Added `make verify` and `make check` static gates for plist, storyboard, asset, CocoaPods lock, and Twitter JSON parsing contracts.
- Guarded profile image JSON parsing in `TweepPicture` instead of force-unwrapping the parsed response.
- Guarded timeline and friends-list JSON parsing in `API.swift` before reading tweet IDs and profile image URLs.
- Documented the verification command for non-Xcode hosts.
