## Twinder Vision

Twinder is a legacy iOS app that uses TwitterKit, Fabric, CocoaPods, Core Data,
and swipe-card interactions to browse and save Twitter profiles.

The repository is useful as a historical sample for Twitter-authenticated API
calls, profile-card UI, local saved-profile storage, and simple social app
prototyping.

The goal is to preserve the sample while making SDK age, credentials, and
social-profile privacy boundaries explicit.

The current focus is:

Priority:

- Preserve the swipe-card profile browsing flow
- Keep Fabric/TwitterKit setup documented as legacy
- Store saved profiles locally unless a backend is explicitly added
- Avoid committing API keys, tokens, or captured profile datasets
- Guard Twitter API JSON parsing before using tweet IDs or profile-image data
- Guard Twitter sessions before friends-list request setup
- Guard friends-list responses before parsing and avoid logging Twitter
  usernames
- Skip malformed Twitter API records instead of crashing
- Avoid force-unwrapping remote profile image URLs or decoded image data
- Keep reused saved-profile rows from displaying stale asynchronous images
- Reused saved-profile cells cancel obsolete image tasks and reject stale
  completions.
- Keep root profile image callbacks weakly captured, generation-bound,
  selected-profile-bound, and cancelled when hidden.
- Reused saved-profile cells remove owned overlays before reconfiguration.
- Saved-profile selection validates table identity before opening Twitter.
- Saved-profile writes persist before publishing success. Use an isolated
  context, and bind optional legacy fields before use.
- Keep swipe cards from retaining or displaying stale asynchronous images
- Keep embedded tweet callbacks from retaining or mutating detached swipe cards
- Cancel replaced or released swipe-card image tasks and reject older same-URL
  request generations
- Encode Twitter profile deep-link query values, validate the ASCII handle
  alphabet and length, and fail closed when the route cannot be constructed or
  opened
- Require bounded HTTPS transport and validated responses for shared profile
  image downloads
- Guard current-user profile image loading before using session or image data
- Cancel and identity-bind current-user profile image callbacks across logout
  and navigation
- Complete current-user profile image lookup failures without logging Twitter
  API details
- Complete missing or failing timeline tweet lookups without logging tweet IDs
  or attempting embedded tweet rendering with empty results
- Guard swipe-card rendering before using remote profile or tweet data
- Guard initial swipe-card creation before removing fetched Tweeps
- Keep failed or cancelled TwitterKit logins on the login screen without
  logging auth details
- Avoid aborting on local Core Data store or save failures
- Keep failed favorite inserts isolated from the shared view context
- Keep GitHub Actions aligned with the local Python `make check` baseline
- Keep CI runners and third-party actions pinned to reviewed versions
- Keep hosted verification read-only, credential-free, and structurally
  protected against workflow policy regressions
- Keep historical Xcode, CocoaPods, TwitterKit, Fabric, iOS target, and Swift
  compatibility notes tied to checked-in metadata

Next priorities:

- Document current API limitations before any revival work
- Add broader tests or manual verification notes for like/skip persistence
- Modernize Swift in a dedicated compatibility pass

Contribution rules:

- One PR = one focused API, swipe UI, persistence, SDK, or documentation change.
- Do not commit credentials or harvested user profile data.
- Keep demo data clearly marked.
- Include simulator/device notes for interaction changes.
- Keep `.github/workflows/check.yml` in sync with the local static contract.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app handles social identities, profile images, and saved preferences.
Changes should avoid hidden profile collection, token exposure, or upload of
saved profiles without consent.

## What We Will Not Merge (For Now)

- Checked-in Twitter or Fabric credentials
- Captured user-profile datasets
- Console logging of Twitter usernames, tweet IDs, or API payload details
- Hidden analytics or profile upload
- SDK rewrites without preserving the sample flow

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
