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
    private var imageTask: NSURLSessionDataTask?
    private var imageRequestGeneration = 0
    private var tweetRequestGeneration = 0

    deinit {
        imageTask?.cancel()
    }

    required init(coder: NSCoder) {
        super.init(coder: coder)
    }

    override func didMoveToWindow() {
        super.didMoveToWindow()
        if self.window == nil {
            tweetRequestGeneration += 1
        }
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
        imageTask?.cancel()
        imageTask = nil
        imageRequestGeneration += 1
        let requestGeneration = imageRequestGeneration
        self.imageView.image = nil
        if let selectedTweep = self.tweep {
            let pic = Picture()
            let urlString = selectedTweep.image
            if let imageURL = NSURL(string: urlString) {
                imageTask = pic.get(imageURL, {[weak self] image, error in
                    if let strongSelf = self {
                        if strongSelf.imageRequestGeneration == requestGeneration {
                            strongSelf.imageTask = nil
                            if let currentTweep = strongSelf.tweep {
                                if currentTweep.image == urlString {
                                    if let loadedImage = image {
                                        strongSelf.imageView.image = loadedImage
                                    }
                                }
                            }
                        }
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
            tweetRequestGeneration += 1
            let requestGeneration = tweetRequestGeneration
            api.getTweet(screenName) { [weak self] (tweet_result: String) in
                if let strongSelf = self {
                    if strongSelf.tweetRequestGeneration == requestGeneration {
                        if let currentTweep = strongSelf.tweep {
                            if currentTweep.screen_name == screenName {
                                if tweet_result.isEmpty {
                                    return
                                }
                                Twitter.sharedInstance().APIClient.loadTweetWithID(tweet_result) { [weak self] (tweet: TWTRTweet!, error: NSError!) in
                                    dispatch_async(dispatch_get_main_queue()) {
                                        if let strongSelf = self {
                                            if strongSelf.tweetRequestGeneration == requestGeneration {
                                                if let currentTweep = strongSelf.tweep {
                                                    if currentTweep.screen_name == screenName {
                                                        if let loadedTweet = tweet {
                                                            let tweetView = TWTRTweetView(tweet: loadedTweet)
                                                            tweetView.showBorder = false
                                                            strongSelf.infoView.addSubview(tweetView)
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }




        //infoView.addSubview(nameLabel)
    }
}
