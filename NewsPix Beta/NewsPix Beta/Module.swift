//
//  Module.swift
//  NewsPix Beta
//
//  Created by UROP on 3/29/16.
//  Copyright © 2016 UROP. All rights reserved.
//

import Foundation
import UIKit

//Carousel Lists
public var index: Int = 0
//Bank of images
public var images: [UIImage!] = []
//Bank of headlines
public var names: [String] = []
//Bank of URLs
public var urls: [NSURL] = []

//Initial view frame from main viewController
public var initial_frame: CGRect = CGRectZero

//Functions for obtaining, parsing JSONs

func getData(urlToRequest: String) -> NSData? {
    //Retrieves NSData from a url
    if let url = NSURL(string: urlToRequest) {
        if let data = NSData(contentsOfURL: url) {
            return data
        }
    }
    return nil
}

func parseJSON(inputData: NSData) {
    //Parse the JSON - in this case, the JSON is a dictionary.
    var json: NSDictionary = [:]
    //The actual parsing must be done with try/catch because it can fail
    do {
        json = try NSJSONSerialization.JSONObjectWithData(inputData, options: NSJSONReadingOptions()) as! NSDictionary
    } catch {
        print(error)
    }
    //Update the carousel lists
    let jsonHeadline: String! = json["headline"] as! String
    let jsonURL: String! = json["url"] as! String
    let jsonImage: String! = json["image"] as! String
    
    images.append(UIImage(data:(getData(jsonImage))!))
    names.append(jsonHeadline)
    urls.append(NSURL(string: jsonURL)!)

}

func altParseJSON(inputData: NSData) {
    //Parse the JSON
    var json: NSMutableArray = []
    //The actual parsing must be done with try/catch because it can fail
    do {
        json = try NSJSONSerialization.JSONObjectWithData(inputData, options: NSJSONReadingOptions()) as! NSMutableArray
    } catch {
        print(error)
    }
    //Update the carousel lists
    for story in json {
        let jsonHeadline: String! = story["headline"] as! String
        let jsonURL: String! = story["url"] as! String
        let jsonImage: String! = story["image"] as! String
    
        images.append(UIImage(data:(getData(jsonImage))!))
        names.append(jsonHeadline)
        urls.append(NSURL(string: jsonURL)!)
    }
    
}

//Method for managing aspect fit image sizes
func imageSizeAfterAspectFit(imgview: UIImageView) -> CGSize {
    
    var newwidth: CGFloat
    var newheight: CGFloat
    let image: UIImage = imgview.image!
    
    if (image.size.height >= image.size.width) {
        newheight = initial_frame.height
        newwidth = (image.size.width/image.size.height) * newheight;
        
        if (newwidth > initial_frame.width){
            let diff: CGFloat = initial_frame.width - newwidth
            newheight = newheight + diff/newheight * newheight
            newwidth = initial_frame.width
        }
    }
    else {
        newwidth = initial_frame.width;
        newheight = (image.size.height/image.size.width) * newwidth
        
        if (newheight > initial_frame.height) {
            let diff: CGFloat = initial_frame.height - newheight
            newwidth = newwidth + diff/newwidth * newwidth
            newheight = initial_frame.height
        }
    }
    
//    //adapt UIImageView size to image size
//    imgview.frame = CGRectMake(imgview.frame.origin.x + (imgview.frame.size.width-newwidth)/2, imgview.frame.origin.y + (imgview.frame.size.height-newheight)/2, newwidth, newheight)
    
    return CGSizeMake(newwidth, newheight);
}