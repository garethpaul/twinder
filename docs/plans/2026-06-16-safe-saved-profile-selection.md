---
title: "fix: Guard saved-profile table selection"
date: 2026-06-16
---

# Guard Saved-Profile Table Selection

## Status: Completed

## Context

`TableController.didSelectRowAtIndexPath` discards the delegate-provided index
path, asks the table for its selected row again, force-unwraps that optional,
force-casts an unused cell, and indexes the saved-profile array without a
bounds check. A transient selection or model/table mismatch can therefore
crash before the safe Twitter deep-link helper is reached.

## Requirements

- R1. Use the `NSIndexPath` supplied by the table delegate as the selection
  identity.
- R2. Reject section or row values that do not describe an existing saved
  profile before indexing the model.
- R3. Remove the unused selected-cell lookup and all selection-path force
  unwraps and casts.
- R4. Preserve the existing safe Twitter deep-link helper and saved-profile
  table/image behavior.
- R5. Add mutation-sensitive static coverage for delegate-path ownership,
  section and row bounds, and ordering before model access.
- R6. Synchronize repository guidance and truthful completed-plan evidence.

## Scope Boundaries

- Do not change Core Data fetching, row ordering, image loading, table layout,
  selection styling, or Twitter URL behavior.
- Do not introduce a new table model abstraction or dependency.
- Native Xcode build and simulator testing remain unavailable on this Linux
  host and must be reported as such.
- The successor PR will be stacked on open PR #7; neither pull request may be
  merged or closed without explicit authorization.

## Implementation Units

### U1. Fail closed on invalid selection identity

- **Files:** `Twinder/TableController.swift`
- Use the provided index path, require section zero, and require the row to be
  within `fav_tweeps.indices` before resolving the selected profile.

### U2. Enforce selection ownership and ordering

- **Files:** `scripts/check_ios_contracts.py`,
  `scripts/test_saved_profile_selection_contract.py`,
  `docs/plans/2026-06-16-safe-saved-profile-selection.md`
- Require delegate-path use, section and bounds guards before model indexing,
  absence of selected-row/cell force unwraps, and completed verification.

### U3. Document the saved-profile selection boundary

- **Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that saved-profile selection fails closed on stale or invalid table
  identity before opening Twitter.

## Verification Plan

- Prove the pre-change selection handler fails the new focused contract.
- Run focused static mutations and repository/external-directory `make check`.
- Reject missing section, missing row bounds, late guard, model-index bypass,
  selected-row force unwrap, guidance, and plan-status mutations.
- Audit the exact diff, generated artifacts, conflict markers, modes,
  whitespace, large files, and credential patterns before shipping.
- Capture one bounded exact-head hosted snapshot after push without polling.

## Verification Completed

- Pre-change source was rejected and hostile saved-profile selection mutations were rejected.
- repository and external-directory `make check` passed all static contracts
  and workflow mutations; Linux truthfully reported `xcodebuild` unavailable.
- generated-artifact and credential-pattern audits passed.
- No native Xcode build, simulator, Twitter app, Core Data runtime, credentials,
  or deployment was exercised.
