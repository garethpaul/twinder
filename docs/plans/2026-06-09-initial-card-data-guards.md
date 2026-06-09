# Initial Card Data Guards

Status: Completed

## Context

The swipe screen removed the first two fetched Tweeps unconditionally when the
API callback returned. Empty or one-item responses could therefore crash before
the existing "No more tweeps" fallback UI had a chance to render.

## Objectives

- Guard initial top-card and bottom-card creation before removing fetched
  Tweeps.
- Reuse the same guarded removal path when replenishing the bottom card after a
  swipe.
- Preserve the existing fallback background and like/skip controls.
- Extend the static iOS checker so inline unguarded `removeAtIndex(0)` card
  setup does not return.

## Work Completed

- Added `nextTweep()` to centralize optional Tweep removal.
- Guarded initial top-card and bottom-card setup with optional binding.
- Routed swipe replenishment through the same guarded helper.
- Updated README, VISION, CHANGES, and the static contract checker.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
