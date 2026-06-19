#!/usr/bin/env python3
from pathlib import Path

from saved_profile_model_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
model = (ROOT / "Twinder" / "FavTweets.swift").read_text(encoding="utf-8")
table = (ROOT / "Twinder" / "TableController.swift").read_text(encoding="utf-8")

errors = validation_errors(model, table)
if errors:
    raise AssertionError(f"baseline saved-profile model invalid: {errors}")

mutations = {
    "nonoptional screen name": (model.replace("screen_name: String?", "screen_name: String", 1), table),
    "nonoptional image URL": (model.replace("image_url: String?", "image_url: String", 1), table),
    "nonoptional display name": (model.replace("name: String?", "name: String", 1), table),
    "unbound selected handle": (
        model,
        table.replace(
            "        if let screenName = selectedTweep.screen_name {\n            twtrScreenName(screenName)\n        }",
            "        twtrScreenName(selectedTweep.screen_name!)",
            1,
        ),
    ),
    "unbound image URL": (
        model,
        table.replace(
            "            if let imageURLString = fav_tweep.image_url {\n                if let imageURL = NSURL(string: imageURLString) {",
            "            if let imageURL = NSURL(string: fav_tweep.image_url!) {",
            1,
        ),
    ),
}

for description, (model_source, table_source) in mutations.items():
    if not validation_errors(model_source, table_source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Saved-profile model contract passed ({len(mutations)} mutations rejected).")
