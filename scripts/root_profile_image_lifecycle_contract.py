#!/usr/bin/env python3
"""Static contract for the root profile image lifecycle."""


def ordered(source, fragments):
    positions = [source.find(fragment) for fragment in fragments]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def validation_errors(source):
    errors = []
    for fragment in (
        "var profileImageTask: NSURLSessionDataTask?",
        "var profileImageGeneration = 0",
        "pic.get(imageURL, {[weak self] image, error in",
        "if let currentTweep = strongSelf.tweep",
        "currentTweep.image == imageURLString",
    ):
        if fragment not in source:
            errors.append("root profile image work must remain weak, cancellable, and identity-bound")
            break

    appearance = source[source.find("override func viewWillAppear"):source.find("override func viewWillDisappear")]
    if not ordered(appearance, ("super.viewWillAppear(animated)", "loadProfileImage()")):
        errors.append("root profile image work must reload on appearance")

    disappearance = source[source.find("override func viewWillDisappear"):source.find("func loadProfileImage")]
    if not ordered(disappearance, (
        "profileImageGeneration += 1",
        "profileImageTask?.cancel()",
        "profileImageTask = nil",
        "super.viewWillDisappear(animated)",
    )):
        errors.append("leaving the root profile must invalidate and cancel image work")

    load = source[source.find("func loadProfileImage"):source.find("deinit")]
    if not ordered(load, (
        "profileImageTask?.cancel()",
        "profileImageTask = nil",
        "profileImageGeneration += 1",
        "imageView.image = nil",
        "let requestGeneration = profileImageGeneration",
        "if let selectedTweep = self.tweep",
        "let imageURLString = selectedTweep.image",
        "if let imageURL = NSURL(string: imageURLString)",
        "profileImageTask = pic.get(imageURL, {[weak self] image, error in",
        "if let strongSelf = self",
        "strongSelf.profileImageGeneration == requestGeneration",
        "if let currentTweep = strongSelf.tweep",
        "currentTweep.image == imageURLString",
        "strongSelf.imageView.image = newImg",
    )):
        errors.append("root profile image callbacks must validate generation and selected identity")

    if "deinit {\n        profileImageTask?.cancel()\n    }" not in source:
        errors.append("root profile image transport must cancel on controller release")
    return errors
