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
        let pic = Picture()
        let url_string = tweep!.image
        pic.get(NSURL(string: url_string)!, {image, error in
            let newImg = image
            self.imageView.image = image
        })


    }

    func constructNameLabel() {
        //        let nameLabelFrame = CGRectMake(
        //            5,
        //            5,
        //            CGRectGetWidth(infoView.bounds),
        //            18
        //        )

        let nameLabel: UILabel = UILabel(frame: infoView.bounds)
        nameLabel.text = "\(tweep!.name)"
        nameLabel.textAlignment = NSTextAlignment.Center
        //nameLabel.textRectForBounds(nameLabel.bounds, limitedToNumberOfLines: 1)
        nameLabel.font = UIFont.systemFontOfSize(20.0)
        nameLabel.adjustsFontSizeToFitWidth = true
        let api = APIClient()
        let screen_name = tweep!.screen_name
        api.getTweet(screen_name) { (tweet_result: String) in


            Twitter.sharedInstance().APIClient.loadTweetWithID(tweet_result) { (tweet: TWTRTweet!, error: NSError!) in
                let tweetView = TWTRTweetView(tweet: tweet)
                tweetView.showBorder = false
                self.infoView.addSubview(tweetView)
            }

        }




        //infoView.addSubview(nameLabel)
    }
}

