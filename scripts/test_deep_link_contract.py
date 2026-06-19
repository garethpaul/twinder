#!/usr/bin/env python3
from pathlib import Path

from deep_link_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Twinder" / "DeepLinks.swift").read_text(encoding="utf-8")
validation_block = """    let allowedScreenNameCharacters = NSCharacterSet(charactersInString: \"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_\")
    let screenNameLength = (screen_name as NSString).length
    if screenNameLength == 0 || screenNameLength > 15 ||
        screen_name.rangeOfCharacterFromSet(allowedScreenNameCharacters.invertedSet) != nil {
        return
    }

"""
components_line = "    let components = NSURLComponents()\n"

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline deep-link handler invalid: {errors}")

mutations = {
    "missing empty handle rejection": baseline.replace("screenNameLength == 0 || ", "", 1),
    "missing maximum handle length": baseline.replace(" || screenNameLength > 15", "", 1),
    "Unicode handle alphabet": baseline.replace(
        'NSCharacterSet(charactersInString: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")',
        "NSCharacterSet.alphanumericCharacterSet()",
        1,
    ),
    "missing invalid-character rejection": baseline.replace(
        " ||\n        screen_name.rangeOfCharacterFromSet(allowedScreenNameCharacters.invertedSet) != nil",
        "",
        1,
    ),
    "validation after construction": baseline.replace(
        validation_block + components_line,
        components_line + validation_block,
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Deep-link contract passed ({len(mutations)} mutations rejected).")
