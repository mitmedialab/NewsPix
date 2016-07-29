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
    
    var orderedViewControllers: [UIViewController] = []
    var isFirstTimeClickingShare: Bool = true
    
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
            urls = [NSURL(string: "http://dev.newspix.today")!, NSURL(string: "http://www.sentinelsource.com/")!]
        }
        
        //Populate orderedViewController with controllers corresponding to each photo
        for num in 0...images.count - 1 {
            let controller = UIStoryboard(name: "Main", bundle: nil).instantiateViewControllerWithIdentifier("MainViewController") as! ViewController
            controller.index = num
            orderedViewControllers.append(controller)
        }
        
        //Initialize first ViewController
        if let firstViewController = orderedViewControllers.first {
            setViewControllers([firstViewController],
                direction: .Forward,
                animated: true,
                completion: nil)
        }
        
    }
    
    //Set title displayed on the Navigation Bar to the name of the news organization
    override func viewWillAppear(animated: Bool) {
        navigationItem.title = "Sentinel Source"
    }
    
    //Sharing Functions
    @IBAction func shareButtonClicked(sender: UIBarButtonItem) {
        let myWebsite = urls[(self.viewControllers![0] as! ViewController).index]
        let objectsToShare = [myWebsite]
        let activityVC = UIActivityViewController(activityItems: objectsToShare, applicationActivities: nil)
        activityVC.excludedActivityTypes = [UIActivityTypePostToWeibo,
            UIActivityTypeMessage,
            UIActivityTypeMail,
            UIActivityTypePrint,
            UIActivityTypeCopyToPasteboard,
            UIActivityTypeAssignToContact,
            UIActivityTypeSaveToCameraRoll,
            UIActivityTypePostToFlickr,
            UIActivityTypePostToVimeo,
            UIActivityTypePostToTencentWeibo]
        
        self.presentViewController(activityVC, animated: true, completion: nil)
        
        //Check if user is logged into Twitter/Facebook, prompt them to sign in if not.
        if isFirstTimeClickingShare {
            let twitterLoggedIn = SLComposeViewController.isAvailableForServiceType(SLServiceTypeTwitter)
            let facebookLoggedIn = SLComposeViewController.isAvailableForServiceType(SLServiceTypeFacebook)
            if !twitterLoggedIn && !facebookLoggedIn {
                self.showAlertMessage("Log into Facebook/Twitter in Settings to enable sharing.", underlyingView: activityVC)
            }
            else if !twitterLoggedIn {
                self.showAlertMessage("Log into Twitter in Settings to enable sharing on Twitter.", underlyingView: activityVC)
            }
            else if !facebookLoggedIn {
                self.showAlertMessage("Log into Facebook in Settings to enable sharing on Facebook.", underlyingView: activityVC)
            }
            isFirstTimeClickingShare = false
        }
        
    }
    
    func showAlertMessage(message: String!, underlyingView: UIViewController) {
        let alertController = UIAlertController(title: "Not Logged In", message: message, preferredStyle: UIAlertControllerStyle.Alert)
        alertController.addAction(UIAlertAction(title: "Okay", style: UIAlertActionStyle.Default, handler: nil))
        underlyingView.presentViewController(alertController, animated: true, completion: nil)
    }

}

// MARK: UIPageViewControllerDataSource
// Sourced from: https://spin.atomicobject.com/2015/12/23/swift-uipageviewcontroller-tutorial/

extension PhotoPageViewController: UIPageViewControllerDataSource {
    
    func pageViewController(pageViewController: UIPageViewController,
        viewControllerBeforeViewController viewController: UIViewController) -> UIViewController? {
            guard let viewControllerIndex = orderedViewControllers.indexOf(viewController) else {
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
    
    func pageViewController(pageViewController: UIPageViewController,
        viewControllerAfterViewController viewController: UIViewController) -> UIViewController? {
            guard let viewControllerIndex = orderedViewControllers.indexOf(viewController) else {
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
