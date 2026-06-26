#!/usr/bin/env python3
"""Mutation tests for account-bound profile image lifecycle ownership."""

from pathlib import Path

from person_profile_image_lifecycle_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Twinder" / "PersonController.swift"


def main():
    source = SOURCE.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError("baseline profile image lifecycle failed: " + "; ".join(errors))

    mutations = {
        "strong profile lookup capture": source.replace("TweepPicture(screenName){ [weak self]", "TweepPicture(screenName){", 1),
        "retain image transport capture": source.replace("pic.get(imageURL, {[weak self] image, error in", "pic.get(imageURL, {image, error in", 1),
        "remove generation invalidation": source.replace("        profileImageGeneration += 1\n", "", 1),
        "retain stale account image": source.replace("        peepImg.image = nil\n", "", 1),
        "remove disappearance cancellation": source.replace("        profileImageTask?.cancel()\n", "", 1),
        "remove appearance reload": source.replace("        loadProfileImage()\n", "", 1),
        "remove lookup main dispatch": source.replace("            dispatch_async(dispatch_get_main_queue()) {\n", "", 1).replace("            }\n        }\n\n    }\n\n    override func viewWillDisappear", "        }\n\n    }\n\n    override func viewWillDisappear", 1),
        "remove lookup generation guard": source.replace("                    if strongSelf.profileImageGeneration == requestGeneration {\n", "", 1).replace("                    }\n                }\n            }\n", "                }\n            }\n", 1),
        "remove image generation guard": source.replace("                                                if strongSelf.profileImageGeneration == requestGeneration {\n", "", 1),
        "remove lookup account guard": source.replace("                                if currentSession.userName == screenName {\n", "", 1),
        "remove image account guard": source.replace("                                                        if currentSession.userName == screenName {\n", "", 1),
        "remove deinit cancellation": source.replace("    deinit {\n        profileImageTask?.cancel()\n    }\n\n", "", 1),
    }

    for name, mutated_source in mutations.items():
        if mutated_source == source:
            raise AssertionError("mutation did not change source: " + name)
        if not validation_errors(mutated_source):
            raise AssertionError("mutation was not rejected: " + name)

    print("person profile image lifecycle mutations rejected ({0} cases)".format(len(mutations)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
