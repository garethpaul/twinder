#!/usr/bin/env python3
from pathlib import Path

from legacy_build_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Makefile").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline legacy build contract invalid: {errors}")

mutations = {
    "missing Xcode availability guard": baseline.replace("if [ -x '/usr/bin/xcodebuild' ]", "if true", 1),
    "missing Xcode major detection": baseline.replace("xcode_major=$$$$('/usr/bin/xcodebuild' -version", "xcode_major=$$$$(echo", 1),
    "accepts modern Xcode": baseline.replace('if [ "$$$$xcode_major" -le 6 ]', 'if [ "$$$$xcode_major" -ge 6 ]', 1),
    "build before version guard": baseline.replace(
        '\t\tif [ "$$$$xcode_major" -le 6 ]; then \\\n\t\t\tcd \'$(REPOSITORY_ROOT_LITERAL)\' && \'/usr/bin/xcodebuild\'',
        '\t\tcd \'$(REPOSITORY_ROOT_LITERAL)\' && \'/usr/bin/xcodebuild\'; \\\n\t\tif [ "$$$$xcode_major" -le 6 ]; then \\\n\t\t\ttrue',
        1,
    ),
    "silent compatibility skip": baseline.replace(
        'echo "iOS build skipped: this project requires Xcode 6.x for its pre-versioned Swift sources."',
        "true",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Legacy build contract passed ({len(mutations)} mutations rejected).")
