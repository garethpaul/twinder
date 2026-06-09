# Twinder Baseline

Status: Completed

## Scope

Preserve the legacy TwitterKit/Fabric/CocoaPods iOS sample while keeping its
project files, bundled resources, dependency lockfiles, and Twitter API parsing
guardrails statically verifiable.

## Completed Work

- Kept plist, storyboard, asset catalog, and CocoaPods lockfile integrity checks
  behind `make check`.
- Preserved Twitter API JSON parsing checks for timeline, friends-list, and
  profile-image data.
- Added canonical `docs/plans` coverage to the iOS static contract checker.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`
