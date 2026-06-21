# Make Authority Isolation

## Status: Completed

## Context

The repository protected its derived root, but GNU Make still accepted caller-
controlled shell, startup-file, execution-mode, and Python expression state.

## Implementation

- Hardened the checked-in Makefile after its parse boundary without changing
  Swift, Xcode, CocoaPods, Fabric, TwitterKit, or application behavior.
- Public aliases use double-colon rules, embed reviewed root and Python command
  values before later non-override target variables can alter them, pin
  `/bin/sh -c` against later non-override shell assignments, and invoke
  `/usr/bin/xcodebuild` without PATH lookup.
- Python defaults to `/usr/bin/python3`; hosted matrices pass an absolute
  setup-python interpreter through a repository-owned `-I -B` launcher.
- Added an adversarial authority harness and pinned CI to `/usr/bin/make check`.

## Verification

- Repository and external-directory `make check` passed all static and mutation
  contracts; the native build retained its documented Linux skip.
- Authority tests cover 35 target/root/shell cases, a literal hostile Python
  path, command and environment Make-syntax rejection, command and environment
  `MAKEFILE_LIST` rejection, startup boundaries, caller `MAKEFLAGS`, and ten
  non-executing or error-ignoring modes.
- Executable regressions reject later single-colon recipe replacement, PATH
  shadowing, and hostile `sitecustomize.py`, while proving later non-override
  root, Python, and shell assignments cannot redirect checked-in commands.
- Workflow regressions parse mapping keys and reject quoted write permissions,
  custom shell/default/environment state, unreviewed steps, and any command
  other than the exact reviewed `make check` invocation.

## Scope Boundary

This is a local checked-in-Makefile boundary, not a sandbox for caller-supplied
Make programs. GNU Make startup files are parsed before repository checks, so
their parse-time code remains outside the local trust boundary. Later makefiles
that use GNU Make `override` directives likewise remain outside the local trust
boundary because they are caller programs with Make-level authority. absolute
Python executable selection is baked into recipes and uses isolated Python
startup; explicit alternate interpreters remain caller authority.

The workflow contract validates the checked-in workflow shape. It does not
claim that repository code can authenticate itself against a coordinated
caller change to both the workflow and the policy; that remains a code-review
and provider-required-check boundary.

Within that boundary, later non-override assignments cannot redirect the
reviewed root, Python command, or recipe shell, later single-colon recipes fail
closed, and PATH cannot replace the native Xcode launcher. This change does not
modernize or execute the legacy Xcode 6 application.
