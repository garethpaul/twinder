# Core Data Failure Guards

## Status: Completed

## Context

The legacy app stores saved profile data locally with Core Data. Its generated
store setup and save paths still force-unwrapped error details and called
`abort()` when the persistent store or context save failed. A local data-store
problem should not become an intentional crash path in this sample.

## Objectives

- Preserve local Core Data storage behavior when setup and saves succeed.
- Remove explicit `abort()` calls from Core Data failure paths.
- Avoid force-unwrapping `error.userInfo` while logging failures.
- Extend static checks to keep the non-crashing failure contract in place.

## Work Completed

- Replaced persistent-store setup aborts with non-crashing log messages.
- Replaced managed-object-context save aborts with non-crashing log messages.
- Added static checks that reject `abort()` and force-unwrapped `error.userInfo`
  in `AppDelegate.swift`.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add manual verification notes for like/skip persistence.
- Modernize the Core Data stack during a dedicated Swift compatibility pass.
