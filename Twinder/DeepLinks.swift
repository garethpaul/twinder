//
//  DeepLinks.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/27/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation
import UIKit

func twtrScreenName(screen_name: String){
    let components = NSURLComponents()
    components.scheme = "twitter"
    components.host = "user"
    components.queryItems = [NSURLQueryItem(name: "screen_name", value: screen_name)]

    if let url = components.URL {
        if UIApplication.sharedApplication().canOpenURL(url) {
            UIApplication.sharedApplication().openURL(url)
        }
    }
}
