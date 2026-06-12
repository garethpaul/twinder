# Saved-Profile Context Guard

Status: Completed

## Problem

The saved-profile table exposes its managed object context as optional but
force-unwraps it in `apiRequest()`. If persistent-store initialization fails,
the app delegate intentionally leaves that context unavailable; opening the
saved-profile screen would then crash instead of showing an empty list.

## Plan

1. Unwrap the managed object context before executing the fetch.
2. Preserve the current empty-list fallback for a missing context or failed
   fetch without changing the table data contract.
3. Add a static contract that rejects reintroduction of the force unwrap and
   requires the guarded fetch path.
4. Document the behavior and verify normal, external, and mutation gates.

## Verification

- `make check` passed 15 static contract groups and 17 workflow mutations;
  Xcode reported the documented Linux-host skip.
- An external-working-directory Make invocation passed the same gates.
- Isolated mutations restoring the force unwrap and removing the Python cache
  ignore were rejected.
- `python3 -m py_compile scripts/check_ios_contracts.py` passed.
- `git diff --check` passed.

Modern Xcode compilation remains unclaimed because this historical project
depends on retired Fabric/TwitterKit binaries and an obsolete CocoaPods stack.
