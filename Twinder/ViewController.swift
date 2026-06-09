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
    
    override func viewDidLoad() {
        super.viewDidLoad()

        if let selectedTweep = self.tweep {
            let pic = Picture()
            let url_string = selectedTweep.image
            if let imageURL = NSURL(string: url_string) {
                pic.get(imageURL, {image, error in
                    if let newImg = image {
                        self.imageView.image = newImg
                    }
                })
            }

        }
    }
}
