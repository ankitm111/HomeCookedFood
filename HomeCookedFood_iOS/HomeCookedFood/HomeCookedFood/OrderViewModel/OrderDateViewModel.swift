//
//  OrderDate.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/20/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import Foundation

class OrderDateViewModel: SellerTableTypeCellProtocol {
    
    let lastOrderdate: Date
    let pickupOrderdate: Date

    init(lastOrderdate: Date, pickupOrderdate: Date) {
        self.lastOrderdate = lastOrderdate
        self.pickupOrderdate = pickupOrderdate
    }
    
    var type: SellerTableCellType {
        get { return .costCell }
    }
    
}
