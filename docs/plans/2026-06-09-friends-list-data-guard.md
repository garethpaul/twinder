# Friends List Data Guard

Status: Completed

## Context

`APIClient.Search` requests Twitter friends-list data and parses the response
into swipe-card `Tweep` records. The legacy code already guarded the current
Twitter session and malformed user records, but it still parsed the response
when the transport callback returned without response data. It also printed the
current Twitter username while building the request.

## Plan

- Require the friends-list callback to confirm both a missing transport error
  and non-empty response data before JSON parsing.
- Keep malformed or unavailable friends-list responses on the existing empty
  result fallback path.
- Remove username console logging from friends-list request setup.
- Extend `scripts/check_ios_contracts.py` so future edits keep the response
  data guard and avoid username logging.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

On this non-macOS host, `make verify` runs the static checks and skips the Xcode
build because `xcodebuild` is unavailable.
