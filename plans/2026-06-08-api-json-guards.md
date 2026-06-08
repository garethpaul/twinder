# API JSON Guard Gate

## Problem

`TweepPicture` already guarded profile image parsing, but `API.swift` still
force-unwrapped Twitter timeline and friends-list responses. Empty timelines,
missing `users`, or incomplete user records could crash the app while browsing
profiles.

## TDD Evidence

1. Extended `scripts/check_ios_contracts.py` with static checks for
   `API.swift` Twitter JSON parsing.
2. Ran `make lint` before changing Swift and confirmed the new check failed on
   forced parsed-JSON unwraps.
3. Replaced the force unwraps with optional array/dictionary checks and reran
   the full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `git diff --check`
