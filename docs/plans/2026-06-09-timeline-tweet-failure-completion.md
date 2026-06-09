# Timeline Tweet Failure Completion

## Status: Completed

## Context

`APIClient.getTweet` fetched a profile's latest timeline tweet for the swipe
card. It only called the completion handler after finding a tweet ID, logged
that ID, and skipped completion when request setup, transport, response data, or
timeline contents were unavailable. The swipe card should treat those cases as
missing optional embed data instead of waiting indefinitely or exposing tweet
identifiers in logs.

## Objectives

- Preserve embedded tweet rendering when the timeline lookup returns a tweet ID.
- Complete missing request, transport, response-data, and empty-timeline paths
  with a harmless empty result.
- Avoid logging tweet identifiers from timeline lookups.
- Keep the swipe card from trying to load an embedded tweet for empty results.
- Extend static checks so these completion and privacy guardrails remain in
  place.

## Work Completed

- Made `APIClient.getTweet` verify response data exists before JSON parsing.
- Added an empty fallback result and completed after parsing whether or not a
  tweet ID was found.
- Completed request setup and transport failures with `completion(result: "")`.
- Removed tweet identifier logging from the timeline lookup.
- Added static checks for the timeline completion paths and empty-result card
  guard.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`

## Xcode Notes

`xcodebuild` may be unavailable on non-macOS hosts. The repository `make check`
wrapper still runs the iOS build when `xcodebuild` is available locally.

## Follow-Up Candidates

- Add a visible placeholder state when no embeddable timeline tweet is
  available.
- Add simulator verification notes for empty timeline and transport failure
  responses when the legacy TwitterKit setup is available.
