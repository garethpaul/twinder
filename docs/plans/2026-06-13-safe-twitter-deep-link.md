---
title: "fix: Build Twitter deep links safely"
type: fix
date: 2026-06-13
---

# Build Twitter Deep Links Safely

## Status: Planned

## Context

`twtrScreenName` currently concatenates an account name into a URL string and
force-unwraps the resulting optional URL for both capability checking and
opening. Unexpected query characters can alter the deep-link structure, and a
failed URL construction would crash instead of leaving the current screen
unchanged.

## Requirements

- R1. Build the `twitter://user` URL with Foundation URL components and one
  `screen_name` query item so the value is encoded as data rather than URL
  syntax.
- R2. Open the Twitter app only when URL construction succeeds and iOS reports
  that the URL can be opened.
- R3. Remove force unwraps and manual URL-string concatenation from the deep
  link helper.
- R4. Preserve the current behavior when Twitter is unavailable: remain in the
  app without adding browser fallback, alerts, or navigation changes.
- R5. Add portable fail-closed contracts and mutation coverage for component
  construction, query encoding, optional handling, and open ordering.

## Implementation Units

### U1. Construct the deep link structurally

- **Files:** `Twinder/DeepLinks.swift`
- Use `NSURLComponents` with the fixed `twitter` scheme and `user` host.
- Represent the screen name as an `NSURLQueryItem` and use optional binding for
  the resulting URL.
- Keep `canOpenURL` before `openURL` and reuse the same bound URL.

### U2. Preserve the behavior with portable contracts

- **Files:** `scripts/check_ios_contracts.py`
- Add a focused deep-link contract group and register it with the canonical
  repository gate.
- Reject string concatenation, URL force unwraps, missing query encoding,
  missing capability checks, or reversed open ordering.

### U3. Record the maintenance boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Document safe query construction, fail-closed routing, and the intentional
  absence of a web fallback.

## Verification

- Run the focused deep-link contract first, then the full local and
  external-working-directory `make check` gates under explicit timeouts.
- Exercise hostile source and checker mutations for the required construction,
  optional binding, capability check, call ordering, documentation, and plan
  completion contracts.
- Validate Python syntax, workflow contracts, structured project files,
  intended paths, generated artifacts, whitespace, and changed-line secret
  patterns.
- Report native Xcode build and simulator execution as unavailable on this
  Linux host; do not claim runtime validation that did not occur.

## Scope Boundaries

- Do not add web fallback, alerts, analytics, dependencies, or Twitter SDK
  changes.
- Do not change call sites, table-selection behavior, or unrelated legacy
  Swift syntax.
- Do not merge or close any pull request without explicit owner authorization.
