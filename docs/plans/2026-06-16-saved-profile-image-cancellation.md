---
title: "fix: Cancel stale saved-profile image requests"
date: 2026-06-16
---

# Cancel Stale Saved-Profile Image Requests

## Status: Planned

## Context

Swipe cards own and cancel their profile-image tasks, but saved-profile table
cells only clear the old image and reject completions for a different index
path. Reused cells therefore leave obsolete network and decode work running,
and an older completion for the same row identity can still race a newer load.

## Requirements

- R1. Give each `TweepCell` ownership of its active optional
  `NSURLSessionDataTask`.
- R2. Cancel and clear the owned task before a replacement load and during
  `prepareForReuse()`.
- R3. Increment a cell-local request generation for replacement and reuse so
  older completions cannot finish a newer load for the same row.
- R4. Accept a returned task only while its generation is still current;
  otherwise cancel it immediately.
- R5. Clear task ownership only when the completion belongs to the current
  generation.
- R6. Preserve the existing HTTPS transport, timeout, response-size, status,
  media-type, decode, main-queue completion, index-path identity, and optional
  image guards.
- R7. Add mutation-sensitive static contracts, synchronized guidance, and
  truthful completed-plan evidence.

## Scope Boundaries

- Do not add request coalescing, retries, dependencies, or a new image-loader
  abstraction.
- Do not change image response limits, table layout, Core Data behavior, or
  swipe-card image ownership.
- Native Xcode build and simulator testing remain unavailable on this Linux
  host and must be reported as such.
- The successor PR will be stacked on open PR #6; neither pull request may be
  merged or closed without explicit authorization.

## Implementation Units

### U1. Own saved-profile image work

- **Files:** `Twinder/TweepCell.swift`, `Twinder/TableController.swift`
- Add cell lifecycle methods for beginning, adopting, and completing an image
  generation. Bind the table completion to those methods before applying the
  existing row identity and decoded-image checks.

### U2. Protect cancellation and generation ordering

- **Files:** `scripts/check_ios_contracts.py`,
  `docs/plans/2026-06-16-saved-profile-image-cancellation.md`
- Require replacement/reuse cancellation, task adoption, stale-task
  cancellation, generation-aware completion, weak cell capture, preserved
  index-path guards, and completed-plan evidence.

### U3. Document saved-profile task ownership

- **Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that reused saved-profile cells cancel obsolete image work and reject
  stale completions.

## Verification Plan

- Capture the pre-change evidence that `TableController` ignores the returned
  image task and `TweepCell` has no cancellation lifecycle.
- Run focused static contracts and repository/external-directory `make check`.
- Reject hostile task-ownership, replacement cancellation, reuse cancellation,
  generation, weak-capture, guidance, and plan-status mutations.
- Audit the exact diff, generated artifacts, conflict markers, modes,
  whitespace, and credential patterns before shipping.
- Capture one bounded exact-head hosted snapshot after push without polling.
