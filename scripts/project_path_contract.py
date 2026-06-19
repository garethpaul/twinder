#!/usr/bin/env python3


def validation_errors(source):
    if "/Users/" in source:
        return ["Xcode build settings must not contain developer-home paths"]
    if source.count("SWIFT_OBJC_BRIDGING_HEADER = Twinder/BridgeHeader.h;") != 2:
        return ["all target configurations must use the repository-relative bridge header"]
    return []
