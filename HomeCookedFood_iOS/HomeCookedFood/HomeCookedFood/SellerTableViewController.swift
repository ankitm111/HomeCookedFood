//
//  MasterViewController.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/6/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import UIKit

class SellerTableViewController: UITableViewController {

    var detailViewController: DetailViewController? = nil
    var objects: [Any] = []
    let sellerDataSource: SellerDataViewModel
 
    required init?(coder aDecoder: NSCoder) {
        
        self.sellerDataSource = SellerDataViewModel()
        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        tableView.register(UINib.init(nibName: "SellerTableViewCell", bundle: nil),
                                 forCellReuseIdentifier: "SellerTableViewCell")
        
        tableView.register(UINib.init(nibName: "OrderTableViewCell", bundle: nil),
                                forCellReuseIdentifier: "OrderTableViewCell")

        tableView.dataSource = self
        tableView.delegate = self
        
        tableView.translatesAutoresizingMaskIntoConstraints = false

        tableView.rowHeight = UITableViewAutomaticDimension
        tableView.estimatedRowHeight = 300
        sellerDataSource.completion = { [weak self] () -> ()  in
            DispatchQueue.main.async {
                self?.tableView.reloadData()
            }
        }
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }


//    @objc
//    func presentModally(_ sender: Any) {
//
//        let modalViewController = SellerDetailViewController(parent: self)
//        modalViewController.modalPresentationStyle = .overCurrentContext
//        present(modalViewController, animated: true, completion: nil)
//
//    }

    // MARK: - Segues

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "showDetail" {
            if let indexPath = tableView.indexPathForSelectedRow {
                let object = objects[indexPath.row] as! NSDate
                let controller = (segue.destination as! UINavigationController).topViewController as! DetailViewController
                controller.detailItem = object
                controller.navigationItem.leftBarButtonItem = splitViewController?.displayModeButtonItem
                controller.navigationItem.leftItemsSupplementBackButton = true
            }
        }
    }

    // MARK: - Table View
//    let data = [["puri", "paneer", "lassi"], ["rice", "chole", "chai"], ["chaat", "salt lassi", "paan"]]
//    let countData = [[2,4,6], [1,2,5], [1,6,3]]
//    let sectionHeader = ["North Indian Tiffin", "South Indian Tiffin", "Chaat Tiffin"]


    override func numberOfSections(in tableView: UITableView) -> Int {
        return sellerDataSource.rowCount()
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return sellerDataSource.items[section].count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        switch sellerDataSource.items[indexPath.section][indexPath.row].type {
        case .costCell:
            if let cell = tableView.dequeueReusableCell(withIdentifier: "OrderTableViewCell", for: indexPath) as? OrderTableViewCell {
                cell.item = sellerDataSource.items[indexPath.section][indexPath.row]
                return cell
            }
            
        case .itemCell:
            if let cell = tableView.dequeueReusableCell(withIdentifier: "SellerTableViewCell", for: indexPath) as? SellerTableViewCell {
                cell.item = sellerDataSource.items[indexPath.section][indexPath.row]
                return cell
            }
        }
        
        return UITableViewCell()
        
    }
    
    override func tableView(_ tableView: UITableView, estimatedHeightForRowAt indexPath: IndexPath) -> CGFloat {
        return UITableViewAutomaticDimension
    }
    
    override func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return UITableViewAutomaticDimension
    }


    override func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return sellerDataSource.sectionTitle[section]
    }

}

