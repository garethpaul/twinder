#!/usr/bin/env python3


def selection_handler(source):
    start = source.find(
        "func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath)"
    )
    end = source.find(
        "func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath)",
        start,
    )
    if start < 0 or end < 0:
        return None
    return source[start:end]


def validation_errors(source):
    handler = selection_handler(source)
    if handler is None:
        return ["saved-profile table selection handler must remain present"]

    guard = (
        "if indexPath.section != 0 || indexPath.item < 0 || "
        "indexPath.item >= self.fav_tweeps.count"
    )
    model_access = "let selectedTweep = self.fav_tweeps[indexPath.item]"
    handle_binding = "if let screenName = selectedTweep.screen_name"
    deep_link = "twtrScreenName(screenName)"

    forbidden = (
        "indexPathForSelectedRow",
        "cellForRowAtIndexPath(indexPath!)",
        "indexPath!",
        "as TweepCell",
        "selectedTweep.screen_name!",
    )
    if any(fragment in handler for fragment in forbidden):
        return ["saved-profile selection must not rediscover or force-unwrap table identity"]

    positions = [
        handler.find(fragment)
        for fragment in (guard, model_access, handle_binding, deep_link)
    ]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["saved-profile selection must validate section and row before model access"]

    return []
