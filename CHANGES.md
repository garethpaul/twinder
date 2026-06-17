# Changes

## 2026-06-17

- Saved-profile writes persist before publishing success. Liked profiles now
  fail closed when Core Data is unavailable, clean up failed inserts, and enter
  in-memory state only after a successful context save.

## 2026-06-16

- Reused saved-profile cells cancel obsolete image tasks and reject stale
  completions.
- Saved-profile selection validates table identity before opening Twitter.

## 2026-06-14

- Documented the historical Xcode project format, iOS 8.0/8.2 targets,
  CocoaPods 0.35.0, MDCSwipeToChoose 0.2.1, TwitterKit 1.2.0, Fabric 1.1.1,
  pre-modern Swift syntax, and retired-service compatibility boundary.

## 2026-06-13

- Built Twitter profile deep links from fixed URL components and an encoded
  screen-name query item, removing optional URL force unwraps.
- Replaced legacy swipe-card image connections with cancellable URLSession
  tasks owned by the card and cancelled on replacement or release.
- Added request-generation checks so older same-URL completions cannot clear or
  overwrite a newer card image load.
- Cleared swipe-card profile images before loading and weakly bound late image
  completions to the card's current profile URL before UI assignment.

## 2026-06-12

- Guarded the saved-profile Core Data fetch against an unavailable managed
  object context so persistent-store setup failures produce an empty table
  instead of a force-unwrap crash.
- Ignored Python bytecode caches produced by local contract compilation.

## 2026-06-10

- Guarded saved-profile table image loading against malformed URLs, failed
  decoding, and asynchronous results targeting reused cells.
- Restricted shared profile image downloads to bounded HTTPS requests, moved
  network work off the main queue, and validated status, media type, size, and
  decoded image data before UI callbacks.
- Made local checks independent of the caller's working directory and fixed the
  hosted runner and action release annotations to reviewed versions.
- Added a pinned, read-only GitHub Actions matrix for Python 3.10, 3.12, and
  3.14 that runs `make check` with credential-free checkout.
- Added dependency-free structural workflow tests that reject contradictory or
  relocated credential settings and other CI policy regressions.
- Extended the static contract checker and docs to require the hosted CI
  verification path.

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
