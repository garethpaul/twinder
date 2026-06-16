#!/usr/bin/env python3
from pathlib import Path

from saved_profile_selection_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Twinder" / "TableController.swift").read_text(encoding="utf-8")
guard = (
    "        if indexPath.section != 0 || indexPath.item < 0 || "
    "indexPath.item >= self.fav_tweeps.count {\n"
    "            return\n"
    "        }\n\n"
)
model_access = "        let selectedTweep = self.fav_tweeps[indexPath.item]\n"

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline selection handler invalid: {errors}")

mutations = {
    "missing section guard": baseline.replace("indexPath.section != 0 || ", "", 1),
    "missing lower row bound": baseline.replace("indexPath.item < 0 || ", "", 1),
    "missing upper row bound": baseline.replace(
        " || indexPath.item >= self.fav_tweeps.count", "", 1
    ),
    "model access before guard": baseline.replace(
        guard + model_access, model_access + guard, 1
    ),
    "rediscovered selected row": baseline.replace(
        "        if indexPath.section",
        "        let indexPath = tableView.indexPathForSelectedRow()!\n        if indexPath.section",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Saved-profile selection contract passed ({len(mutations)} mutations rejected).")
