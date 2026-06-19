#!/usr/bin/env python3
from pathlib import Path

from saved_profile_cell_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Twinder" / "TableController.swift").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline saved-profile cell lifecycle invalid: {errors}")

mutations = {
    "missing header cleanup": baseline.replace(
        "            cell.viewWithTag(savedProfileHeaderTag)?.removeFromSuperview()\n",
        "",
        1,
    ),
    "missing border cleanup": baseline.replace(
        "            cell.viewWithTag(savedProfileBorderTag)?.removeFromSuperview()\n",
        "",
        1,
    ),
    "untagged header": baseline.replace(
        "            headerView.tag = savedProfileHeaderTag\n", "", 1
    ),
    "untagged border": baseline.replace(
        "            headerBackgroundLabel.tag = savedProfileBorderTag\n", "", 1
    ),
    "cleanup after header creation": baseline.replace(
        "            cell.viewWithTag(savedProfileHeaderTag)?.removeFromSuperview()\n",
        "",
        1,
    ).replace(
        "            let headerView: UIView = UIView",
        "            cell.viewWithTag(savedProfileHeaderTag)?.removeFromSuperview()\n            let headerView: UIView = UIView",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Saved-profile cell lifecycle passed ({len(mutations)} mutations rejected).")
