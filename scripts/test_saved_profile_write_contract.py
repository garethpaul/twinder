#!/usr/bin/env python3
from pathlib import Path

from saved_profile_write_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Twinder" / "TweepPickerViewController.swift").read_text(
    encoding="utf-8"
)

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline saved-profile write invalid: {errors}")

mutations = {
    "missing context guard": baseline.replace(
        "if let context = self.managedObjectContext",
        "if self.managedObjectContext != nil",
        1,
    ),
    "force-unwrapped insertion context": baseline.replace(
        "inManagedObjectContext: context",
        "inManagedObjectContext: self.managedObjectContext!",
        1,
    ),
    "missing field population": baseline.replace(
        "            newTweet.screen_name = tweep.screen_name\n",
        "",
        1,
    ),
    "force-cast inserted entity": baseline.replace(
        "if let newTweet = insertedObject as? FavTweets",
        "let newTweet = insertedObject as FavTweets",
        1,
    ),
    "missing persistence attempt": baseline.replace(
        "if !context.save(&error)",
        "if error != nil",
        1,
    ),
    "missing failed-insert cleanup": baseline.replace(
        "                context.deleteObject(newTweet)\n",
        "",
        1,
    ),
    "missing failure result": baseline.replace(
        "                return false\n",
        "                return true\n",
        1,
    ),
    "append before save": baseline.replace(
        "            self.savedTweeps.append(tweep)\n", "", 1
    ).replace(
        "            if !context.save(&error) {\n",
        "            self.savedTweeps.append(tweep)\n            if !context.save(&error) {\n",
        1,
    ),
    "force-unwrapped selected profile": baseline.replace(
        "if let selectedTweep = tpv.tweep",
        "if tpv.tweep != nil",
        1,
    ).replace("saveTweep(selectedTweep)", "saveTweep(tpv.tweep!)", 1),
    "unconditional success diagnostic": baseline.replace(
        "                if saveTweep(selectedTweep) {\n                    println(\"Tweep saved!\")\n                }",
        "                saveTweep(selectedTweep)\n                println(\"Tweep saved!\")",
        1,
    ),
    "missing success result": baseline.replace(
        "            return true\n",
        "            return false\n",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Saved-profile write contract passed ({len(mutations)} mutations rejected).")
