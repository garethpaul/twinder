# Login Session Guard

## Status: Completed

## Context

`LoginController` navigated to the main profile flow whenever TwitterKit called
the login completion block. Cancelled logins, failed authentication, or missing
sessions could therefore enter the app without a valid Twitter session.

## Objectives

- Preserve successful TwitterKit login navigation.
- Keep failed or cancelled TwitterKit logins on the login screen.
- Avoid force-unwrapping the optional login error.
- Add static checker coverage for the login navigation contract.

## Work Completed

- Updated `LoginController` to call the main-view segue only when TwitterKit
  returns a non-nil session and no error.
- Logged TwitterKit login errors without force-unwrapping them.
- Added static checker coverage for the login session guard.
- Updated README, VISION, and CHANGES to document the guard coverage.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Show an inline login error state instead of logging failed TwitterKit logins.
- Add simulator verification notes for the legacy TwitterKit login flow.
