//
//  API.swift
//  Twinder
//
//  Created by Gareth Jones  on 12/26/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import Foundation
import Foundation
import TwitterKit

class APIClient {

    class func fetchTweeps(tweepHandler: (Array<Tweep>) -> ()) -> Void {

        // Fetch those tweeps
        self.Search() { (result: Array<Tweep>) in
            let new_result = shuffle(result)

            // Used for demo purposes
            //var new_result = Array<Tweep>()
            //new_result.append(Tweep(name: "Justin Beiber", image: "https://pbs.twimg.com/profile_images/520374943272284160/FzNKwxes_400x400.jpeg", screen_name: "justinbeiber"))
            //new_result.append(Tweep(name: "Barack Obama", image: "https://pbs.twimg.com/profile_images/451007105391022080/iu1f7brY_400x400.png", screen_name: "barackobama"))
            tweepHandler(new_result)
        }

    }

    func getTweet(screen_name: String, completion: (result: String) -> Void){

        // setup some type aliases to handle regular wording for JSON type objects
        typealias JSON = AnyObject
        typealias JSONDictionary = Dictionary<String, JSON>
        typealias JSONArray = Array<JSON>

        // set an endpoint you can check out the docs via:
        // https://dev.twitter.com/rest/reference/get/search/tweets
        let RESTAPIEndpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"

        // setup the params for the request

        let params = ["count": "2", "screen_name": screen_name]

        // setup container for an error
        var clientError : NSError?


        let request = Twitter.sharedInstance().APIClient.URLRequestWithMethod("GET", URL:  RESTAPIEndpoint, parameters: params, error:&clientError)

        // if the request is ready to rock and roll
        if request != nil {
                  
            // let's send us a REST API reuest
            Twitter.sharedInstance().APIClient.sendTwitterRequest(request) {
                (response, data, connectionError) -> Void in

                if (connectionError == nil) {

                    // Setup a tweet array to contain all of those juicy tweets
                    var jsonError : NSError?
                    let json : AnyObject? =
                    NSJSONSerialization.JSONObjectWithData(data,
                        options: nil,
                        error: &jsonError)

                    if let tweets = json! as? JSONArray {
                        let tweet = tweets[0]["id_str"] as String!
                        println(tweet)
                        completion(result: tweet)
                    }

                }
            }
        }
    }

    class func Search(completion: (result: Array<Tweep>) -> Void) {
        
        // setup some type aliases to handle regular wording for JSON type objects
        typealias JSON = AnyObject
        typealias JSONDictionary = Dictionary<String, JSON>
        typealias JSONArray = Array<JSON>

        // set an endpoint you can check out the docs via:
        // https://dev.twitter.com/rest/reference/get/search/tweets
        let RESTAPIEndpoint = "https://api.twitter.com/1.1/friends/list.json"

        // setup the params for the request
        let screen_name = Twitter.sharedInstance().session().userName
        println(screen_name)
        let params = ["count": "200", "include_user_entities": "true", "screen_name": screen_name]

        // setup container for an error
        var clientError : NSError?

        // Initialize Twitter
        Twitter.initialize()

        // Send a REQUEST to Twitter using GuestAuthentication e.g. no authenticated user just the app.
        Twitter.sharedInstance().logInWithCompletion{
            (session, error) -> Void in
            if (session != nil) {

                // woohoo we have a session - let's get crazy
                let request = Twitter.sharedInstance().APIClient.URLRequestWithMethod("GET", URL:  RESTAPIEndpoint, parameters: params, error:&clientError)

                // if the request is ready to rock and roll
                if request != nil {

                    // let's send us a REST API reuest
                    Twitter.sharedInstance().APIClient.sendTwitterRequest(request) {
                        (response, data, connectionError) -> Void in
                        if (connectionError == nil) {

                            // Setup a tweet array to contain all of those juicy tweets
                            var jsonError : NSError?
                            let json : AnyObject? =
                            NSJSONSerialization.JSONObjectWithData(data,
                                options: nil,
                                error: &jsonError)

                            var tweetArray = Array<Tweep>()

                            // Iterate through JSON response and append the values to the TweetArray
                            if let tweeps = json!["users"] as? JSONArray {
                                for tweep in tweeps {
                                    let screen_name = tweep["screen_name"] as String!
                                    let name = tweep["name"] as String!
                                    let image = tweep["profile_image_url"] as String!
                                    let highimage = image.stringByReplacingOccurrencesOfString("_normal", withString: "", options: NSStringCompareOptions.LiteralSearch, range: nil)
                                        //println(image)
                                    tweetArray.append(Tweep(name: name, image: highimage, screen_name: screen_name))
                                }

                            }
                            completion(result: tweetArray)
                        }
                            
                            
                            
                        else {
                            println("Error: \(connectionError)")
                        }
                    }
                }
                else {
                    println("Error: \(clientError)")
                }
                
            } else {
                println("error: \(error.localizedDescription)");
            }
            
        }
    }
}