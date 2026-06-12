# CI Baseline

Status: Completed

## Context

The repository had a local Python-backed `make check` static contract for the
legacy iOS project, but no hosted workflow ran it for pushes and pull requests.

## Changes

- Added a GitHub Actions workflow that installs Python 3.12 and runs
  `make check`.
- Extended the static contract checker and docs so the hosted CI baseline stays
  visible.

## Verification

- `make check`
