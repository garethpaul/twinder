//
//  TweepPickerView.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/26/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

//

import Foundation
import UIKit
import TwitterKit

class TweepPickerView : MDCSwipeToChooseView {
    var tweep: Tweep?
    var infoView: UIView = UIView()

    required init(coder: NSCoder) {
        super.init(coder: coder)
    }

    init(frame: CGRect, tweep: Tweep, options: MDCSwipeToChooseViewOptions) {
        super.init(frame: frame, options: options)

        self.tweep = tweep

        // Setup resizing masks
        self.autoresizingMask = UIViewAutoresizing.FlexibleHeight |
            UIViewAutoresizing.FlexibleWidth |
            UIViewAutoresizing.FlexibleBottomMargin

        self.imageView.autoresizingMask = self.autoresizingMask
        self.imageView.contentMode = UIViewContentMode.ScaleAspectFill

        self.imageView.frame = CGRectMake(
            2,
            2,
            CGRectGetWidth(self.bounds) - 4,
            CGRectGetHeight(self.bounds) - 4
        )

        constructInfoView()
        loadImageView()
    }

    func constructInfoView() {
        let infoViewHeight: CGFloat = 150

        let infoViewFrame: CGRect = CGRectMake(
            0,
            CGRectGetHeight(self.bounds) - infoViewHeight,
            CGRectGetWidth(self.bounds),
            infoViewHeight
        )

        infoView = UIView(frame: infoViewFrame)
        infoView.backgroundColor = UIColor.whiteColor()
        infoView.clipsToBounds = true
        infoView.autoresizingMask = UIViewAutoresizing.FlexibleWidth |
            UIViewAutoresizing.FlexibleTopMargin;

        self.addSubview(infoView)

        constructNameLabel()
    }

    func loadImageView() {
        if let selectedTweep = self.tweep {
            let pic = Picture()
            let urlString = selectedTweep.image
            if let imageURL = NSURL(string: urlString) {
                pic.get(imageURL, {image, error in
                    if let loadedImage = image {
                        self.imageView.image = loadedImage
                    }
                })
            }
        }


    }

    func constructNameLabel() {
        //        let nameLabelFrame = CGRectMake(
        //            5,
        //            5,
        //            CGRectGetWidth(infoView.bounds),
        //            18
        //        )

        let nameLabel: UILabel = UILabel(frame: infoView.bounds)
        if let selectedTweep = self.tweep {
            nameLabel.text = "\(selectedTweep.name)"
        }
        nameLabel.textAlignment = NSTextAlignment.Center
        //nameLabel.textRectForBounds(nameLabel.bounds, limitedToNumberOfLines: 1)
        nameLabel.font = UIFont.systemFontOfSize(20.0)
        nameLabel.adjustsFontSizeToFitWidth = true
        let api = APIClient()
        if let selectedTweep = self.tweep {
            let screenName = selectedTweep.screen_name
            api.getTweet(screenName) { (tweet_result: String) in
                if tweet_result.isEmpty {
                    return
                }
                Twitter.sharedInstance().APIClient.loadTweetWithID(tweet_result) { (tweet: TWTRTweet!, error: NSError!) in
                    if let loadedTweet = tweet {
                        let tweetView = TWTRTweetView(tweet: loadedTweet)
                        tweetView.showBorder = false
                        self.infoView.addSubview(tweetView)
                    }
                }
            }
        }




        //infoView.addSubview(nameLabel)
    }
}
