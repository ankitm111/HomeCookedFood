//
//  SellerTableViewCell.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/13/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import UIKit

class SellerTableViewCell: UITableViewCell {

    @IBOutlet weak var testLabel: UILabel!
    @IBOutlet weak var itemCount: UILabel!
    
    var item: SellerTableTypeCellProtocol? {
        didSet {
            guard let item = item as? SellerViewModel else {
                return
            }
            
            testLabel.text = item.name
//            itemCount.text = String(item.count)
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
    override func layoutSubviews() {
    }
    
}
