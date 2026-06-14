# Legacy Xcode And TwitterKit Setup Notes

## Status: Planned

## Context

The README currently tells contributors to use macOS, Xcode, and CocoaPods but
does not identify the historical versions committed to the repository. That can
mislead readers into expecting a current Xcode build or a functioning retired
TwitterKit service.

## Priority

Document the checked-in iOS, CocoaPods, swipe-card, TwitterKit, and Fabric
boundaries needed to understand or attempt historical reproduction.

## Requirements

- Record the iOS 8.0/8.2 deployment targets and Xcode 3.2-compatible project
  format from the project file.
- Record CocoaPods 0.35.0 and MDCSwipeToChoose 0.2.1 from `Podfile.lock`.
- Record vendored TwitterKit 1.2.0 and Fabric 1.1.1 from their framework
  metadata.
- Explain that the source uses a pre-modern Swift dialect and may require a
  historical toolchain migration before current Xcode can compile it.
- State that TwitterKit/Fabric and their service dependencies are retired and
  that credentials, login, API, and simulator behavior remain unverified.
- Keep the checked-in project, lockfile, and framework metadata as executable
  sources of truth.
- Add fail-closed documentation, metadata, suite, roadmap, changelog, and plan
  contracts plus hostile mutations.

## Verification

- focused static setup-note and metadata contracts
- repository and external-directory `make check`
- hostile deployment-target, CocoaPods, swipe dependency, framework-version,
  documentation, suite, roadmap, and plan-status mutations
- final artifact, credential, exact-diff, and hosted static-check audits

## Scope Boundary

This change does not install historical CocoaPods, rewrite Swift, modify the
Xcode project, add credentials, contact Twitter services, or claim successful
Xcode, simulator, login, or API execution.
