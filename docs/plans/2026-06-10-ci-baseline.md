# CI Baseline

Status: Completed

## Context

The repository had a local Python-backed `make check` static contract for the
legacy iOS project, but no hosted workflow ran it for pushes and pull requests.

## Changes

- Added a read-only GitHub Actions workflow for Python 3.10, 3.12, and 3.14.
- Pinned third-party actions to immutable commits and bounded job runtime.
- Extended the static contract checker and docs to protect the hosted gate.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_ios_contracts.py`
- `git diff --check`
