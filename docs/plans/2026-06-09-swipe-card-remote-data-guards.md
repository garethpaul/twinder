# Swipe Card Remote Data Guards

## Status: Completed

## Context

The detail profile image path had guard coverage, but the main swipe card still
force-unwrapped selected profile data, remote profile image URLs, decoded image
data, and embedded tweet payloads. A malformed Twitter API record, invalid image
URL, failed image decode, or failed tweet lookup could crash the primary browse
flow.

## Objectives

- Preserve the swipe-card profile browsing flow.
- Guard selected `Tweep` data before using image, name, and screen-name fields.
- Guard profile image URL construction before starting image downloads.
- Guard decoded image data before assigning it to the card.
- Guard embedded tweet loading before rendering `TWTRTweetView`.
- Keep static checks covering the swipe-card remote-data contract.

## Work Completed

- Updated `TweepPickerView` to unwrap selected profiles, profile image URLs,
  decoded images, and loaded tweets with `if let`.
- Removed force unwraps for selected profile image, name, and screen-name data
  in the swipe-card view.
- Added static checker coverage for swipe-card remote-data guardrails.
- Updated README, VISION, and CHANGES to document the added guard coverage.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add a local placeholder image when swipe-card image downloads fail.
- Add empty-list handling before initial card creation when the API returns no
  usable profiles.
