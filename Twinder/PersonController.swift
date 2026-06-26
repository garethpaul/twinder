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

    var profileImageTask: NSURLSessionDataTask?
    var profileImageGeneration = 0

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
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        loadProfileImage()
    }

    func loadProfileImage() {
        // Get User's Picture
        if let session = Twitter.sharedInstance().session() {
            let screenName = session.userName
            profileImageTask?.cancel()
            profileImageTask = nil
            profileImageGeneration += 1
            let requestGeneration = profileImageGeneration
            TweepPicture(screenName){ [weak self] (result: String) in
                dispatch_async(dispatch_get_main_queue()) {
                    if let strongSelf = self {
                        if strongSelf.profileImageGeneration == requestGeneration {
                            if let currentSession = Twitter.sharedInstance().session() {
                                if currentSession.userName == screenName {
                                    if result.isEmpty {
                                        return
                                    }
                                    let pic = Picture()
                                    let url = result.stringByReplacingOccurrencesOfString("_normal", withString: "", options: NSStringCompareOptions.LiteralSearch, range: nil)
                                    if let imageURL = NSURL(string: url) {
                                        strongSelf.profileImageTask = pic.get(imageURL, {[weak self] image, error in
                                            if let strongSelf = self {
                                                if strongSelf.profileImageGeneration == requestGeneration {
                                                    strongSelf.profileImageTask = nil
                                                    if let currentSession = Twitter.sharedInstance().session() {
                                                        if currentSession.userName == screenName {
                                                            if let profileImage = image {
                                                                let circle = CircleImage(RBResizeImage(profileImage, CGSize(width: 150, height: 150)))
                                                                strongSelf.peepImg.image = circle
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        })
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    override func viewWillDisappear(animated: Bool) {
        profileImageGeneration += 1
        profileImageTask?.cancel()
        profileImageTask = nil
        super.viewWillDisappear(animated)
    }

    deinit {
        profileImageTask?.cancel()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
}
