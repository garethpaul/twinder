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

        if(self.tweep != nil) {
            let pic = Picture()
            let url_string = tweep!.image
            pic.get(NSURL(string: url_string)!, {image, error in
                let newImg = image
                self.imageView.image = newImg

            })

        }
    }
}
