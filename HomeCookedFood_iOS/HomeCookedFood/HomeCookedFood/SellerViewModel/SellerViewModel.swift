//
//  ItemViewModel.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/20/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import Foundation

class SellerViewModel: SellerTableTypeCellProtocol {
    var type: SellerTableCellType {
        get {
            return .itemCell
        }
    }
    
    let name: String
    let count: UInt
    
    init(name: String, count: UInt) {
        self.name = name
        self.count = count
    }
}
