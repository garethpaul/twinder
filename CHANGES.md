# Changes

## 2026-06-08

- Added a `make verify` static gate for plist, storyboard, asset, CocoaPods lock, and Tweep image parsing contracts.
- Guarded profile image JSON parsing in `TweepPicture` instead of force-unwrapping the parsed response.
- Documented the verification command for non-Xcode hosts.
