# AGENTS.md

## Repository purpose

`garethpaul/twinder` is an Apple platform application or Objective-C/Swift sample. A simple application that showcases Fabric + Cocoapods

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `Podfile` - CocoaPods dependency definition
- `Twinder.xcodeproj` - Xcode project
- `Twinder.xcworkspace` - Xcode workspace
- `Fabric.framework` - repository source or sample assets
- `plans` - repository source or sample assets
- `Twinder` - repository source or sample assets
- `TwinderTests` - repository source or sample assets
- `TwitterKit.framework` - repository source or sample assets

## Development commands

- Install dependencies: `pod install`
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Workflow contract mutations: `make contract-test`
- Tests: `make test`
- Build: `make build`
- Local Apple development: `open Twinder.xcworkspace`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C/C++ headers (24), Swift (23), Objective-C (1).
- Use the CocoaPods workspace when present; update `Podfile.lock` only with an intentional dependency change.
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `TwinderTests/TwinderTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.
- Keep hosted verification read-only and credential-free with immutable action
  pins; update the structural workflow mutations with any intentional policy
  change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-twinder-baseline.md` for the current static verification baseline.
- Reused saved-profile cells cancel obsolete image tasks and reject stale completions.
- Saved-profile selection validates table identity before opening Twitter.
- See `docs/plans/2026-06-08-profile-image-loading-guards.md` for profile-card image URL and decode guard coverage.
- `Pods/` is vendored dependency code; do not hand-edit it unless intentionally updating dependencies.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
