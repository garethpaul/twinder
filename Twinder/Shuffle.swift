//
//  Shuffle.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/26/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation

func shuffle<C: MutableCollectionType where C.Index == Int>(var list: C) -> C {
    let count = countElements(list)
    for i in 0..<(count - 1) {
        let j = Int(arc4random_uniform(UInt32(count - i))) + i
        swap(&list[i], &list[j])
    }
    return list
}