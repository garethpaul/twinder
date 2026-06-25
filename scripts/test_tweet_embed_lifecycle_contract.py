#!/usr/bin/env python3
from pathlib import Path

from tweet_embed_lifecycle_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "Twinder" / "TweepPickerView.swift").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline tweet embed lifecycle invalid: {errors}")

mutations = {
    "strong outer capture": baseline.replace("api.getTweet(screenName) { [weak self]", "api.getTweet(screenName) {", 1),
    "strong inner capture": baseline.replace("loadTweetWithID(tweet_result) { [weak self]", "loadTweetWithID(tweet_result) {", 1),
    "missing detach invalidation": baseline.replace("        tweetRequestGeneration += 1\n", "", 1),
    "missing request identity": baseline.replace("strongSelf.tweetRequestGeneration == requestGeneration", "true", 1),
    "missing profile identity": baseline.replace("currentTweep.screen_name == screenName", "true", 1),
    "background UI mutation": baseline.replace("dispatch_async(dispatch_get_main_queue())", "dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0))", 1),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Tweet embed lifecycle passed ({len(mutations)} mutations rejected).")
