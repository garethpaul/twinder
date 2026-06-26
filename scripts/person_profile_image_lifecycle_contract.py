#!/usr/bin/env python3
"""Static contract for account-bound profile image lifecycle ownership."""


def ordered(source, fragments):
    positions = [source.find(fragment) for fragment in fragments]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def validation_errors(source):
    errors = []

    for fragment in (
        "var profileImageTask: NSURLSessionDataTask?",
        "var profileImageGeneration = 0",
        "TweepPicture(screenName){ [weak self]",
        "strongSelf.profileImageTask = pic.get(imageURL, {[weak self] image, error in",
        "if currentSession.userName == screenName",
    ):
        if fragment not in source:
            errors.append("profile image work must remain weak, cancellable, and account-bound")
            break

    disappearance = source[source.find("override func viewWillDisappear"):source.find("override func didReceiveMemoryWarning")]
    if not ordered(
        disappearance,
        (
            "profileImageGeneration += 1",
            "profileImageTask?.cancel()",
            "profileImageTask = nil",
            "super.viewWillDisappear(animated)",
        ),
    ):
        errors.append("leaving the profile must invalidate and cancel image work")

    appearance = source[source.find("override func viewWillAppear"):source.find("func loadProfileImage")]
    if not ordered(
        appearance,
        (
            "super.viewWillAppear(animated)",
            "loadProfileImage()",
        ),
    ):
        errors.append("returning to the profile must start a fresh image lookup")

    setup = source[source.find("if let session = Twitter.sharedInstance().session()"):source.find("TweepPicture(screenName)")]
    if not ordered(
        setup,
        (
            "let screenName = session.userName",
            "profileImageTask?.cancel()",
            "profileImageTask = nil",
            "profileImageGeneration += 1",
            "let requestGeneration = profileImageGeneration",
        ),
    ):
        errors.append("each profile image lookup must own a fresh request generation")

    lookup = source[source.find("TweepPicture(screenName)"):source.find("override func viewWillDisappear")]
    before_transport, separator, after_transport = lookup.partition(
        "strongSelf.profileImageTask = pic.get(imageURL, {[weak self] image, error in"
    )
    if not separator or not ordered(
        before_transport,
        (
            "TweepPicture(screenName){ [weak self]",
            "dispatch_async(dispatch_get_main_queue())",
            "if let strongSelf = self",
            "                        if strongSelf.profileImageGeneration == requestGeneration",
            "if let currentSession = Twitter.sharedInstance().session()",
            "if currentSession.userName == screenName",
        ),
    ) or not ordered(
        after_transport,
        (
            "                                                if strongSelf.profileImageGeneration == requestGeneration",
            "if let currentSession = Twitter.sharedInstance().session()",
            "if currentSession.userName == screenName",
            "strongSelf.peepImg.image = circle",
        ),
    ):
        errors.append("profile image callbacks must validate generation and account before UI")

    if "deinit {\n        profileImageTask?.cancel()\n    }" not in source:
        errors.append("profile image transport must be cancelled when its controller is released")

    return errors
