# Profile Image Loading Guards

## Status: Completed

## Context

The Twitter API JSON parsing paths were guarded, but profile-card rendering
still force-unwrapped the selected `Tweep`, the profile image URL, and decoded
image data. Invalid remote image URLs, failed downloads, or non-image responses
could crash the card view.

## Objectives

- Preserve the swipe-card profile browsing flow.
- Guard selected profile data before image loading.
- Guard profile image URL construction before network requests.
- Let image downloads fail without force-unwrapping decoded data.
- Keep static checks covering these remote-data guardrails.

## Work Completed

- Guarded `self.tweep` before profile image loading.
- Guarded `NSURL(string:)` before downloading profile images.
- Changed `Picture.get` to return optional decoded images.
- Guarded profile image assignment with `if let`.
- Extended `scripts/check_ios_contracts.py` and updated README, VISION, and
  CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add a local placeholder image when profile image downloads fail.
- Add manual verification notes for like/skip persistence.
