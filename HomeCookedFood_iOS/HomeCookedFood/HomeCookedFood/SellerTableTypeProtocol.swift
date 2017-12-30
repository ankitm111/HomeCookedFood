//
//  SellerTableTypeProtocol.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/20/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import Foundation
enum SellerTableCellType {
    case itemCell
    case costCell
}

protocol SellerTableTypeCellProtocol {
    var type: SellerTableCellType { get }
}

// defaults
extension SellerTableTypeCellProtocol {
    var rowCount: Int {
        get { return 1 }
    }
}

