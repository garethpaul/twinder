//
//  TweepCell.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/27/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation
import UIKit

class TweepCell: UITableViewCell {
    @IBOutlet var peepImage: UIImageView!
    private var imageTask: NSURLSessionDataTask?
    private var imageRequestGeneration = 0
    
    override init(style: UITableViewCellStyle, reuseIdentifier: String!) {
        super.init(style: UITableViewCellStyle.Value1, reuseIdentifier: reuseIdentifier)
    }

    required init(coder aDecoder: NSCoder) {
        //fatalError("init(coder:) has not been implemented")
        super.init(coder: aDecoder)
    }

    override func awakeFromNib() {
        super.awakeFromNib()
    }

    deinit {
        imageTask?.cancel()
    }

    override func prepareForReuse() {
        super.prepareForReuse()
        imageTask?.cancel()
        imageTask = nil
        imageRequestGeneration += 1
        peepImage.image = nil
    }

    func beginImageLoad() -> Int {
        imageTask?.cancel()
        imageTask = nil
        imageRequestGeneration += 1
        peepImage.image = nil
        return imageRequestGeneration
    }

    func ownImageTask(task: NSURLSessionDataTask?, generation: Int) {
        if imageRequestGeneration == generation {
            imageTask = task
        } else {
            task?.cancel()
        }
    }

    func finishImageLoad(generation: Int) -> Bool {
        if imageRequestGeneration == generation {
            imageTask = nil
            return true
        }
        return false
    }
}
