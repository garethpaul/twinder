# Trusted Workflow Contract

## Status: Completed

## Problem

The three required `check` contexts were bound to the GitHub Actions app, but
their workflow YAML came from the pull-request head. A candidate could retain
the required matrix job names while replacing the command and its checked-in
validator, so green required checks did not independently prove the reviewed
workflow contract.

## Design

The repository now includes a `pull_request_target` workflow that GitHub loads
from the base revision. It checks out only the exact base SHA, downloads three
candidate files through the GitHub API as inert bytes, and executes only the
base-owned Python policy. The policy requires the candidate `check.yml` to
match the reviewed SHA-256 byte contract and requires candidate copies of the
trusted workflow and policy to equal their base versions.

This deliberately makes the trust root immutable through ordinary pull
requests. An intentional workflow-policy change therefore needs a separate
trusted base-maintenance operation followed by an update to the required-check
configuration. The initial bootstrap is manually reviewed because a newly
introduced `pull_request_target` workflow cannot execute from the candidate
branch before it exists on the base branch.

## Proof

- The local contract rejects 35 workflow mutations, including exact-command,
  extra-step, shell, environment, permission, Unicode, folded-scalar, literal
  scalar, comment, and YAML-anchor variants.
- The trusted-policy suite rejects command replacement, line wrapping, CRLF and
  comment rewrites, and candidate changes to either trust-root file.
- Actionlint validates both workflows, and the full repository `make check`
  exercises both mutation suites under isolated Python startup.
