//
//  UIViewExtensions.swift
//  NewsPix Beta
//
//  Created by UROP on 4/13/16.
//  Copyright © 2016 UROP. All rights reserved.
//

//Sourced from https://www.andrewcbancroft.com/2014/07/27/fade-in-out-animations-as-class-extensions-with-swift/
import Foundation
import UIKit
    
extension UIView {
        func fadeIn(duration: NSTimeInterval = 0.5, delay: NSTimeInterval = 0.0, completion: ((Bool) -> Void) = {(finished: Bool) -> Void in}) {
            UIView.animateWithDuration(duration, delay: delay, options: UIViewAnimationOptions.CurveEaseIn, animations: {
                self.alpha = 1.0
                }, completion: completion)  }
        
        func fadeOut(duration: NSTimeInterval = 1.0, delay: NSTimeInterval = 0.0, completion: (Bool) -> Void = {(finished: Bool) -> Void in}) {
            UIView.animateWithDuration(duration, delay: delay, options: UIViewAnimationOptions.CurveEaseIn, animations: {
                self.alpha = 0.0
                }, completion: completion)
        }
}