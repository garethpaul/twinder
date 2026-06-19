#!/usr/bin/env python3


def validation_errors(model_source, table_source):
    model_contracts = (
        "@NSManaged var screen_name: String?",
        "@NSManaged var image_url: String?",
        "@NSManaged var name: String?",
    )
    if any(contract not in model_source for contract in model_contracts):
        return ["FavTweets properties must match the optional Core Data schema"]

    table_contracts = (
        "if let screenName = selectedTweep.screen_name",
        "twtrScreenName(screenName)",
        "if let imageURLString = fav_tweep.image_url",
        "if let imageURL = NSURL(string: imageURLString)",
    )
    positions = [table_source.find(contract) for contract in table_contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["saved-profile consumers must bind optional persisted fields before use"]
    return []
