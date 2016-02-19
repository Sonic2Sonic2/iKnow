# -*- coding: utf-8 -*-
import urllib
import json


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

    #return f.read()

def GetDataFromFile(Name):
    f = open('code.txt', 'r')
    text = f.read()
    #print text
    return text

if __name__=="__main__":
    print GetGeocode("交大")
    #print GetDataFromFile("code.txt")
    #d = json.dumps(GetDataFromFile("code.txt"))

    #items2 = json.loads(GetDataFromFile("code.txt"))
    #for name_item in items2["results"]:
    #name_item = items2["results"][0]
    #print name_item["geometry"]["location"]["lat"]
    #print name_item["geometry"]["location"]["lng"]
        
#f1 = open('code.txt', 'w')

#params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
#f = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=台灣台大&key=AIzaSyDU0SvmkoV9K_hm5xqDM39_-acX5HF7IW4")

#f1.write(f.read())
#f1.close()
#print f.read()