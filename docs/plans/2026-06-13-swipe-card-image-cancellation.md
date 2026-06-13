---
title: "fix: Cancel stale swipe-card image requests"
date: 2026-06-13
---

# Cancel Stale Swipe-Card Image Requests

## Status: Completed

## Context

Swipe cards now reject image completions for a different URL, but the legacy
`NSURLConnection.sendAsynchronousRequest` call cannot be cancelled. Released or
reloaded cards therefore keep consuming network and decode work, and reloading
the same URL can still accept an older completion.

## Requirements

- R1. Replace the legacy asynchronous connection helper with an HTTPS-only
  `NSURLSessionDataTask` that preserves timeout, cache, status, MIME, size,
  decode, and main-queue completion guards.
- R2. Return the optional task from `Picture.get` without breaking callers that
  intentionally ignore it.
- R3. Store the active task on `TweepPickerView` and cancel it before starting a
  replacement request and when the card is released.
- R4. Increment and capture a request generation so an older completion for the
  same URL cannot mutate a newer load.
- R5. Clear the owned task only when the completion still belongs to the active
  generation.
- R6. Preserve weak card capture, URL identity, optional image decoding, and
  main-thread UI assignment.
- R7. Extend static contracts and mutation coverage for task ownership,
  cancellation order, generation identity, and legacy API removal.

## Scope Boundaries

- Do not add caching, request coalescing, retry behavior, dependencies, or a
  new image-loading abstraction.
- Do not change image response limits or other profile-image call sites.
- Native Xcode build and simulator testing remain unavailable on this Linux
  host and must be reported as such.

## Implementation Units

### U1. Return a cancellable URLSession task

- **Files:** `Twinder/Picture.swift`
- Create, resume, and return an `NSURLSessionDataTask?` while preserving all
  existing transport and completion safeguards.

### U2. Own and invalidate card image work

- **Files:** `Twinder/TweepPickerView.swift`
- Cancel on replacement and deinitialization, and bind completions to a request
  generation in addition to URL identity.

### U3. Preserve repository contracts and guidance

- **Files:** `scripts/check_ios_contracts.py`, `README.md`, `SECURITY.md`,
  `VISION.md`, `CHANGES.md`
- Register the completed plan and enforce the cancellation lifecycle.

## Verification

- `python3 -B -c '...check_profile_image_loading_guards();
  check_swipe_card_image_identity_guard()'` passed the focused cancellation and
  generation contracts.
- Full local, external-directory, and space-containing-path `make check` runs
  passed 16 static groups and 17 workflow mutations; Xcode remains unavailable
  on Linux.
- Ten hostile mutations covering task return/resume, replacement/deinit
  cancellation, generation identity, task clearing, legacy API removal, and
  stale plan status were rejected.
- Python syntax, workflow contracts, SVG XML, `git diff --check`, generated-
  artifact, and focused secret reviews are included in final validation.
