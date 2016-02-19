# -*- coding: utf-8 -*-
import rauth
import time
import json
import urllib

def main():
    locations = GetGeocode("交大")
    api_calls = []  
    params = get_search_parameters(locations[0], locations[1])
    api_calls.append(get_results(params))
    d = json.dumps(api_calls)
    #Be a good internet citizen and rate-limit yourself
    time.sleep(1.0)
    items = json.loads(d)
    ##Do other processing

    for name_item in items:
        for name2 in name_item["businesses"]:
            print name2["name"]


def GetGeocode(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    key = "&key=AIzaSyDU0SvmkoV9K_hm5xqDM39_-acX5HF7IW4"
    location = "台灣" + location
    googleapi_loca = url+location+key
    f = urllib.urlopen(googleapi_loca)
    items2 = json.loads(f.read())
    name_item = items2["results"][0]
    k =[]
    k.append(name_item["geometry"]["location"]["lat"])
    k.append(name_item["geometry"]["location"]["lng"])
    return k

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
    params["term"] = "restaurant+chinese"
    params["ll"] = "{},{}".format(str(lat),str(long))
    params["radius_filter"] = "3000"
    params["limit"] = "5"

    return params


if __name__=="__main__":
    main()