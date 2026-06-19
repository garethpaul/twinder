#!/usr/bin/env python3
from pathlib import Path

from project_path_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Twinder.xcodeproj" / "project.pbxproj").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline project path contract invalid: {errors}")

mutations = {
    "absolute developer path": baseline.replace(
        "Twinder/BridgeHeader.h", "/Users/example/work/Twinder/BridgeHeader.h", 1
    ),
    "missing debug bridge header": baseline.replace(
        "SWIFT_OBJC_BRIDGING_HEADER = Twinder/BridgeHeader.h;", "", 1
    ),
    "missing release bridge header": baseline.rsplit(
        "SWIFT_OBJC_BRIDGING_HEADER = Twinder/BridgeHeader.h;", 1
    )[0]
    + baseline.rsplit("SWIFT_OBJC_BRIDGING_HEADER = Twinder/BridgeHeader.h;", 1)[1],
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Project path contract passed ({len(mutations)} mutations rejected).")
