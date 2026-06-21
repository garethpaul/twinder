# Make Authority Isolation

## Status: Completed

## Context

The repository protected its derived root, but GNU Make still accepted caller-
controlled shell, startup-file, execution-mode, and Python expression state.

## Implementation

- Hardened Make startup and every public target without changing Swift, Xcode,
  CocoaPods, Fabric, TwitterKit, or application behavior.
- Added an adversarial authority harness and pinned CI to `/usr/bin/make check`.

## Verification

- Repository and external-directory `make check` passed all static and mutation
  contracts; the native build retained its documented Linux skip.
- Authority tests cover 35 target/root/shell cases plus tool, startup, and mode
  rejection.

## Scope Boundary

This change does not modernize or execute the legacy Xcode 6 application.
