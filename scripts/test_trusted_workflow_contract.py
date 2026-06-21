#!/usr/bin/env python3
from pathlib import Path

from trusted_workflow_contract import validate_candidate


ROOT = Path(__file__).resolve().parents[1]
CHECK = (ROOT / ".github" / "workflows" / "check.yml").read_bytes()
GATE = (ROOT / ".github" / "workflows" / "trusted-workflow-contract.yml").read_bytes()
POLICY = (ROOT / "scripts" / "trusted_workflow_contract.py").read_bytes()
GATE_TEXT = GATE.decode("utf-8")
MAKEFILE = (ROOT / "Makefile").read_text(encoding="utf-8")

required_gate_fragments = (
    "pull_request_target:",
    "ref: ${{ github.event.pull_request.base.sha }}",
    "persist-credentials: false",
    "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
    "actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd",
    "/usr/bin/python3 -I -B scripts/trusted_workflow_contract.py",
)
for fragment in required_gate_fragments:
    if fragment not in GATE_TEXT:
        raise AssertionError(f"trusted gate is missing required fragment: {fragment}")

if "ref: ${{ github.event.pull_request.head.sha }}" in GATE_TEXT:
    raise AssertionError("trusted gate must never check out candidate code")

if "scripts/test_trusted_workflow_contract.py" not in MAKEFILE:
    raise AssertionError("Makefile must run the trusted workflow contract tests")


def rejected(description, *, check=CHECK, gate=GATE, policy=POLICY):
    errors = validate_candidate(
        candidate_check=check,
        candidate_gate=gate,
        candidate_policy=policy,
        base_gate=GATE,
        base_policy=POLICY,
    )
    if not errors:
        raise AssertionError(f"{description} was accepted")


baseline_errors = validate_candidate(
    candidate_check=CHECK,
    candidate_gate=GATE,
    candidate_policy=POLICY,
    base_gate=GATE,
    base_policy=POLICY,
)
if baseline_errors:
    raise AssertionError(f"baseline trusted workflow contract is invalid: {baseline_errors}")

rejected("no-op command", check=CHECK.replace(b"/usr/bin/make check", b"/usr/bin/true      ", 1))
rejected(
    "folded command",
    check=CHECK.replace(
        b'run: /usr/bin/make check PYTHON="$(command -v python)"',
        b'run: >\n          /usr/bin/make check PYTHON="$(command -v python)"',
        1,
    ),
)
rejected("candidate gate edit", gate=GATE + b"\n# candidate edit\n")
rejected("candidate policy edit", policy=POLICY + b"\n# candidate edit\n")
rejected("CRLF rewrite", check=CHECK.replace(b"\n", b"\r\n"))
rejected("workflow comment", check=CHECK + b"\n# candidate comment\n")

print("trusted workflow contract tests passed (6 trust-boundary mutations rejected).")
