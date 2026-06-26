# Person Profile Image Lifecycle

Status: Completed

## Problem

`PersonController` strongly captured itself across a Twitter profile lookup and
a subsequent image download. It retained no cancellable task, did not
invalidate callbacks when leaving or logging out, and did not verify that the
active Twitter session still represented the account that started the work.

## Decision

- Weakly capture the controller in both asynchronous stages.
- Dispatch the Twitter lookup completion to the main queue before reading or
  changing controller-owned lifecycle state.
- Own the URLSession image task and cancel it before replacement, when the
  controller leaves, and during deinitialization.
- Start a fresh generation when the same controller reappears after a cancelled
  navigation-away load.
- Bind every completion to a request generation and the originating Twitter
  screen name before applying the decoded image.

## Verification

- The portable lifecycle contract requires weak captures, main-queue lookup
  ownership, cancellation, generation matching, and current-account identity.
- Eleven hostile mutations remove each boundary and must be rejected.
- `make check` remains the canonical verification gate; a compatible Xcode 6
  environment and retired TwitterKit service access remain necessary for native
  runtime validation.
