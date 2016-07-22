//
//  ViewController.swift
//  NewsPix Beta
//
//  Created by UROP on 3/12/16.
//  Copyright © 2016 UROP. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UIScrollViewDelegate {
    
    @IBOutlet var swipeRight: UISwipeGestureRecognizer!
    @IBOutlet var swipeLeft: UISwipeGestureRecognizer!
    @IBOutlet weak var scrollView: UIScrollView!
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var pictureTitle: UIButton!
    
    
    @IBOutlet weak var imageViewHeight: NSLayoutConstraint!
    @IBOutlet weak var imageViewBottomConstraint: NSLayoutConstraint!
    @IBOutlet weak var imageViewLeadingConstraint: NSLayoutConstraint!
    @IBOutlet weak var imageViewTopConstraint: NSLayoutConstraint!
    @IBOutlet weak var imageViewTrailingConstraint: NSLayoutConstraint!
    
    //Sets status bar to white
    override func preferredStatusBarStyle() -> UIStatusBarStyle {
        return UIStatusBarStyle.LightContent
    }

    var lastZoomScale: CGFloat = -1
    
    override func viewDidLoad() {
        super.viewDidLoad()
        initial_frame = view.frame
        
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

        //Initialize Display
        self.pictureTitle.setTitle(names[index],forState: UIControlState.Normal)
        self.imageView.image = images[index]
        
        //Always make pictureTitle fit in one line
        self.pictureTitle.titleLabel?.adjustsFontSizeToFitWidth = true
        
    }
    
    override func viewWillAppear(animated: Bool) {
        navigationItem.title = "Sentinel Source"
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        
        //scrollView Initialization settings
        scrollView.delegate = self
        updateZoom()
        updateConstraints()
        scrollView.decelerationRate = UIScrollViewDecelerationRateFast
    }
    
    @IBAction func didPressTitle() {
        let url = urls[index];
        UIApplication.sharedApplication().openURL(url);
    }
    
    @IBAction func handleSwipe(recognizer:UISwipeGestureRecognizer) {
        if (recognizer.direction == UISwipeGestureRecognizerDirection.Right) {
            index -= 1
            if index < 0 {index = names.count-1}
        }
        if (recognizer.direction == UISwipeGestureRecognizerDirection.Left) {
            index += 1
            if index > names.count-1 {index = 0}
        }
        
        self.imageView.fadeOut()
        self.pictureTitle.fadeOut()
        
        //Transitionary code
        self.imageView.image = images[index]
        self.pictureTitle.setTitle(names[index],forState: UIControlState.Normal)
        scrollView.zoomScale = 1.0

        self.pictureTitle.fadeIn()
        self.imageView.fadeIn()
    }

    @IBAction func shareButtonClicked(sender: UIBarButtonItem) {
        let textToShare = self.pictureTitle.currentTitle!
        let myWebsite = urls[index]
        let objectsToShare = [textToShare, myWebsite]
        let activityVC = UIActivityViewController(activityItems: objectsToShare, applicationActivities: nil)
        
        activityVC.excludedActivityTypes = [UIActivityTypePostToWeibo,
            UIActivityTypeMessage,
            UIActivityTypeMail,
            UIActivityTypePrint,
            UIActivityTypeCopyToPasteboard,
            UIActivityTypeAssignToContact,
            UIActivityTypeSaveToCameraRoll,
            UIActivityTypeAddToReadingList,
            UIActivityTypePostToFlickr,
            UIActivityTypePostToVimeo,
            UIActivityTypePostToTencentWeibo,
            UIActivityTypeAirDrop]
        
        self.presentViewController(activityVC, animated: true, completion: nil)
        }
    
    override func viewWillTransitionToSize(size: CGSize,
        withTransitionCoordinator coordinator: UIViewControllerTransitionCoordinator) {
            
            super.viewWillTransitionToSize(size, withTransitionCoordinator: coordinator)
            
            coordinator.animateAlongsideTransition({ [weak self] _ in
                self?.updateZoom()
                }, completion: nil)
    }
    
    func updateConstraints() {
        if let _ = imageView.image {
            
            let imageWidth = imageSizeAfterAspectFit(imageView).width
            let imageHeight = imageSizeAfterAspectFit(imageView).height
            
            let viewWidth = scrollView.bounds.size.width
            let viewHeight = scrollView.bounds.size.height
            
            // center image if it is smaller than the scroll view
            var hPadding = (viewWidth - scrollView.zoomScale * imageWidth) / 2
            if hPadding < 0 { hPadding = 0 }
            
            var vPadding = (viewHeight - scrollView.zoomScale * imageHeight) / 2
            if vPadding < 0 { vPadding = 0 }
            
            imageViewTrailingConstraint.constant = hPadding
            imageViewLeadingConstraint.constant = hPadding
            
            imageViewTopConstraint.constant = vPadding
            imageViewBottomConstraint.constant = vPadding
            
            imageViewHeight.constant = imageSizeAfterAspectFit(imageView).height
            
            view.layoutIfNeeded()
            
            //Disable scrolling if image is fully zoomed out
            if scrollView.zoomScale == 1.0 {
                scrollView.scrollEnabled = false
            }
            else {
                scrollView.scrollEnabled = true
            }
        }
        
    }
    
    // Zoom to show as much image as possible unless image is smaller than the scroll view
    // **Called only upon view initialization and upon device rotation**
    private func updateZoom() {
        if let image = imageView.image {
            var minZoom = min(scrollView.bounds.size.width / image.size.width,
                scrollView.bounds.size.height / image.size.height)

            if minZoom > 1 { minZoom = 1 }
            
            scrollView.minimumZoomScale = 1
            scrollView.maximumZoomScale = 8

            // Force scrollViewDidZoom fire if zoom did not change
            if minZoom == lastZoomScale { minZoom += 0.000001 }
            scrollView.zoomScale = minZoom
            lastZoomScale = scrollView.zoomScale
            
        }
    }
    
    // UIScrollViewDelegate
    // -----------------------
    
    func scrollViewDidZoom(scrollView: UIScrollView) {
        updateConstraints()
    }
    
    func viewForZoomingInScrollView(scrollView: UIScrollView) -> UIView? {
        return imageView
        }
    
} //Do not delete! End of ViewController class
