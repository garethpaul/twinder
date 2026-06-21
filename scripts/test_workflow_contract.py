#!/usr/bin/env python3
from pathlib import Path

from workflow_contract import CHECKOUT_ACTION, SETUP_ACTION, validate


ROOT = Path(__file__).resolve().parents[1]
BASELINE = (ROOT / ".github" / "workflows" / "check.yml").read_text(encoding="utf-8")


def mutate(description, target, replacement):
    mutated = BASELINE.replace(target, replacement, 1)
    if mutated == BASELINE:
        raise AssertionError(f"{description} mutation did not alter the workflow")
    return mutated


baseline_errors = validate(BASELINE)
if baseline_errors:
    raise AssertionError(f"baseline workflow is invalid: {baseline_errors}")

mutations = {
    "contradictory credentials": mutate("contradictory credentials", "persist-credentials: false", "persist-credentials: false\n          persist-credentials: true"),
    "checkout ref override": mutate("checkout ref override", "persist-credentials: false", "persist-credentials: false\n          ref: master"),
    "relocated credentials": mutate("relocated credentials", "        with:\n          persist-credentials: false\n", "").replace("permissions:", "persist-credentials: false\n\npermissions:", 1),
    "floating checkout": mutate("floating checkout", CHECKOUT_ACTION, "actions/checkout@v6"),
    "floating setup": mutate("floating setup", SETUP_ACTION, "actions/setup-python@v6"),
    "extra action": mutate("extra action", "      - name: Set up Python", "      - uses: example/unreviewed-action@v1\n      - name: Set up Python"),
    "write permission": mutate("write permission", "contents: read", "contents: read\n  issues: write"),
    "quoted write permission": mutate("quoted write permission", "contents: read", 'contents: read\n  "issues": write'),
    "job write permission": mutate(
        "job write permission",
        "  check:\n    runs-on:",
        "  check:\n    permissions:\n      issues: write\n    runs-on:",
    ),
    "missing pull request": mutate("missing pull request", "  pull_request:\n", ""),
    "missing push": mutate("missing push", "  push:\n    branches:\n      - master\n", ""),
    "missing manual dispatch": mutate("missing manual dispatch", "  workflow_dispatch:\n", ""),
    "duplicate runner": mutate("duplicate runner", "    runs-on: ubuntu-24.04", "    runs-on: ubuntu-24.04\n    runs-on: ubuntu-24.04"),
    "unbounded job": mutate("unbounded job", "    timeout-minutes: 10\n", ""),
    "fail-fast matrix": mutate("fail-fast matrix", "      fail-fast: false", "      fail-fast: true"),
    "reduced matrix": mutate("reduced matrix", '["3.10", "3.12", "3.14"]', '["3.12"]'),
    "continued failure": mutate("continued failure", "    strategy:", "    continue-on-error: true\n    strategy:"),
    "custom default shell": mutate(
        "custom default shell",
        "  check:\n    runs-on:",
        "  check:\n    defaults:\n      run:\n        shell: /usr/bin/true {0}\n    runs-on:",
    ),
    "skipped check job": mutate(
        "skipped check job",
        "  check:\n    runs-on:",
        "  check:\n    if: ${{ github.event_name == 'workflow_run' }}\n    runs-on:",
    ),
    "containerized check job": mutate(
        "containerized check job",
        "  check:\n    runs-on:",
        "  check:\n    container: example/unreviewed:latest\n    runs-on:",
    ),
    "service container": mutate(
        "service container",
        "  check:\n    runs-on:",
        "  check:\n    services:\n      hostile:\n        image: example/unreviewed:latest\n    runs-on:",
    ),
    "hostile job environment": mutate(
        "hostile job environment",
        "  check:\n    runs-on:",
        "  check:\n    env:\n      PATH: .:/usr/bin:/bin\n    runs-on:",
    ),
    "redirected working directory": mutate(
        "redirected working directory",
        '        run: /usr/bin/make check PYTHON="$(command -v python)"',
        '        working-directory: /tmp\n        run: /usr/bin/make check PYTHON="$(command -v python)"',
    ),
    "custom step shell": mutate(
        "custom step shell",
        '        run: /usr/bin/make check PYTHON="$(command -v python)"',
        '        shell: /usr/bin/true {0}\n        run: /usr/bin/make check PYTHON="$(command -v python)"',
    ),
    "unnamed executable step": mutate(
        "unnamed executable step",
        "      - name: Run static contracts",
        "      - run: ./ci-bypass.sh\n      - name: Run static contracts",
    ),
    "flow-style executable step": mutate(
        "flow-style executable step",
        "      - name: Run static contracts",
        "      - { run: ./ci-bypass.sh }\n      - name: Run static contracts",
    ),
    "extra job": mutate(
        "extra job",
        "  check:\n    runs-on:",
        "  hostile:\n    runs-on: ubuntu-24.04\n    steps:\n      - run: ./ci-bypass.sh\n  check:\n    runs-on:",
    ),
    "wrong Python selector": mutate("wrong Python selector", "python-version: ${{ matrix.python-version }}", 'python-version: "3.12"'),
    "hosted Xcode": mutate("hosted Xcode", "run: /usr/bin/make check", "run: xcodebuild build && /usr/bin/make check"),
    "weakened gate": mutate("weakened gate", "run: /usr/bin/make check", "run: /usr/bin/make lint"),
}

accepted_mutations = [description for description, workflow in mutations.items() if not validate(workflow)]
if accepted_mutations:
    raise AssertionError(f"mutations were accepted: {', '.join(accepted_mutations)}")

print(f"workflow contract tests passed ({len(mutations)} mutations rejected).")
