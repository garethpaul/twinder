---
title: "fix: Guard swipe-card image completion identity"
type: fix
date: 2026-06-13
---

# Guard Swipe-Card Image Completion Identity

## Status: Completed

## Context

`TweepPickerView` starts an asynchronous profile-image request and captures the
card strongly. Its completion assigns any successful image without confirming
that the card still represents the same profile URL. A late response can retain
an already-discarded swipe card until the request finishes or overwrite a card
whose model changed before completion.

## Requirements

- R1. Capture the swipe-card view weakly in the asynchronous image completion.
- R2. Assign a decoded image only while the card still represents the exact URL
  requested by that operation.
- R3. Preserve the existing optional URL and decoded-image guards.
- R4. Clear the card image before starting a request so reused or reassigned
  cards do not display stale content while loading.
- R5. Add static and hostile-mutation coverage for weak capture, URL identity,
  nil reset, and guarded assignment ordering.
- R6. Document that this prevents stale completion updates but does not cancel
  or coalesce the underlying legacy request.

## Scope Boundaries

This change does not replace `NSURLConnection`, alter cache or response limits,
change the card model lifecycle, or claim simulator/device verification on this
Linux host.

## Implementation Units

### U1. Bind Completion to Card Identity

- **Files:** `Twinder/TweepPickerView.swift`
- Clear the image, capture `self` weakly, promote it safely, compare the current
  model URL with the originally requested URL, then assign the decoded image.

### U2. Protect the Contract

- **Files:** `scripts/check_ios_contracts.py`
- Require weak capture, safe promotion, image clearing, URL identity, and
  assignment after both identity and image guards.

### U3. Document and Verify

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, this plan.
- Record portable checks, mutation results, and the unavailable native build.

## Risks

- Legacy Swift syntax must remain compatible with the existing project.
- Static contracts cannot prove UIKit lifecycle behavior; native build and
  simulator execution remain follow-up validation.
- The underlying network request continues after a card is released, although
  weak capture prevents the request from retaining or updating that card.

## Verification

- `python3 -B -c '...check_swipe_card_image_identity_guard()'`: passed the
  focused reset, weak-capture, model, URL, decode, and assignment-order checks.
- `/tmp/engineering-bar/mutate-twinder-card-image-identity.sh`: rejected six
  reset, capture, promotion, model, identity, and assignment mutations.
- `git diff --check`: passed.
- `make check`: passed 16 static contract groups and 17 workflow mutations;
  the build target truthfully reported that `xcodebuild` is unavailable.
- `make -C /tmp/engineering-bar/twinder-card-image-identity-external/repo
  check`: passed the same portable gate from an external temporary path.
- Native Xcode build and simulator execution: unavailable on this Linux host.
