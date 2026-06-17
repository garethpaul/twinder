# Saved-Profile Write Transaction

## Status: Completed

## Priority

1. Prevent a like swipe from crashing when Core Data initialization failed.
2. Persist each inserted favorite before treating the profile as saved.
3. Keep failed writes out of in-memory saved state and success diagnostics.
4. Reject partial or reordered implementations with portable focused tests.

## Context

`TweepPickerViewController.saveTweep` force-unwraps its optional managed object
context, inserts a `FavTweets` object, and appends the profile to an in-memory
array without saving the context. A missing context therefore crashes, while a
normal-looking success can remain only in memory and disappear when the app
exits.

## Requirements

- R1. Guard the optional managed object context before insertion.
- R2. Validate the inserted entity type and populate the `FavTweets` object
  through the guarded context.
- R3. Attempt `NSManagedObjectContext.save` before appending to `savedTweeps`.
- R4. Delete the inserted object and return failure when persistence fails.
- R5. Return a success value from `saveTweep` and emit the existing success
  diagnostic only when the durable write succeeds.
- R6. Remove the liked-profile force unwrap while preserving swipe and card
  progression behavior.
- R7. Add mutation-sensitive contracts and maintenance documentation for
  context ownership, save ordering, rollback, result propagation, and completed
  verification evidence.

## Implementation Units

### U1. Make saved-profile writes transactional

**Files:** `Twinder/TweepPickerViewController.swift`

Change `saveTweep` into a Boolean operation. Guard the context, insert and
populate through that context, save before updating in-memory state, delete the
new object after a failed save, and return the observed outcome. Use optional
binding for the swiped profile and report success only for a true result.

### U2. Enforce the write boundary

**Files:** `scripts/check_ios_contracts.py`,
`scripts/test_saved_profile_write_contract.py`, `Makefile`

Add a focused source contract that requires the context guard, insertion,
field population, save attempt, failure cleanup, append ordering, Boolean
return, and guarded caller. Exercise isolated hostile mutations through the
canonical test target.

### U3. Record the persistence contract

**Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-17-saved-profile-write-transaction.md`

Document that a liked profile is reported and retained in memory only after a
successful Core Data save.

## Verification Plan

- Run the focused write contract and its hostile mutations.
- Run repository-root and external-working-directory `make check` under hard
  timeouts.
- Compile Python checkers and audit the exact intended diff, generated
  artifacts, conflict markers, large files, and secret-like values.
- Capture one bounded exact-head hosted PR and security snapshot after push.

## Scope Boundaries

- Do not modernize the Swift syntax, Core Data stack, retired Twitter/Fabric
  dependencies, CocoaPods artifacts, or card architecture in this change.
- Do not add migrations, duplicate detection, user-facing error UI, network
  calls, or claim native runtime coverage from Linux.
- Do not merge or close the existing stacked pull requests.

## Work Completed

- Guarded the optional managed object context before creating a favorite.
- Saved the populated object before appending the profile to in-memory state.
- Validated the inserted entity type, deleted failed or unexpected inserts,
  and returned a Boolean result to the swipe handler.
- Removed selected-profile force unwraps and limited the success diagnostic to
  successful durable writes.
- Added a focused contract module, eleven hostile mutations, canonical Make
  integration, and synchronized maintenance guidance.

## Verification Completed

- The focused saved-profile write contract passed; eleven hostile saved-profile write mutations were rejected.
- repository and external-directory `make check` passed all portable project
  and workflow contracts; Linux truthfully reported `xcodebuild` unavailable.
- generated-artifact and credential-pattern audits passed before shipment.
- No native Xcode build, simulator, Core Data runtime, Twitter session, or
  device persistence behavior was exercised.
