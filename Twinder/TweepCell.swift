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
}
