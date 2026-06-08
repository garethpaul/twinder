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

Next priorities:

- Add setup notes for Xcode, CocoaPods, and legacy TwitterKit requirements
- Document current API limitations before any revival work
- Add broader tests or manual verification notes for like/skip persistence
- Modernize Swift in a dedicated compatibility pass

Contribution rules:

- One PR = one focused API, swipe UI, persistence, SDK, or documentation change.
- Do not commit credentials or harvested user profile data.
- Keep demo data clearly marked.
- Include simulator/device notes for interaction changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app handles social identities, profile images, and saved preferences.
Changes should avoid hidden profile collection, token exposure, or upload of
saved profiles without consent.

## What We Will Not Merge (For Now)

- Checked-in Twitter or Fabric credentials
- Captured user-profile datasets
- Hidden analytics or profile upload
- SDK rewrites without preserving the sample flow

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
