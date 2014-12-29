//
//  PersonController.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/28/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation
//
//  LoginController.swift
//

import UIKit
import TwitterKit
import CoreData
import QuartzCore

class PersonController: UIViewController {

    // MARK: LogOut Button
    @IBOutlet var logoutBtn: UIButton!
    @IBAction func logOutBtn(sender: AnyObject) {
        Twitter().logOut()
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let signInViewController: AnyObject! = storyboard.instantiateViewControllerWithIdentifier("LoginController")
        let appDelegate = UIApplication.sharedApplication().delegate as AppDelegate
        appDelegate.window?.rootViewController = signInViewController as? UIViewController
    }

    // MARK: Rounded image showing logged in user
    @IBOutlet var peepImg: UIImageView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Setup logout button
        logoutBtn.backgroundColor = toColor("5E41A3")
        logoutBtn.setTitleColor(toColor("fefefe"), forState: UIControlState.Normal)
        logoutBtn.layer.cornerRadius = 10;
        logoutBtn.clipsToBounds = true
        logoutBtn.sizeToFit()

        // Get User's Picture
        TweepPicture(Twitter().session().userName){ (result: String) in
            let pic = Picture()
            let url = result.stringByReplacingOccurrencesOfString("_normal", withString: "", options: NSStringCompareOptions.LiteralSearch, range: nil)
            pic.get(NSURL(string: url)!, {image, error in
                let newImg = image
                let circle = CircleImage(RBResizeImage(newImg, CGSize(width: 150, height: 150)))
                self.peepImg!.image = circle


            })
        }

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
}

