#!/usr/bin/env python3


def validation_errors(source):
    contracts = (
        'let allowedScreenNameCharacters = NSCharacterSet(charactersInString: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")',
        "let screenNameLength = (screen_name as NSString).length",
        "if screenNameLength == 0 || screenNameLength > 15",
        "screen_name.rangeOfCharacterFromSet(allowedScreenNameCharacters.invertedSet) != nil",
        "return",
        "let components = NSURLComponents()",
        'NSURLQueryItem(name: "screen_name", value: screen_name)',
        "if let url = components.URL",
        "UIApplication.sharedApplication().canOpenURL(url)",
        "UIApplication.sharedApplication().openURL(url)",
    )
    positions = [source.find(contract) for contract in contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["Twitter deep links must validate an ASCII handle before URL construction and opening"]
    return []
