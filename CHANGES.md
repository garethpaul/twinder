# Changes

## 2026-06-09

- Guarded friends-list response parsing behind response-data presence and
  removed username console logging from request setup.
- Completed swipe-card timeline tweet lookups with an empty result when request,
  transport, response-data, malformed-JSON, or empty-timeline paths fail, and
  skipped embedded tweet loading for empty IDs.
- Extended static checker coverage for timeline tweet completion guards.
- Completed current-user profile image lookup failures instead of logging
  Twitter API error details or leaving callers waiting.
- Added static checker coverage for TweepPicture failure completions.
- Guarded friends-list request setup before using the current Twitter session
  username and extended static checker coverage.
- Guarded current-user profile image loading before using the Twitter session,
  remote image URL, decoded image data, or profile image outlet.
- Added static checker coverage for current-user profile image guardrails.
- Guarded Twitter login navigation so failed or cancelled TwitterKit logins do
  not enter the main profile flow or log auth details.
- Added static checker coverage for the login session guard.
- Guarded swipe-card profile data, profile image URL construction, decoded
  image assignment, and embedded tweet rendering before using remote Twitter
  data.
- Added static checker coverage for swipe-card remote-data guardrails.
- Guarded initial and replenished swipe-card creation before removing fetched
  Tweeps so short or empty API responses do not crash the card setup flow.

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
