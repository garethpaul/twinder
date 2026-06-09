# Timeline Tweet Completion

## Status: Completed

## Context

Swipe cards ask `APIClient.getTweet` for an embedded timeline tweet ID. The
helper only called its completion handler when a tweet ID was parsed, so
request setup failures, transport errors, missing response data, malformed
JSON, empty timelines, or tweets without `id_str` could leave the card waiting.

## Objectives

- Complete timeline tweet lookups with an empty result on every failure path.
- Avoid logging tweet identifiers from the lookup helper.
- Keep swipe-card rendering from calling TwitterKit with an empty tweet ID.
- Extend static checks so the completion and caller guards remain covered by
  `make check`.

## Work Completed

- Added an empty fallback result in `APIClient.getTweet`.
- Required response data before timeline JSON parsing.
- Completed request setup and transport/data failure paths with an empty
  result.
- Removed tweet-ID logging from the timeline helper.
- Guarded `TweepPickerView` against empty tweet lookup completions before
  calling `loadTweetWithID`.
- Updated static checks, README, VISION, and CHANGES.

## Verification

- Negative check before implementation:
  `make check` failed with
  `timeline tweet lookup must verify response data exists before JSON parsing`.
- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`

## Follow-Up Candidates

- Add a local placeholder for cards when embedded tweet lookup fails.
- Add simulator verification notes when a legacy Xcode/TwitterKit setup is
  available.
