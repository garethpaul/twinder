#!/usr/bin/env python3


def validation_errors(source):
    did_move_start = source.find("override func didMoveToWindow()")
    did_move_end = source.find("init(frame:", did_move_start)
    request_start = source.find("let api = APIClient()")
    if min(did_move_start, did_move_end, request_start) < 0:
        return ["tweet embeds must define card lifecycle and request ownership"]

    did_move = source[did_move_start:did_move_end]
    if "if self.window == nil" not in did_move or "tweetRequestGeneration += 1" not in did_move:
        return ["detached tweet cards must invalidate pending embed callbacks"]

    request = source[request_start:]
    contracts = (
        "let requestGeneration = tweetRequestGeneration",
        "api.getTweet(screenName) { [weak self]",
        "strongSelf.tweetRequestGeneration == requestGeneration",
        "currentTweep.screen_name == screenName",
        "loadTweetWithID(tweet_result) { [weak self]",
        "dispatch_async(dispatch_get_main_queue())",
        "strongSelf.infoView.addSubview(tweetView)",
    )
    positions = [request.find(contract) for contract in contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["tweet embeds must reject detached or stale card callbacks on the main queue"]
    if "private var tweetRequestGeneration = 0" not in source:
        return ["tweet embeds must track a request generation"]
    return []
