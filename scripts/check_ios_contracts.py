#!/usr/bin/env python3
"""Static verification for the legacy Twinder iOS project."""

from pathlib import Path
import json
import plistlib
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-twinder-baseline.md"


def fail(message):
    print(f"check_ios_contracts.py: {message}", file=sys.stderr)
    return 1


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_plist(relative_path):
    with (ROOT / relative_path).open("rb") as plist_file:
        return plistlib.load(plist_file)


def check_project_files_parse():
    app_info = load_plist("Twinder/Info.plist")
    test_info = load_plist("TwinderTests/Info.plist")
    require(app_info["UIMainStoryboardFile"] == "Main", "app must launch Main.storyboard")
    require(test_info["CFBundlePackageType"] == "BNDL", "test target must remain a bundle")

    for relative_path in [
        "Twinder/Base.lproj/Main.storyboard",
        "Twinder/Base.lproj/LaunchScreen.xib",
    ]:
        ET.parse(ROOT / relative_path)

    for path in (ROOT / "Twinder/Images.xcassets").rglob("Contents.json"):
        json.loads(path.read_text(encoding="utf-8"))


def check_pod_lock_integrity():
    podfile_lock = (ROOT / "Podfile.lock").read_bytes()
    manifest_lock = (ROOT / "Pods/Manifest.lock").read_bytes()
    require(podfile_lock == manifest_lock, "Podfile.lock and Pods/Manifest.lock must stay in sync")

    project = read_text("Twinder.xcodeproj/project.pbxproj")
    require("TwinderTests.swift in Sources" in project, "test source must remain in the Xcode project")
    require("Pods-Twinder.debug.xcconfig" in project, "CocoaPods debug xcconfig must remain referenced")


def check_tweep_picture_json_guard():
    source = read_text("Twinder/TweepPicture.swift")
    require("json!" not in source, "TweepPicture must not force-unwrap parsed JSON")
    require("profile_image_url!" not in source, "TweepPicture must not force-unwrap profile image URLs")
    require("if let jsonObject = json as? JSONDictionary" in source, "TweepPicture must validate JSON dictionary shape")
    require("if let profileImageURL" in source, "TweepPicture must validate profile image URL presence")


def check_api_json_guards():
    source = read_text("Twinder/API.swift")
    require("json!" not in source, "API.swift must not force-unwrap parsed JSON")
    require("tweets.count > 0" in source, "timeline parsing must check for at least one tweet")
    require("if let jsonObject = json as? JSONDictionary" in source, "friends-list parsing must validate JSON dictionary shape")
    require("if let tweepData = tweep as? JSONDictionary" in source, "friends-list parsing must validate each user record")
    require(
        'if let image = tweepData["profile_image_url"] as? String',
        "friends-list parsing must validate profile image URL presence",
    )


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def main():
    checks = [
        check_project_files_parse,
        check_pod_lock_integrity,
        check_tweep_picture_json_guard,
        check_api_json_guards,
        check_docs_plans,
    ]
    try:
        for check in checks:
            check()
    except (AssertionError, ET.ParseError, json.JSONDecodeError, plistlib.InvalidFileException) as exc:
        return fail(str(exc))

    print(f"Twinder static contracts passed ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
