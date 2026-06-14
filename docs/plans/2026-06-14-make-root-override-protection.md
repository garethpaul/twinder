---
title: "fix: Protect the Make repository root from overrides"
date: 2026-06-14
---

# Protect the Make Repository Root from Overrides

## Status: Planned

## Context

The Makefile derives `ROOT` from its own location, but a command-line variable
assignment can replace an ordinary `:=` definition. A hostile `ROOT` can
redirect the iOS contracts, workflow mutations, and optional Xcode build away
from the reviewed checkout.

## Requirements

- Protect `ROOT` with GNU Make's `override` directive while deriving it from
  the loaded Makefile path.
- Preserve `PYTHON ?= python3` and the existing static, workflow, and optional
  Xcode targets.
- Require exact protected root and Python override lines in the portable iOS
  checker.
- Pass local, external-directory, and hostile `ROOT=` full gates.
- Reject weakened root, checker, Python override, and plan-status mutations.
- Preserve all Swift, storyboard, CocoaPods, workflow, and documentation
  contracts without claiming native Xcode execution on Linux.

## Implementation Units

- **Makefile:** protect the internal root assignment only.
- **scripts/check_ios_contracts.py:** enforce exact root and Python lines and
  register this completed plan.
- **this plan:** record actual bounded verification before shipment.

## Verification Plan

- focused CI baseline contract and Python compilation
- full `make check` under a hard timeout
- external-directory and hostile `ROOT=<empty-directory>` full gates
- mutations for ordinary, recursive, `CURDIR`, first-Makefile, checker,
  Python-override, and plan-status regressions
- workflow YAML, plist/storyboard/assets, SVG XML, intended-path,
  generated-artifact, `git diff --check`, and changed-line secret audits

## Scope Boundaries

- Do not alter application source, dependencies, workflows, project files, or
  runtime behavior.
- Do not merge or close any stacked pull request without owner authorization.
