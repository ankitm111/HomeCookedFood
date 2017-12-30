//
//  SellerDataViewModel.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/7/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import UIKit

//{
//    "date_time": "20171110-133927",
//    "max_count": 5,
//    "meal_items": [
//    [
//    "chole",
//    2
//    ],
//    [
//    "bhature",
//    2
//    ]
//    ],
//    "price": 10,
//    "tagnames": [
//    "dal, tadka"
//    ]
//}

struct MealItems: Codable {
    
}

struct Meal: Codable {
    let date_time: String
    let max_count: UInt
    let meal_items: [MealItems]
    let price: UInt
    let tagnames: [String]
}

class SellerDataViewModel {
    
    var items: [[SellerTableTypeCellProtocol]]
    var sectionTitle: [String]
    var completion: (() -> ())? = nil
    
    func rowCount() -> Int {
        // order dates
        return self.items.count
    }
    
    init() {
        
        self.sectionTitle = ["Tiffin1"]
        self.items = [[SellerViewModel(name: "rice", count: 1),
                       SellerViewModel(name: "dal", count: 1),
                       SellerViewModel(name: "curd", count: 2),
                       OrderDateViewModel(lastOrderdate: Date(), pickupOrderdate: Date())]]
        makeAwesomeDinnerRequest()

    }
    
   private func makeAwesomeDinnerRequest() {
        
        //Get the url from url string
        let url:URL = URL(string: "http://127.0.0.1:5000/hcf/users/provider/meals/awesomedinner")!
        
        //Get the session instance
        let session = URLSession.shared
        
        //Create Mutable url request
        var request = URLRequest(url: url as URL)
        
        //Set the http method type
        request.httpMethod = "GET"
        
        //Set the cache policy
        request.cachePolicy = URLRequest.CachePolicy.reloadIgnoringCacheData
        
        request.addValue("Basic YW5raXRtMTEyOnB5dGhvbg==", forHTTPHeaderField: "Authorization")

        let task = session.dataTask(with: request as URLRequest) { [weak self]
            (data, response, error) in
            
            guard let data = data as Data?, let _:URLResponse = response  , error == nil else {
                print(error!)
                return
            }
            do {
                let decoder = JSONDecoder()
                let meal = try decoder.decode(Meal.self, from: data)
                print(meal)
                self?.completion?()
            } catch let e {
                print("catch \(e)")
            }
            
        }
        
        //resume the task
        task.resume()
    }
}
