//
//  FavTweets.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/27/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation
import CoreData

class FavTweets: NSManagedObject {

    @NSManaged var screen_name: String
    @NSManaged var image_url: String
    @NSManaged var name: String

}
