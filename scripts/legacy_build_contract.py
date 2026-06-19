#!/usr/bin/env python3


def validation_errors(source):
    contracts = (
        "if command -v xcodebuild",
        "xcode_major=$$(xcodebuild -version",
        'if [ "$$xcode_major" -le 6 ]',
        'cd "$(ROOT)" && xcodebuild',
        "requires Xcode 6.x for its pre-versioned Swift sources",
        "xcodebuild is not available on this host",
    )
    positions = [source.find(contract) for contract in contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["legacy builds must run only on Xcode 6 and explain every skip path"]
    return []
