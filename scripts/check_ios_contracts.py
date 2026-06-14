#!/usr/bin/env python3
"""Static verification for the legacy Twinder iOS project."""

from pathlib import Path
import json
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

from workflow_contract import validate as validate_workflow


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-twinder-baseline.md"
TWEEP_PICTURE_FAILURE_PLAN = DOCS_PLANS / "2026-06-09-tweep-picture-failure-completion.md"
INITIAL_CARD_PLAN = DOCS_PLANS / "2026-06-09-initial-card-data-guards.md"
TIMELINE_TWEET_FAILURE_PLAN = DOCS_PLANS / "2026-06-09-timeline-tweet-failure-completion.md"
TIMELINE_TWEET_PLAN = DOCS_PLANS / "2026-06-09-timeline-tweet-completion.md"
FRIENDS_LIST_DATA_PLAN = DOCS_PLANS / "2026-06-09-friends-list-data-guard.md"
CI_PLAN = DOCS_PLANS / "2026-06-10-ci-baseline.md"
PROFILE_IMAGE_TRANSPORT_PLAN = DOCS_PLANS / "2026-06-10-profile-image-transport.md"
TABLE_IMAGE_REUSE_PLAN = DOCS_PLANS / "2026-06-10-table-image-reuse.md"
SAVED_PROFILE_CONTEXT_PLAN = DOCS_PLANS / "2026-06-12-saved-profile-context-guard.md"
SWIPE_CARD_IMAGE_IDENTITY_PLAN = DOCS_PLANS / "2026-06-13-swipe-card-image-identity.md"
SWIPE_CARD_IMAGE_CANCELLATION_PLAN = DOCS_PLANS / "2026-06-13-swipe-card-image-cancellation.md"
SAFE_TWITTER_DEEP_LINK_PLAN = DOCS_PLANS / "2026-06-13-safe-twitter-deep-link.md"
MAKE_ROOT_PROTECTION_PLAN = DOCS_PLANS / "2026-06-14-make-root-override-protection.md"
CI_WORKFLOW = ROOT / ".github/workflows/check.yml"


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
    gitignore = read_text(".gitignore")
    require("__pycache__/" in gitignore, "Python bytecode cache directories must be ignored")
    require("*.py[cod]" in gitignore, "Python bytecode files must be ignored")

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


def check_tweep_picture_failure_completion():
    source = read_text("Twinder/TweepPicture.swift")
    person_controller = read_text("Twinder/PersonController.swift")

    require(
        "connectionError == nil && data != nil" in source,
        "TweepPicture must verify response data exists before JSON parsing",
    )
    require(
        source.count('completion(result: "")') >= 4,
        "TweepPicture must complete missing-data, malformed-JSON, transport, and request failures",
    )
    require(
        "println(" not in source and "NSLog(" not in source,
        "TweepPicture must not log Twitter API errors or profile lookup details",
    )
    require(
        "if result.isEmpty" in person_controller,
        "PersonController must ignore empty TweepPicture failure completions",
    )


def check_api_json_guards():
    source = read_text("Twinder/API.swift")
    swipe_card = read_text("Twinder/TweepPickerView.swift")
    require("json!" not in source, "API.swift must not force-unwrap parsed JSON")
    require(
        "Twitter.sharedInstance().session().userName" not in source,
        "friends-list parsing must not force-use the Twitter session username",
    )
    require(
        "if let currentSession = Twitter.sharedInstance().session()" in source,
        "friends-list parsing must guard the current Twitter session before request setup",
    )
    require("tweets.count > 0" in source, "timeline parsing must check for at least one tweet")
    require("if let jsonObject = json as? JSONDictionary" in source, "friends-list parsing must validate JSON dictionary shape")
    require("if let tweepData = tweep as? JSONDictionary" in source, "friends-list parsing must validate each user record")
    require(
        'if let image = tweepData["profile_image_url"] as? String',
        "friends-list parsing must validate profile image URL presence",
    )
    require(
        "connectionError == nil && data != nil" in source,
        "timeline tweet lookup must verify response data exists before JSON parsing",
    )
    require(
        source.count("connectionError == nil && data != nil") >= 2,
        "friends-list and timeline tweet lookups must verify response data exists before JSON parsing",
    )
    require(
        "println(screen_name)" not in source,
        "friends-list lookup must not log Twitter usernames",
    )
    require(
        'var tweetResult = ""' in source,
        "timeline tweet lookup must keep an empty fallback result",
    )
    require(
        "completion(result: tweetResult)" in source,
        "timeline tweet lookup must complete after parsing succeeds or finds no tweet",
    )
    require(
        source.count('completion(result: "")') >= 2,
        "timeline tweet lookup request and transport failure paths must complete",
    )
    require(
        "println(tweet)" not in source,
        "timeline tweet lookup must not log tweet identifiers",
    )
    require(
        "if tweet_result.isEmpty" in swipe_card,
        "TweepPickerView must ignore empty timeline tweet lookup completions",
    )


def check_profile_image_loading_guards():
    view_controller = read_text("Twinder/ViewController.swift")
    picture = read_text("Twinder/Picture.swift")

    require(
        "tweep!.image" not in view_controller,
        "ViewController must not force-unwrap the selected Tweep image URL",
    )
    require(
        "NSURL(string: url_string)!" not in view_controller,
        "ViewController must not force-unwrap profile image URL construction",
    )
    require(
        "if let selectedTweep = self.tweep" in view_controller,
        "ViewController must guard selected Tweep before image loading",
    )
    require(
        "if let imageURL = NSURL(string: url_string)" in view_controller,
        "ViewController must guard profile image URL construction",
    )
    require(
        "if let newImg = image" in view_controller,
        "ViewController must guard decoded profile images before assignment",
    )
    require(
        "func get(url: NSURL, handler: ((image: UIImage?, NSError!) -> Void)) -> NSURLSessionDataTask?" in picture,
        "Picture.get must expose optional decoded images and return a cancellable task",
    )
    require(
        "UIImage(data: data)!" not in picture,
        "Picture.get must not force-unwrap decoded image data",
    )
    require(
        "handler(image: nil, error)" in picture,
        "Picture.get must report failed image downloads without crashing",
    )
    transport_contracts = {
        'url.scheme?.lowercaseString != "https"': "require HTTPS profile image URLs",
        "maximumImageBytes = 5 * 1024 * 1024": "bound profile image responses to 5 MiB",
        "cachePolicy: .ReturnCacheDataElseLoad": "use the response cache when possible",
        "timeoutInterval: 15": "bound profile image request duration",
        "NSURLSession.sharedSession().dataTaskWithRequest(imageRequest": "download profile images with URLSession",
        "imageTask.resume()": "start the profile image task explicitly",
        "return imageTask": "return the cancellable profile image task",
        "if let httpResponse = response as? NSHTTPURLResponse": "validate HTTP responses",
        "httpResponse.statusCode >= 200 && httpResponse.statusCode < 300": "reject non-success HTTP responses",
        'mimeType?.hasPrefix("image/") == true': "reject non-image response bodies",
        "data.length <= self.maximumImageBytes": "reject oversized response bodies",
        "dispatch_async(dispatch_get_main_queue())": "deliver image completions on the main queue",
        'description: "Profile image could not be decoded"': "report image decode failures",
    }
    for fragment, behavior in transport_contracts.items():
        require(fragment in picture, f"Picture.get must {behavior}")
    require("NSURLConnection" not in picture, "Picture.get must not retain the legacy connection API")
    require("httpResponse!" not in picture, "Picture.get must not force-unwrap HTTP responses")


def check_person_profile_image_guards():
    source = read_text("Twinder/PersonController.swift")

    require(
        "Twitter().session().userName" not in source,
        "PersonController must not force-use the Twitter session username",
    )
    require(
        "if let session = Twitter.sharedInstance().session()" in source,
        "PersonController must guard the current Twitter session before profile image loading",
    )
    require(
        "NSURL(string: url)!" not in source,
        "PersonController must not force-unwrap profile image URL construction",
    )
    require(
        "if let imageURL = NSURL(string: url)" in source,
        "PersonController must guard profile image URL construction",
    )
    require(
        not re.search(r"^\s*let newImg = image\s*$", source, re.MULTILINE),
        "PersonController must not assign optional decoded profile image data directly",
    )
    require(
        "if let profileImage = image" in source,
        "PersonController must guard decoded profile images before resizing",
    )
    require(
        "self.peepImg!.image" not in source,
        "PersonController must not force-unwrap the profile image outlet when assigning",
    )


def check_table_profile_image_reuse_guards():
    source = read_text("Twinder/TableController.swift")

    for contract in (
        "cell.peepImage.image = nil",
        "if let imageURL = NSURL(string: fav_tweep.image_url)",
        "if let img = newImage",
        "if let currentIndexPath = tableView.indexPathForCell(cell)",
        "if currentIndexPath.isEqual(indexPath)",
    ):
        require(contract in source, f"saved-profile table image guard is missing: {contract}")

    require(
        "NSURL(string: fav_tweep.image_url)!" not in source,
        "saved-profile table must not force-unwrap profile image URLs",
    )
    require(
        "let img: UIImage = NewImage" not in source,
        "saved-profile table must not assign optional decoded image data directly",
    )


def check_swipe_card_image_identity_guard():
    source = read_text("Twinder/TweepPickerView.swift")
    contracts = (
        "private var imageTask: NSURLSessionDataTask?",
        "private var imageRequestGeneration = 0",
        "deinit {",
        "imageTask?.cancel()",
        "imageRequestGeneration += 1",
        "let requestGeneration = imageRequestGeneration",
        "self.imageView.image = nil",
        "imageTask = pic.get(imageURL, {[weak self] image, error in",
        "if let strongSelf = self",
        "if strongSelf.imageRequestGeneration == requestGeneration",
        "strongSelf.imageTask = nil",
        "if let currentTweep = strongSelf.tweep",
        "if currentTweep.image == urlString",
        "if let loadedImage = image",
        "strongSelf.imageView.image = loadedImage",
    )
    for contract in contracts:
        require(contract in source, f"swipe-card image identity guard is missing: {contract}")

    ordered_contracts = (
        "self.imageView.image = nil",
        "imageTask = pic.get(imageURL, {[weak self] image, error in",
        "if let strongSelf = self",
        "if strongSelf.imageRequestGeneration == requestGeneration",
        "strongSelf.imageTask = nil",
        "if let currentTweep = strongSelf.tweep",
        "if currentTweep.image == urlString",
        "if let loadedImage = image",
        "strongSelf.imageView.image = loadedImage",
    )
    positions = [source.index(contract) for contract in ordered_contracts]
    require(
        positions == sorted(positions),
        "swipe-card image reset, weak capture, identity, decode, and assignment guards must stay ordered",
    )
    require(
        "self.imageView.image = loadedImage" not in source,
        "swipe-card image completion must not strongly capture the card",
    )
    require(
        source.count("imageTask?.cancel()") >= 2,
        "swipe-card image tasks must be cancelled on replacement and deinitialization",
    )
    load_source = source[source.index("func loadImageView()") : source.index("func constructNameLabel()")]
    lifecycle_contracts = (
        "imageTask?.cancel()",
        "imageTask = nil",
        "imageRequestGeneration += 1",
        "let requestGeneration = imageRequestGeneration",
        "self.imageView.image = nil",
        "imageTask = pic.get(imageURL, {[weak self] image, error in",
        "if strongSelf.imageRequestGeneration == requestGeneration",
        "strongSelf.imageTask = nil",
        "if currentTweep.image == urlString",
        "strongSelf.imageView.image = loadedImage",
    )
    lifecycle_positions = [load_source.index(contract) for contract in lifecycle_contracts]
    require(
        lifecycle_positions == sorted(lifecycle_positions),
        "swipe-card cancellation, generation, identity, and assignment guards must stay ordered",
    )


def check_saved_profile_context_guard():
    source = read_text("Twinder/TableController.swift")

    require(
        "managedObjectContext!.executeFetchRequest" not in source,
        "saved-profile fetch must not force-unwrap the managed object context",
    )
    require(
        "if let context = managedObjectContext" in source,
        "saved-profile fetch must guard the managed object context",
    )
    require(
        "context.executeFetchRequest(fetchRequest, error: nil)" in source,
        "saved-profile fetch must execute through the guarded context",
    )


def check_swipe_card_remote_data_guards():
    source = read_text("Twinder/TweepPickerView.swift")

    require(
        "tweep!.image" not in source,
        "TweepPickerView must not force-unwrap Tweep image URLs",
    )
    require(
        "tweep!.name" not in source,
        "TweepPickerView must not force-unwrap Tweep names",
    )
    require(
        "tweep!.screen_name" not in source,
        "TweepPickerView must not force-unwrap Tweep screen names",
    )
    require(
        "NSURL(string: url_string)!" not in source,
        "TweepPickerView must not force-unwrap profile image URL construction",
    )
    require(
        "self.imageView.image = image" not in source,
        "TweepPickerView must guard decoded profile images before assignment",
    )
    require(
        "TWTRTweetView(tweet: tweet)" not in source,
        "TweepPickerView must guard loaded tweets before rendering",
    )
    require(
        "if let selectedTweep = self.tweep" in source,
        "TweepPickerView must guard selected Tweep data",
    )
    require(
        "if let imageURL = NSURL(string: urlString)" in source,
        "TweepPickerView must guard profile image URL construction",
    )
    require(
        "if let loadedImage = image" in source,
        "TweepPickerView must guard decoded profile images before assignment",
    )
    require(
        "if let loadedTweet = tweet" in source,
        "TweepPickerView must guard embedded tweet loading before rendering",
    )


def check_initial_card_data_guards():
    source = read_text("Twinder/TweepPickerViewController.swift")

    require(
        "func nextTweep() -> Tweep?" in source,
        "TweepPickerViewController must centralize guarded Tweep removal",
    )
    require(
        "return self.tweeps.removeAtIndex(0)" in source,
        "TweepPickerViewController must only remove Tweeps through nextTweep",
    )
    require(
        "if let firstTweep = self.nextTweep()" in source,
        "initial top card setup must guard the first fetched Tweep",
    )
    require(
        "if let secondTweep = self.nextTweep()" in source,
        "initial bottom card setup must guard the second fetched Tweep",
    )
    require(
        "if let nextTweep = self.nextTweep()" in source,
        "swipe replenishment must guard each next Tweep before card creation",
    )
    require(
        "self.tweeps.removeAtIndex(0))" not in source,
        "card setup must not remove Tweeps inline without the nextTweep guard",
    )


def check_core_data_failure_guards():
    app_delegate = read_text("Twinder/AppDelegate.swift")

    require(
        "abort()" not in app_delegate,
        "Core Data failure paths must not abort the app",
    )
    require(
        "error!.userInfo" not in app_delegate,
        "Core Data failure logging must not force-unwrap error userInfo",
    )
    require(
        "Failed to initialize persistent store" in app_delegate,
        "persistent store failures must be logged without crashing",
    )
    require(
        "Failed to save context" in app_delegate,
        "managed object context save failures must be logged without crashing",
    )


def check_login_session_guard():
    source = read_text("Twinder/LoginController.swift")

    require(
        'self.performSegueWithIdentifier("ViewController", sender: self)' in source,
        "LoginController must keep routing successful logins to the main view",
    )
    require(
        "if session != nil && error == nil" in source,
        "LoginController must only segue after TwitterKit returns a session without an error",
    )
    require(
        source.index("if session != nil && error == nil")
        < source.index('self.performSegueWithIdentifier("ViewController", sender: self)'),
        "LoginController must check the TwitterKit session before segueing",
    )
    require(
        "println(" not in source and "NSLog(" not in source,
        "LoginController must not log TwitterKit login errors or session details",
    )


def check_twitter_deep_link_guard():
    source = read_text("Twinder/DeepLinks.swift")

    contracts = {
        "let components = NSURLComponents()": "build Twitter deep links with URL components",
        'components.scheme = "twitter"': "keep the fixed Twitter URL scheme",
        'components.host = "user"': "keep the fixed Twitter user route",
        'NSURLQueryItem(name: "screen_name", value: screen_name)': "encode the screen name as one query item",
        "if let url = components.URL": "fail closed when URL construction fails",
        "UIApplication.sharedApplication().canOpenURL(url)": "check app routing before opening",
        "UIApplication.sharedApplication().openURL(url)": "open the validated bound URL",
    }
    for fragment, behavior in contracts.items():
        require(fragment in source, f"DeepLinks must {behavior}")

    require(
        '"twitter://user?screen_name=" + screen_name' not in source,
        "DeepLinks must not concatenate screen names into URL syntax",
    )
    require("url!" not in source, "DeepLinks must not force-unwrap constructed URLs")
    require(
        source.index("if let url = components.URL")
        < source.index("UIApplication.sharedApplication().canOpenURL(url)")
        < source.index("UIApplication.sharedApplication().openURL(url)"),
        "DeepLinks must construct, validate, and open the same URL in order",
    )

    documentation = {
        "README.md": "Twitter profile deep links encode the screen name as a query item",
        "SECURITY.md": "Twitter profile routes build the screen name as a URL query item",
        "VISION.md": "Encode Twitter profile deep-link query values",
        "CHANGES.md": "Built Twitter profile deep links from fixed URL components",
    }
    for relative_path, phrase in documentation.items():
        require(phrase in read_text(relative_path), f"{relative_path} must document safe Twitter deep links")


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")
    require(TWEEP_PICTURE_FAILURE_PLAN in plans, f"{TWEEP_PICTURE_FAILURE_PLAN.relative_to(ROOT)} must be present")
    require(INITIAL_CARD_PLAN in plans, f"{INITIAL_CARD_PLAN.relative_to(ROOT)} must be present")
    require(TIMELINE_TWEET_FAILURE_PLAN in plans, f"{TIMELINE_TWEET_FAILURE_PLAN.relative_to(ROOT)} must be present")
    require(TIMELINE_TWEET_PLAN in plans, f"{TIMELINE_TWEET_PLAN.relative_to(ROOT)} must be present")
    require(FRIENDS_LIST_DATA_PLAN in plans, f"{FRIENDS_LIST_DATA_PLAN.relative_to(ROOT)} must be present")
    require(CI_PLAN in plans, f"{CI_PLAN.relative_to(ROOT)} must be present")
    require(
        PROFILE_IMAGE_TRANSPORT_PLAN in plans,
        f"{PROFILE_IMAGE_TRANSPORT_PLAN.relative_to(ROOT)} must be present",
    )
    require(TABLE_IMAGE_REUSE_PLAN in plans, f"{TABLE_IMAGE_REUSE_PLAN.relative_to(ROOT)} must be present")
    require(
        SAVED_PROFILE_CONTEXT_PLAN in plans,
        f"{SAVED_PROFILE_CONTEXT_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        SWIPE_CARD_IMAGE_IDENTITY_PLAN in plans,
        f"{SWIPE_CARD_IMAGE_IDENTITY_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        SWIPE_CARD_IMAGE_CANCELLATION_PLAN in plans,
        f"{SWIPE_CARD_IMAGE_CANCELLATION_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        SAFE_TWITTER_DEEP_LINK_PLAN in plans,
        f"{SAFE_TWITTER_DEEP_LINK_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        MAKE_ROOT_PROTECTION_PLAN in plans,
        f"{MAKE_ROOT_PROTECTION_PLAN.relative_to(ROOT)} must be present",
    )

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def check_ci_baseline_docs():
    require(CI_WORKFLOW.exists(), ".github/workflows/check.yml is missing")
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")
    errors = validate_workflow(workflow)
    require(not errors, f"CI workflow must {errors[0]}" if errors else "")

    makefile = read_text("Makefile")
    makefile_lines = set(makefile.splitlines())
    require(
        "override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile_lines,
        "Makefile must protect commands rooted at the repository",
    )
    require("PYTHON ?= python3" in makefile_lines, "Makefile must preserve the Python command override")
    require('"$(ROOT)/scripts/check_ios_contracts.py"' in makefile, "Makefile must use the rooted checker path")
    require('"$(ROOT)/scripts/test_workflow_contract.py"' in makefile, "Makefile must run workflow contract mutations")
    require('cd "$(ROOT)" && xcodebuild' in makefile, "Makefile must run xcodebuild from the repository root")

    docs = {
        "README.md": ["GitHub Actions", "docs/plans/2026-06-10-ci-baseline.md"],
        "VISION.md": ["GitHub Actions"],
        "SECURITY.md": ["GitHub Actions", "make check"],
        "CHANGES.md": ["GitHub Actions"],
    }

    for relative_path, required_phrases in docs.items():
        text = read_text(relative_path)
        for phrase in required_phrases:
            require(phrase in text, f"{relative_path} must document {phrase}")


def main():
    checks = [
        check_project_files_parse,
        check_pod_lock_integrity,
        check_tweep_picture_json_guard,
        check_tweep_picture_failure_completion,
        check_api_json_guards,
        check_profile_image_loading_guards,
        check_person_profile_image_guards,
        check_table_profile_image_reuse_guards,
        check_swipe_card_image_identity_guard,
        check_saved_profile_context_guard,
        check_swipe_card_remote_data_guards,
        check_initial_card_data_guards,
        check_core_data_failure_guards,
        check_login_session_guard,
        check_twitter_deep_link_guard,
        check_docs_plans,
        check_ci_baseline_docs,
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
