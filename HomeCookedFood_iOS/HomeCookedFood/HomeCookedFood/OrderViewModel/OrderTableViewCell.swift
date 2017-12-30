//
//  OrderTableViewCell.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/20/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import UIKit

class OrderTableViewCell: UITableViewCell {

    
    @IBOutlet weak var orderByLabel: UILabel!
    @IBOutlet weak var pickupDateLabel: UILabel!
    @IBOutlet weak var costLabel: UILabel!
    
    var item: SellerTableTypeCellProtocol? {
        didSet {
            guard let item = item as? OrderDateViewModel else {
                return
            }
            
            orderByLabel.text = "Order by: " + String(describing: item.lastOrderdate)
            pickupDateLabel.text = "Pickup by: " + String(describing: item.pickupOrderdate)
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
    override func layoutSubviews() {
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    
    
}
