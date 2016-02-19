# -*- coding: utf-8 -*-
import rauth
import time
import json

def main():
    locations = [(39.98,-82.98),(42.24,-83.61),(41.33,-89.13)]
    api_calls = []
    for lat,long in locations:
        params = get_search_parameters(lat,long)
        api_calls.append(get_results(params))
        #Be a good internet citizen and rate-limit yourself
        time.sleep(1.0)

    ##Do other processing

    for key in api_calls:
        print key

def main2():
    api_calls = []
    params = get_search_parameters_L()
    api_calls.append(get_results(params))
    d = json.dumps(api_calls)
    #item = json.load(api_calls)
    #Be a good internet citizen and rate-limit yourself
    time.sleep(1.0)
    items = json.loads(d)
    ##Do other processing

    for name_item in items:
    	for name2 in name_item["businesses"]:
    	    print name2["name"]

    #for key in api_calls:
        #print key
    #    for name_item in key:
    #        print name_item


def get_results(params):

    #Obtain these from Yelp's manage access page
    consumer_key = "zL6GUBjcMjK8xFsGhmirmg"
    consumer_secret = "LGix0hLov03PZ7z16svTs1dnMdc"
    token = "7xp93HFfj9gPddJud46SoFEphYObk9Oe"
    token_secret = "2U1XaBB3L8BRl4cbT1Ur9_h4bXM"

    session = rauth.OAuth1Session(
        consumer_key = consumer_key
        ,consumer_secret = consumer_secret
        ,access_token = token
        ,access_token_secret = token_secret)

    request = session.get("http://api.yelp.com/v2/search",params=params)

    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()

    return data

def get_search_parameters(lat,long):
    #See the Yelp API for more details
    params = {}
    params["term"] = "german"
    params["ll"] = "{},{}".format(str(lat),str(long))
    params["radius_filter"] = "300"
    params["limit"] = "5"


    return params

def get_search_parameters_L():
    #See the Yelp API for more details
    params = {}
    params["term"] = "餐廳"
    #params["ll"] = "{},{}".format(str(lat),str(long))
    params["location"] = "羅斯福路"
    params["radius_filter"] = "300"
    params["limit"] = "10"
    #params["offset"] = "2"

    return params

if __name__=="__main__":
    main()