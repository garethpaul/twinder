#!/usr/bin/env python3
import hashlib
import sys
from pathlib import Path


EXPECTED_CHECK_SHA256 = "18d8a126367a639da34207176359f2329816fb126ad88972e9e3212233ccae5b"


def validate_candidate(
    *,
    candidate_check,
    candidate_gate,
    candidate_policy,
    base_gate,
    base_policy,
):
    errors = []
    if hashlib.sha256(candidate_check).hexdigest() != EXPECTED_CHECK_SHA256:
        errors.append("candidate check workflow must match the reviewed byte-for-byte contract")
    if candidate_gate != base_gate:
        errors.append("candidate must not modify the base-owned trusted workflow gate")
    if candidate_policy != base_policy:
        errors.append("candidate must not modify the base-owned trusted workflow policy")
    return errors


def main(argv):
    if len(argv) != 4:
        raise SystemExit(
            "usage: trusted_workflow_contract.py "
            "CANDIDATE_CHECK CANDIDATE_GATE CANDIDATE_POLICY"
        )

    root = Path(__file__).resolve().parents[1]
    errors = validate_candidate(
        candidate_check=Path(argv[1]).read_bytes(),
        candidate_gate=Path(argv[2]).read_bytes(),
        candidate_policy=Path(argv[3]).read_bytes(),
        base_gate=(root / ".github/workflows/trusted-workflow-contract.yml").read_bytes(),
        base_policy=Path(__file__).read_bytes(),
    )
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("base-owned trusted workflow contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
