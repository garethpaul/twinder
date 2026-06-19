#!/usr/bin/env python3


def validation_errors(source):
    contracts = (
        "cell.viewWithTag(savedProfileHeaderTag)?.removeFromSuperview()",
        "cell.viewWithTag(savedProfileBorderTag)?.removeFromSuperview()",
        "let headerView: UIView = UIView",
        "headerView.tag = savedProfileHeaderTag",
        "cell.addSubview(headerView)",
        "let headerBackgroundLabel: UILabel = UILabel",
        "headerBackgroundLabel.tag = savedProfileBorderTag",
        "cell.addSubview(headerBackgroundLabel)",
    )
    positions = [source.find(contract) for contract in contracts]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return ["saved-profile cells must remove owned overlays before recreating them"]
    return []
