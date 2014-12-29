//
//  Tweep.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/26/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//
import Foundation

class Tweep {
    var name: String
    var image: String
    var screen_name: String

    init(name: String, image: String, screen_name: String) {
        self.name = name
        self.image = image
        self.screen_name = screen_name
    }
}