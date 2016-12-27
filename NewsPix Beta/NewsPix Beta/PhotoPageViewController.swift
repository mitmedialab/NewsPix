//
//  PhotoPageViewController.swift
//  NewsPix Beta
//
//  Created by UROP on 7/27/16.
//  Copyright © 2016 UROP. All rights reserved.
//

import UIKit
import Social

class PhotoPageViewController: UIPageViewController {
    
    let defaults = UserDefaults.standard
    var orderedViewControllers: [UIViewController] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        dataSource = self
        
        //Download content from server
        if images.count == 0 {
            altParseJSON(getData("http://dev.newspix.today/get_all_stories/keene_sentinel")!)
        }
        //Provide default images if server connection fails
        if images.count == 0 {
            names = ["Newspix", "Keene Sentinel"]
            images = [UIImage(named: "newspixlogo.png")!, UIImage(named: "Keene Sentinel.png")!]
            urls = [URL(string: "http://dev.newspix.today")!, URL(string: "http://www.sentinelsource.com/")!]
        }
        
        //Populate orderedViewController with controllers corresponding to each photo
        for num in 0...images.count - 1 {
            let controller = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "MainViewController") as! ViewController
            controller.index = num
            orderedViewControllers.append(controller)
        }
        
        //Initialize first ViewController
        if let firstViewController = orderedViewControllers.first {
            setViewControllers([firstViewController],
                direction: .forward,
                animated: true,
                completion: nil)
        }
        
    }
    
    //Set title displayed on the Navigation Bar to the name of the news organization
    override func viewWillAppear(_ animated: Bool) {
        navigationItem.title = "Sentinel Source"
    }
    
    //Sharing Function
    @IBAction func shareButtonClicked(_ sender: UIBarButtonItem) {
        let urlToShare = urls[(self.viewControllers![0] as! ViewController).index]
        let actionSheetController: UIAlertController = UIAlertController(title: "Share", message: nil, preferredStyle: .actionSheet)
        
        let cancelAction: UIAlertAction = UIAlertAction(title: "Cancel", style: .cancel) { action -> Void in
            //Dismiss the action sheet
        }
        actionSheetController.addAction(cancelAction)

        let shareFacebookAction: UIAlertAction = UIAlertAction(title: "Facebook", style: .default) { action -> Void in
            //Check if user is logged in for Facebook
            if !SLComposeViewController.isAvailable(forServiceType: SLServiceTypeFacebook) {
                self.showAlertMessage("Log into Facebook in Settings to enable sharing on Facebook.", underlyingView: self)
            }
            else {
                let fbShare: SLComposeViewController = SLComposeViewController(forServiceType: SLServiceTypeFacebook)
                fbShare.add(urlToShare)
                self.present(fbShare, animated: true, completion: nil)
            }
        }
//        shareFacebookAction.setValue(UIImage(named: "Facebook Filled.png"), forKey: "image")
        actionSheetController.addAction(shareFacebookAction)

        let shareTwitterAction: UIAlertAction = UIAlertAction(title: "Twitter", style: .default) { action -> Void in
            //Check if user is logged in for Twitter
            if !SLComposeViewController.isAvailable(forServiceType: SLServiceTypeTwitter) {
                self.showAlertMessage("Log into Twitter in Settings to enable sharing on Twitter.", underlyingView: self)
            }
            else {
                let tShare: SLComposeViewController = SLComposeViewController(forServiceType: SLServiceTypeTwitter)
                
                self.present(tShare, animated: true, completion: nil)
            }
        }
//        shareTwitterAction.setValue(UIImage(named: "Twitter Filled.png"), forKey: "image")
        actionSheetController.addAction(shareTwitterAction)
        
        self.present(actionSheetController, animated: true, completion: nil)
    }
    
    func showAlertMessage(_ message: String!, underlyingView: UIViewController) {
        let alertController = UIAlertController(title: "Not Logged In", message: message, preferredStyle: UIAlertControllerStyle.alert)
        alertController.addAction(UIAlertAction(title: "Okay", style: UIAlertActionStyle.default, handler: nil))
        underlyingView.present(alertController, animated: true, completion: nil)
    }

}

// MARK: UIPageViewControllerDataSource
// Sourced from: https://spin.atomicobject.com/2015/12/23/swift-uipageviewcontroller-tutorial/

extension PhotoPageViewController: UIPageViewControllerDataSource {
    
    func pageViewController(_ pageViewController: UIPageViewController,
        viewControllerBefore viewController: UIViewController) -> UIViewController? {
            guard let viewControllerIndex = orderedViewControllers.index(of: viewController) else {
                return nil
            }
            
            let previousIndex = viewControllerIndex - 1
            
            // User is on the first view controller and swiped left to loop to
            // the last view controller.
            guard previousIndex >= 0 else {
                return orderedViewControllers.last
            }
            
            guard orderedViewControllers.count > previousIndex else {
                return nil
            }
            
            return orderedViewControllers[previousIndex]
    }
    
    func pageViewController(_ pageViewController: UIPageViewController,
        viewControllerAfter viewController: UIViewController) -> UIViewController? {
            guard let viewControllerIndex = orderedViewControllers.index(of: viewController) else {
                return nil
            }
            
            let nextIndex = viewControllerIndex + 1
            let orderedViewControllersCount = orderedViewControllers.count
            
            // User is on the last view controller and swiped right to loop to
            // the first view controller.
            guard orderedViewControllersCount != nextIndex else {
                return orderedViewControllers.first
            }
            
            guard orderedViewControllersCount > nextIndex else {
                return nil
            }
            
            return orderedViewControllers[nextIndex]
    }
    
}
