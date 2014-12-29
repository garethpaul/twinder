//
//  DeepLinks.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/27/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation

func twtrScreenName(screen_name: String){
    let deepLinkUrl: NSString = "twitter://user?screen_name=" + screen_name
    let url = NSURL(string: (deepLinkUrl))
    if UIApplication.sharedApplication().canOpenURL(url!) {
        // url is good to go
        UIApplication.sharedApplication().openURL(url!)
    }
}
