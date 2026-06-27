# Root Profile Image Lifecycle

Status: Completed

## Problem

`ViewController` started a profile image request from `viewDidLoad`, strongly
captured itself, discarded the returned task, and accepted any later completion.
Navigation or selected-profile replacement could therefore retain the screen or
render stale imagery.

## Decision

Own the task and a request generation in the controller. Reload on appearance,
clear stale imagery, weakly capture the callback, require both the current
generation and selected image identity, and cancel on disappearance or release.

## Verification

The canonical static checker imports a dedicated lifecycle contract. Eight
hostile mutations independently remove weak capture, cancellation, generation,
identity, clearing, reload, or teardown ownership and must fail.
Canonical repository verification runs these checks through `make check`.
