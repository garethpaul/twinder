//
//  LoginController.swift
//

import UIKit
import TwitterKit
import CoreData

class LoginController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        self.view.backgroundColor = toColor("5E41A3")
        // If the login is successful then move the user to the viewController
        let logInButton = TWTRLogInButton(logInCompletion: {
            (session: TWTRSession!, error: NSError!) in
            

            self.performSegueWithIdentifier("ViewController", sender: self)
        })

        // Append the login button to the view
        logInButton.center = self.view.center
        self.view.addSubview(logInButton)

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    
}

