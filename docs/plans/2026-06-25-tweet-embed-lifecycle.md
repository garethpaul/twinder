# Tweet Embed Lifecycle Ownership

## Status: Completed

## Problem

Nested timeline and tweet-loading callbacks captured each swipe card strongly.
A swiped-away card could remain alive until both requests completed and then
receive a detached UI mutation.

## Design

- Weakly capture the card in both asynchronous callbacks.
- Invalidate pending tweet work when the card leaves its window.
- Require the request generation and profile handle to remain current.
- Dispatch the final TwitterKit view insertion to the main queue.

## Test-First Evidence

The new portable lifecycle contract failed against the original strong-capture
implementation. The source fix then passed the baseline plus six mutations that
remove weak captures, invalidation, identity checks, or main-queue dispatch.

## Verification

- `python3 scripts/test_tweet_embed_lifecycle_contract.py`
- `python3 scripts/check_ios_contracts.py`
- `make check`
- external-directory `make check`
- `git diff --check`

Native execution remains limited to a compatible Xcode 6-era environment and
the retired Fabric/TwitterKit service boundary.
