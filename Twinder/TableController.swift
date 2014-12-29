//
//  TableController.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/27/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation

import UIKit
import CoreData

class TableController:UIViewController, UITableViewDataSource, UITableViewDelegate {

    // MARK: IBOutlet
    // TableView inside ViewController
    @IBOutlet var tableView: UITableView!


    // Setup lazy managedObjectContext for corestorage
    lazy var managedObjectContext : NSManagedObjectContext? = {
        let appDelegate = UIApplication.sharedApplication().delegate as AppDelegate
        if let managedObjectContext = appDelegate.managedObjectContext {
            return managedObjectContext
        }
        else {
            return nil
        }
        }()

    // Hold array for favourite tweeps to display in table
    var fav_tweeps: [FavTweets] = []

    // send "apirequest" to core starge
    func apiRequest() -> [FavTweets]{

        // Get Entity "Fav tweets" see Store.xcdatamodelid
        let fetchRequest = NSFetchRequest(entityName: "FavTweets")

        // If we can find some favs return them
        if let fetchResults = managedObjectContext!.executeFetchRequest(fetchRequest, error: nil) as? [FavTweets] {
            return fetchResults
        }

        // Return empty if there are no results
        return []
    }


    override func viewDidLoad() {
        super.viewDidLoad()

        // get favourite tweeps
        fav_tweeps = self.apiRequest()

        // important setup delegate and datasource for hte table
        tableView.delegate = self
        tableView.dataSource = self

        // remove weird edges
        self.tableView.contentInset = UIEdgeInsetsMake(-35, 0, -35, 0);

    }

    // UITableViewDataSource Functions
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {

        // return the number of objects in fav_tweeps to setup the data source
        return fav_tweeps.count
    }

    func tableView(tableView: UITableView!, heightForHeaderInSection section: Int) -> CGFloat {

        // set the height of the header section to zero
        return 0.0
    }

    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {

        let indexPath = tableView.indexPathForSelectedRow();
        let currentCell = tableView.cellForRowAtIndexPath(indexPath!) as TweepCell;
        if let selected_tweep = self.fav_tweeps[indexPath!.item] as FavTweets! {

            // if the row is selected do a deep link to open the twitter app/website to find the given user.
            twtrScreenName(selected_tweep.screen_name)
        }
        
    }


    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell{

        // Tweep cell - see Views/TweepCell.swift
        let cell: TweepCell = tableView.dequeueReusableCellWithIdentifier("cell") as TweepCell

        // Set the margins of the cell to zero
        cell.layoutMargins = UIEdgeInsetsZero

        // Do not preserve the margins of the superview
        cell.preservesSuperviewLayoutMargins = false;

        // Set the cell background to b clear
        cell.backgroundColor = UIColor.clearColor()

        // Allow cell selecton
        cell.setSelected(true, animated:true)

        // Work through the fav_tweets based on their index e.g. FavTweets[0] - first fav
        if let fav_tweep = self.fav_tweeps[indexPath.item] as FavTweets! {

            // get the image from the cell (see Views/TweepCell.swift)
            let old = cell.peepImage

            // Create a new instance of picture (see Functions/Picture.swift)
            let pic = Picture()

            // Send HTTP request to get the image
            pic.get(NSURL(string: fav_tweep.image_url)!, {NewImage, error in

                // Setup variables for the new image
                let img: UIImage = NewImage
                let width = img.size.width;
                let height = img.size.height;
                let screenWidth = self.view.frame.size.width;
                let apect = width/height;
                let nHeight = screenWidth/apect;

                // Display the new image
                old.frame = CGRectMake(0, 0, screenWidth, nHeight);
                old.center = self.view.center;
                old.image = img;
            })

            // Don't allow the images to overflow the cell
            cell.clipsToBounds = true

            //  Append a header to the cell to show the tweep's name above the image.
            let screen_width = self.view.frame.size.width
            let headerView: UIView = UIView(frame: CGRectMake(0,0,screen_width,50))
            headerView.backgroundColor = toColor("000000")
            headerView.alpha = CGFloat(55)

            // Set the text for the header
            let headerText: UILabel = UILabel(frame: CGRectMake(10, 2, screen_width-10, 50))
            headerText.text = fav_tweep.name
            headerText.textColor = toColor("fefefe")
            headerView.addSubview(headerText)

            // Add the header view to the cell
            cell.addSubview(headerView)

            // Create a larger border to the bottom of the cell
            let headerBackgroundLabel: UILabel = UILabel(frame: CGRectMake(0,220,screen_width,20))
            headerBackgroundLabel.backgroundColor = toColor("5E41A3")
            cell.addSubview(headerBackgroundLabel)
        }
        return cell;
    }
}