#!/usr/bin/env python3
"""Mutation tests for the root profile image lifecycle."""

from pathlib import Path
from root_profile_image_lifecycle_contract import validation_errors

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Twinder" / "ViewController.swift"


def main():
    source = SOURCE.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError("baseline root profile image lifecycle failed: " + "; ".join(errors))

    mutations = {
        "strong callback capture": source.replace("pic.get(imageURL, {[weak self] image, error in", "pic.get(imageURL, {image, error in", 1),
        "remove disappearance cancellation": source.replace("        profileImageTask?.cancel()\n", "", 1),
        "remove generation invalidation": source.replace("        profileImageGeneration += 1\n", "", 1),
        "retain stale image": source.replace("        imageView.image = nil\n", "", 1),
        "remove generation check": source.replace("strongSelf.profileImageGeneration == requestGeneration", "true", 1),
        "remove identity check": source.replace("currentTweep.image == imageURLString", "true", 1),
        "remove appearance reload": source.replace("        loadProfileImage()\n", "", 1),
        "remove deinit cancellation": source.replace("\n    deinit {\n        profileImageTask?.cancel()\n    }", "", 1),
    }
    for name, mutated in mutations.items():
        if mutated == source:
            raise AssertionError("mutation did not apply: " + name)
        if not validation_errors(mutated):
            raise AssertionError("mutation survived: " + name)
    print("root profile image lifecycle mutations rejected (%d cases)" % len(mutations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
