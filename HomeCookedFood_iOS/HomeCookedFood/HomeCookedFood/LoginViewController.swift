//
//  LoginViewController.swift
//  HomeCookedFood
//
//  Created by Arpit Mehta on 1/9/18.
//  Copyright © 2018 Arpit Mehta. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit

class LoginViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        if ((FBSDKAccessToken.current()) != nil) {
            // User is logged in, do work such as go to next view controller.
            
            return
        }


        // Do any additional setup after loading the view.
        let loginButton = FBSDKLoginButton()
        loginButton.center = self.view.center
        
        // Extend the code sample from 6a. Add Facebook Login to Your Code
        // Add to your viewDidLoad method:
        loginButton.readPermissions = ["public_profile", "email"]
        
        self.view.addSubview(loginButton)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        //showLandingPage
        
        self.performSegue(withIdentifier: "showLandingPage", sender: self)
//        let vc = LandingPageViewController()
//        
//        self.navigationController?.pushViewController(vc, animated: true)
    }
    

    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        
        
    }
 

}

