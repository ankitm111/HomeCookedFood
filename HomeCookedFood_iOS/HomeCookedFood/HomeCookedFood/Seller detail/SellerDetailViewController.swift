//
//  SellerDetailViewController.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 11/6/17.
//  Copyright © 2017 Arpit Mehta. All rights reserved.
//

import UIKit

class SellerDetailViewController: UIViewController {

    @IBOutlet weak var nameLabel: UITextView!
    @IBOutlet weak var itemLabel: UITextView!
    @IBOutlet weak var dateLabel: UITextView!
    @IBOutlet weak var tagsLabel: UITextView!
    
    @IBAction func onCloseButtonTapped(_ sender: Any) {
        
        dismiss(animated: true, completion: nil)
    }
    
    weak var parentVC: UIViewController?
    init(parent: UIViewController) {
        self.parentVC = parent
        super.init(nibName: nil, bundle: nil)
    }
    
    override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
        super.init(nibName: nil, bundle: nil)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
