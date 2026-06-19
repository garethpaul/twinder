#!/usr/bin/env python3


def function_body(source, start_marker, end_marker):
    start = source.find(start_marker)
    end = source.find(end_marker, start)
    if start < 0 or end < 0:
        return None
    return source[start:end]


def validation_errors(source):
    save_handler = function_body(
        source,
        "func saveTweep(tweep: Tweep) -> Bool",
        "func skipTweep(tweep: Tweep)",
    )
    swipe_handler = function_body(
        source,
        "func view(view: UIView!, wasChosenWithDirection direction: MDCSwipeDirection)",
        "func nextTweep() -> Tweep?",
    )
    if save_handler is None or swipe_handler is None:
        return ["saved-profile write and swipe handlers must remain present"]

    forbidden = ("self.managedObjectContext!", "tpv.tweep!")
    if any(fragment in save_handler + swipe_handler for fragment in forbidden):
        return ["saved-profile writes must not force-unwrap context or selected profile"]

    save_contracts = (
        "if let coordinator = self.managedObjectContext?.persistentStoreCoordinator",
        "let writeContext = NSManagedObjectContext()",
        "writeContext.persistentStoreCoordinator = coordinator",
        'let insertedObject = NSEntityDescription.insertNewObjectForEntityForName("FavTweets", inManagedObjectContext: writeContext)',
        "if let newTweet = insertedObject as? FavTweets",
        "newTweet.screen_name = tweep.screen_name",
        "newTweet.image_url = tweep.image",
        "newTweet.name = tweep.name",
        "var error: NSError? = nil",
        "if !writeContext.save(&error)",
        "writeContext.rollback()",
        "return false",
        "self.savedTweeps.append(tweep)",
        "return true",
    )
    positions = [save_handler.find(contract) for contract in save_contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["saved-profile writes must isolate, persist, roll back, then publish success"]

    if "inManagedObjectContext: context" in save_handler:
        return ["saved-profile writes must not mutate the shared view context"]

    first_rollback = save_handler.find("writeContext.rollback()")
    second_rollback = save_handler.find("writeContext.rollback()", first_rollback + 1)
    if second_rollback < save_handler.find("return true"):
        return ["saved-profile writes must roll back failed and unexpected insertions"]

    caller_contracts = (
        "if let selectedTweep = tpv.tweep",
        "if saveTweep(selectedTweep)",
        'println("Tweep saved!")',
    )
    positions = [swipe_handler.find(contract) for contract in caller_contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["like swipes must report success only after a successful saved-profile write"]

    return []
