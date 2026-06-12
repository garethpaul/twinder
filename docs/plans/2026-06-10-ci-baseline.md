# CI Baseline

Status: Completed

## Context

The repository had a local Python-backed `make check` static contract for the
legacy iOS project, but no hosted workflow ran it for pushes and pull requests.

## Objectives

- Run the static contracts across maintained Python versions.
- Keep workflow permissions read-only and runs bounded.
- Pin the runner and third-party actions to reviewed versions.
- Disable checkout credential persistence and test workflow policy structurally.

## Changes

- Added a read-only GitHub Actions workflow for Python 3.10, 3.12, and 3.14.
- Pinned third-party actions to immutable commits and bounded job runtime.
- Disabled checkout credential persistence and added 17 dependency-free hostile
  mutations covering credentials, permissions, triggers, actions, matrix
  coverage, runtime bounds, hosted Xcode, and the canonical gate.
- Extended the static contract checker and docs to protect the hosted gate.

## Verification

- `make check`
- `python3 -B scripts/test_workflow_contract.py`
- `python3 -B scripts/check_ios_contracts.py`
- `git diff --check`
