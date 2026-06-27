//
//  ViewController.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/26/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import UIKit
import Foundation

class ViewController: UIViewController {

    @IBOutlet weak var imageView: UIImageView!

    var tweep: Tweep?
    var lView: UIImageView!
    var profileImageTask: NSURLSessionDataTask?
    var profileImageGeneration = 0

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        loadProfileImage()
    }

    override func viewWillDisappear(animated: Bool) {
        profileImageGeneration += 1
        profileImageTask?.cancel()
        profileImageTask = nil
        super.viewWillDisappear(animated)
    }

    func loadProfileImage() {
        profileImageTask?.cancel()
        profileImageTask = nil
        profileImageGeneration += 1
        imageView.image = nil
        let requestGeneration = profileImageGeneration

        if let selectedTweep = self.tweep {
            let pic = Picture()
            let imageURLString = selectedTweep.image
            if let imageURL = NSURL(string: imageURLString) {
                profileImageTask = pic.get(imageURL, {[weak self] image, error in
                    if let strongSelf = self {
                        if strongSelf.profileImageGeneration == requestGeneration {
                            if let currentTweep = strongSelf.tweep {
                                if currentTweep.image == imageURLString {
                                    if let newImg = image {
                                        strongSelf.imageView.image = newImg
                                    }
                                }
                            }
                        }
                    }
                })
            }
        }
    }

    deinit {
        profileImageTask?.cancel()
    }
}
