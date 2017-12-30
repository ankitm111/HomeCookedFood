//
//  BuyerSearchViewController.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 12/18/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import UIKit

class BuyerSearchViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    
    
    // MARK: - Properties
    @IBOutlet var tableView: UITableView!
    @IBOutlet var searchFooter: SearchFooter!

    let searchController = UISearchController(searchResultsController: nil)

    
    override func viewDidLoad() {
        super.viewDidLoad()

        
        // Setup the Search Controller
        searchController.searchResultsUpdater = self
        searchController.obscuresBackgroundDuringPresentation = false
        searchController.searchBar.placeholder = "Search Tiffins"
        navigationItem.searchController = searchController
        definesPresentationContext = true
        
        searchController.searchBar.scopeButtonTitles = ["All", "Vegetarian", "Non Vegetarian"]
        searchController.searchBar.delegate = self
        
        // Setup the search footer
        tableView.tableFooterView = searchFooter


        // Do any additional setup after loading the view.
    }

    // MARK: - Table View
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        
        return 5
//        if isFiltering() {
//            searchFooter.setIsFilteringToShow(filteredItemCount: filteredCandies.count, of: candies.count)
//            return filteredCandies.count
//        }
//
//        searchFooter.setNotFiltering()
//        return candies.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "TiffinCell", for: indexPath)
//        let candy: Candy
//        if isFiltering() {
//            candy = filteredCandies[indexPath.row]
//        } else {
//            candy = candies[indexPath.row]
//        }
        cell.textLabel!.text = "Arpit"
        return cell
    }

    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}

extension BuyerSearchViewController: UISearchResultsUpdating {
    // MARK: - UISearchResultsUpdating Delegate
    func updateSearchResults(for searchController: UISearchController) {
        let searchBar = searchController.searchBar
        let scope = searchBar.scopeButtonTitles![searchBar.selectedScopeButtonIndex]
//        filterContentForSearchText(searchController.searchBar.text!, scope: scope)
    }
}

extension BuyerSearchViewController: UISearchBarDelegate {
    // MARK: - UISearchBar Delegate
    func searchBar(_ searchBar: UISearchBar, selectedScopeButtonIndexDidChange selectedScope: Int) {
//        filterContentForSearchText(searchBar.text!, scope: searchBar.scopeButtonTitles![selectedScope])
    }
}
