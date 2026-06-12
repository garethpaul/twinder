# Profile Image Transport

Status: Completed

## Context

The shared legacy image helper accepted arbitrary URL schemes, downloaded on
the main operation queue, and decoded response bodies without validating HTTP
status, media type, size, or request duration.

## Changes

- Restricted profile image requests to HTTPS and a 15-second timeout.
- Moved network work off the main queue while preserving main-queue callbacks.
- Rejected non-success, non-image, oversized, and undecodable responses.
- Fixed the Makefile and hosted workflow contracts to use stable execution
  paths and runner versions.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_ios_contracts.py`
- Mutation checks for each image transport and CI contract
- `git diff --check`

Modern Xcode compilation is not claimed because the project depends on retired
Fabric/TwitterKit SDKs and a historical CocoaPods toolchain.
