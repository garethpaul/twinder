//
//  TweepPickerViewController.swift
//

import UIKit
import Foundation
import CoreData

class TweepPickerViewController: UIViewController, MDCSwipeToChooseDelegate {

    // Set the button details
    let buttonDiameter: CGFloat = 80
    let buttonHPadding: CGFloat = 70

    // Setup variables.
    var tweeps: Array<Tweep> = Array()
    var topCardView: UIView = UIView()
    var bottomCardView: UIView = UIView()
    var savedTweeps: Array<Tweep> = Array()
    var lView: UIImageView!


    // Mark IBActions/Outlets
    @IBAction func moveToTable(sender: AnyObject) {

    }
    @IBOutlet var peepButtonItem: UIBarButtonItem!


    // Setup a lazy managedObjectContext for storage using CoreData see Store.xcdatamodelId
    lazy var managedObjectContext : NSManagedObjectContext? = {
        let appDelegate = UIApplication.sharedApplication().delegate as AppDelegate
        if let managedObjectContext = appDelegate.managedObjectContext {
            return managedObjectContext
        }
        else {
            return nil
        }
        }()


    override func viewDidLoad() {
        super.viewDidLoad()

        // Setup the logo to display on the navibation controller
        lView = UIImageView(frame: CGRectMake(0, 0, 75, 23))
        lView.image = UIImage(named: "twinder")?.imageWithRenderingMode(.AlwaysTemplate)
        lView.tintColor = toColor("#FEFEFE")
        lView.frame.origin.x = (self.view.frame.size.width - lView.frame.size.width) / 2
        lView.frame.origin.y = -lView.frame.size.height - 1
        self.navigationController?.view.addSubview(lView)
        self.navigationController?.view.bringSubviewToFront(lView)

        // Customize the navigation bar.
        let titleDict: NSDictionary = [NSForegroundColorAttributeName: toColor("5E41A3")]
        self.navigationController?.navigationBar.titleTextAttributes = titleDict
        self.navigationController?.navigationBar.shadowImage = UIImage()
        self.navigationController?.navigationBar.topItem?.title = ""
        self.navigationController?.navigationBar.barTintColor = toColor("5E41A3")
        self.navigationItem.setHidesBackButton(true, animated:true);
        self.navigationController?.navigationItem.setHidesBackButton(
            true, animated: true)


        // Fetch some tweets/tweeps
        APIClient.fetchTweeps({(fetchedTweeps: Array<Tweep>) -> Void in

            // store the tweeps in an array
            self.tweeps = fetchedTweeps

            // Setup initial card views
            self.topCardView = self.createTweepView(self.topCardViewFrame(), tweep: self.tweeps.removeAtIndex(0))

            // Append the card to the view
            self.view.addSubview(self.topCardView)

            // Append the "bottom" card under the top card
            self.bottomCardView = self.createTweepView(self.bottomCardViewFrame(), tweep: self.tweeps.removeAtIndex(0))
            self.view.insertSubview(self.bottomCardView, belowSubview: self.topCardView)

            // constructors see functions below...
            self.constructBackground()
            self.constructNopeButton()
            self.constructLikeButton()
        })

    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)

        // Animate the logo when the view appears.
        UIView.animateWithDuration(0.6, delay: 0, usingSpringWithDamping: 0.5, initialSpringVelocity: 0.8, options: .CurveEaseInOut, animations: { () -> Void in
            // Place the frame at the correct origin position.
            self.lView.frame.origin.y = 33
            }, completion: nil)
    }


    func saveTweep(tweep: Tweep) -> Void {

        // Once you swipe to like a tweep store the data in corestorage
        let newTweet = NSEntityDescription.insertNewObjectForEntityForName("FavTweets", inManagedObjectContext: self.managedObjectContext!) as FavTweets

        // Save the variables into corestorage see Modes/FavTweets.swift for details
        newTweet.screen_name = tweep.screen_name
        newTweet.image_url = tweep.image
        newTweet.name = tweep.name

        // Store the saved tweep into an array
        self.savedTweeps.append(tweep)
    }

    func skipTweep(tweep: Tweep) -> Void {
        println("skipping")
    }

    func view(view: UIView!, wasChosenWithDirection direction: MDCSwipeDirection) {

        // If there is a swipe perform an action on direction
        let tpv = view as TweepPickerView
        if (direction == MDCSwipeDirection.Right) {
            if(tpv.tweep != nil) {
                saveTweep(tpv.tweep!)
            }
            println("Tweep saved!")
        } else {

            // User must have swiped left :-)
            if(tpv.tweep != nil) {
                skipTweep(tpv.tweep!)
            }
            println("Tweep skipped!")
        }

        // Switch the topCard with the bottomCard
        topCardView = bottomCardView

        // See if we have some tweeps to show.
        if(self.tweeps.count > 0) {

            // Create a new bottom card view
            bottomCardView = createTweepView(bottomCardViewFrame(), tweep: self.tweeps.removeAtIndex(0))
            bottomCardView.alpha = 0.0

            // Insert a new bottomCard
            self.view.insertSubview(bottomCardView, belowSubview: topCardView)

            // Animate the bottom card in
            UIView.animateWithDuration(
                0.5,
                delay: 0.0,
                options: UIViewAnimationOptions.CurveEaseInOut,
                animations: {
                    self.bottomCardView.alpha = 1
                },
                completion: nil
            )
        } else {
            // Bottomcard is empty
            bottomCardView = UIView()
        }
    }

    // Setup the frame for the topCard
    func topCardViewFrame() -> CGRect {
        let hPadding: CGFloat = 40
        let topPadding:CGFloat = 80
        let bottomPadding:CGFloat = 270

        return CGRectMake(
            hPadding,
            topPadding,
            CGRectGetWidth(self.view.frame) - (hPadding * 2),
            CGRectGetHeight(self.view.frame) - bottomPadding
        )
    }

    // Setup the frame for the bottomCard
    func bottomCardViewFrame() -> CGRect {
        let topFrame: CGRect = topCardViewFrame()

        return CGRectMake(
            topFrame.origin.x,
            topFrame.origin.y + 10,
            CGRectGetWidth(topFrame),
            CGRectGetHeight(topFrame)
        )
    }

    // Construct ButtonY
    func buttonY() -> CGFloat {
        return CGRectGetMaxY(self.bottomCardView.frame) +
            ((CGRectGetHeight(self.view.bounds) - CGRectGetMaxY(self.bottomCardView.frame) - buttonDiameter) / 2)
    }

    // Construct a nope/dislike button
    func constructNopeButton() {
        let frame: CGRect = CGRectMake(
            buttonHPadding,
            buttonY(),
            buttonDiameter,
            buttonDiameter
        )

        // Setup the button to display "no"
        let button: UIButton = UIButton.buttonWithType(UIButtonType.System) as UIButton
        button.frame = frame
        button.setImage(UIImage(named: "dislike"), forState: UIControlState.Normal)
        button.tintColor = toColor("F00A3F")
        button.addTarget(self, action: "nopeTopCardView", forControlEvents: UIControlEvents.TouchUpInside)

        // Add the button to the view
        self.view.insertSubview(button, atIndex: 0)
    }

    func constructLikeButton() {
        let frame: CGRect = CGRectMake(
            CGRectGetWidth(self.view.bounds) - buttonDiameter - buttonHPadding,
            buttonY(),
            buttonDiameter,
            buttonDiameter
        )

        // Setup the button to display "yes"
        let button: UIButton = UIButton.buttonWithType(UIButtonType.System) as UIButton
        button.frame = frame
        button.setImage(UIImage(named: "like"), forState: UIControlState.Normal)
        button.tintColor = toColor("15B374")
        button.addTarget(self, action: "likeTopCardView", forControlEvents: UIControlEvents.TouchUpInside)

        // Add the button to the view
        self.view.insertSubview(button, atIndex: 0)
    }

    func nopeTopCardView() {
        self.topCardView.mdc_swipe(MDCSwipeDirection.Left)
    }

    func likeTopCardView() {
        self.topCardView.mdc_swipe(MDCSwipeDirection.Right)
    }

    // Setup background if there are no tweeps to show this is important
    func constructBackground() {
        let frownView: UIImageView = UIImageView(image: UIImage(named: "frown"))
        frownView.contentMode = UIViewContentMode.Center
        frownView.alpha = 0.5
        frownView.frame = CGRectMake(
            CGRectGetMinX(bottomCardView.frame),
            CGRectGetMinY(bottomCardView.frame),
            CGRectGetWidth(bottomCardView.frame),
            CGRectGetWidth(bottomCardView.frame)
        )

        let noMoreLabel: UILabel = UILabel(frame: CGRectMake(
            CGRectGetMinX(frownView.frame),
            CGRectGetMaxY(frownView.frame),
            CGRectGetWidth(frownView.frame),
            18
            ))
        noMoreLabel.font = UIFont.systemFontOfSize(20)
        noMoreLabel.alpha = 0.5
        noMoreLabel.text = "No more tweeps"
        noMoreLabel.textAlignment = NSTextAlignment.Center

        self.view.insertSubview(frownView, atIndex: 0)
        self.view.insertSubview(noMoreLabel, atIndex: 0)
    }

    // Setup TweepView with options
    func createTweepView(frame: CGRect, tweep: Tweep) -> TweepPickerView {
        var options: MDCSwipeToChooseViewOptions = MDCSwipeToChooseViewOptions()
        options.delegate = self
        options.likedText = "YES"
        options.likedColor = toColor("15B374")
        options.nopeText = "NO"
        options.nopeColor = toColor("F00A3F")

        options.onPan = {(state: MDCPanState!) -> Void in
            let frame: CGRect = self.bottomCardViewFrame()
            self.bottomCardView.frame = CGRectMake(
                frame.origin.x,
                frame.origin.y - (state.thresholdRatio * 10.0),
                CGRectGetWidth(frame),
                CGRectGetHeight(frame)
            )
        };

        var tpw: TweepPickerView = TweepPickerView(frame: frame, tweep: tweep, options: options)

        return tpw
    }

}
