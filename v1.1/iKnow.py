# -*- coding: utf8 -*-
import knowledge_manipulate as km
import random

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from Tkinter import *
import speech_recognition as sr
import uniout
import sys
import rauth
import time
import json
import urllib

class iKnowMainWindow(Frame):   # Main UI interacting with user
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.system_state = 1    # [variable] store the state of the system. Default is 1 (1st result)
        self.user_say = ""      # [variable] store what user said (from speech to text component)

        self.createWidgets()    # [function] Draw all components onto the window
        self.knowledgeInit()    # [function] Initialize all knowledge bases
 
    def createWidgets(self):
        self.inputText = Label(self)    # Draw input label and entrybox
        self.inputText["text"] = "Input:"
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=6)
 
        self.outputText = Label(self)   # Draw output label and entrybox
        self.outputText["text"] = "Output:"
        self.outputText.grid(row=2, column=0)
        self.outputField = Entry(self)
        self.outputField["width"] = 50
        self.outputField.grid(row=2, column=1, columnspan=6)
         
        self.theButton = Button(self)         # Draw the control button
        self.theButton["text"] = "Start"
        self.theButton.grid(row=4, column=3)
        self.theButton["command"] = self.pushButtonAndGetToWork

        self.displayText = Label(self)  # Draw the displaying label benethe the control button
        self.displayText["text"] = "iKnow: a Context-Aware Recommender System"
        self.displayText.grid(row=5, column=0, columnspan=7)
        return 0

    def knowledgeInit(self):
        print "Loading knowledge bases."
        self.shutdown_keyword = km.loadList("shutdown_keyword.txt")
        self.random_keyword = km.loadList("random_keyword.txt")
        return 0

    def pushButtonAndGetToWork(self):
        print ""
        print "push button!"
        self.inputField.delete(0, 'end')    # clear inputField
        self.outputField.delete(0, 'end')   # clear outputField

        self.user_say = getSpeechThenToTextDev()
        #self.user_say = getSpeechThenToText()       # Get speech and also do speech to text
        self.understanding()                        # Do natural language understanding
        self.readyForAction()                       # Ready for action
        return 0

    def understanding(self):
        if self.user_say == -1:
            self.system_state = 90

        else:
            self.user_say = self.user_say.decode("utf8")
            self.inputField.insert(0, self.user_say)    # Show what user say

            for shutdown_term in self.shutdown_keyword:   # Shut down detected
                if shutdown_term in self.user_say:
                    self.system_state = -1
                    return

            for random_term in self.random_keyword:
                if random_term in self.user_say:
                    self.system_state = 12
                    return

            self.system_state = 11   # Anyway, put to state 1-1 for testing

        return 0 

    def readyForAction(self):
        if self.system_state == -1:   # -1: shut down
            sys.exit()

        elif self.system_state == 11: # 11:
            self.resultOutput = getTag_Location(self.user_say)

            self.outputField.insert(0, self.resultOutput[0])
            self.displayText["text"] = self.resultOutput[1]

            #getLocation(self.user_say)
            #getTag(self.user_say)

            return 0

        elif self.system_state == 12: # 12:
            whatToEat()
            return 0

        elif self.system_state == 90:   # 90: speech input value error
            print u"語音辨識錯誤，請重新輸入！"
            return 0

        else:
            print u"異常狀況：請檢查 system_state 是否有遺漏"
            return -1


def getSpeechThenToTextDev(): # for silent testing while developing (kill this function when it's no use)
    #dev_test_utt = "請幫我找台大附近的義大利麵"  # normal test 
    dev_test_utt = "請幫我找一下台大後門附近的義大利麵"  # test loca_dict
    #dev_test_utt = "請幫我找一下台大附近的賣火鍋的"  # test 
    #dev_test_utt = "台大附近的義大利麵"  # test no location_front
    #dev_test_utt = "我想吃麵"  # test no location and category (use special term)
    #dev_test_utt = "我想吃牛肉麵"  # test no location and category (use special term)
    #dev_test_utt = "我想吃義大利麵"    # test no location
    #dev_test_utt = "這裏有沒有優格"    # test no location and loca/cate keyword conflict
    #dev_test_utt = "台大附近的咖哩店"  # test no front
    #dev_test_utt = "台大附近義大利麵"  # test no front
    #dev_test_utt = "我想吃迴轉壽司" # test no-use category
    #dev_test_utt = "台大附近的牛肉麵"    # test no category
    #dev_test_utt = "今天要吃什麼呢"   # test random
    #dev_test_utt = "台大附近奶凍捲"   # test no category and tag_front: CATASTROPHE
    print "測試：", dev_test_utt
    return dev_test_utt


def getSpeechThenToText():    # see https://pypi.python.org/pypi/SpeechRecognition/ for detail
    r = sr.Recognizer()
    m = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            #while True:
            print("Say something!")
            audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try: # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio, language = "zh-TW")

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes: # this version of Python uses bytes for strings (Python 2)
                    #print(u"You said {}".format(value).encode("big5"))  # encode big5 for show on Windows Console, 之後再處理
                    print( u"You said {}".format(value) )
                    c = value.encode("utf-8")
                    return c
                else: # this version of Python uses unicode for strings (Python 3+)
                    print( "You said {}".format(value) )
                    c = ""
                    return c
            except sr.UnknownValueError:    # value error (not a recogizable utterance)
                #print("Oops! Didn't catch that")
                return -1 # -1: speech input value error
            except sr.RequestError as e:    # service unavailable
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass


def whatToEat():    ### DANGER, THIS PART SHOULD BE REWRITED ###
    favorate_dictionary = km.loadList("favorate_dictionary.txt")

    fav_list = []
    for term in favorate_dictionary:
        fav_list += [term]

    print "不知道要吃什麼嗎？讓我來幫忙丟個飛鏢吧！！"
    time.sleep(1.0)
    print "登登！"
    time.sleep(1.0)

    print "===================="
    for i in range(5):
        choose_num = random.randint(0, len( fav_list )-1 )
        print fav_list[ choose_num ]
        fav_list.pop( choose_num )

    print "===================="

    return 0

def getTag_Location(sentence):
    tags = getTag(sentence) # tags[0]: category, [1]: term
    cate = ','.join( tags[0] )
    term = ','.join( tags[1] )
    geo = getLocation(sentence)

    param = getSearchParameters(cate, term)
    result_from_yelp = getYelpResult(geo[:-1], param)

    if len(result_from_yelp.businesses) == 0:
        print "查無資料，請再次嚐試."
        return "（回傳句）查無資料", "（回傳地址）查無資料"
    else: 
        outputRestaurant = []

        for index in range( len(result_from_yelp.businesses) ):
            print result_from_yelp.businesses[ index ].name
            print result_from_yelp.businesses[ index ].location.address
            print result_from_yelp.businesses[ index ].distance

        responseSentence = ( '最高分回傳：'.decode('utf-8') + result_from_yelp.businesses[0].name )
        address = result_from_yelp.businesses[0].location.address

        return responseSentence, address


def getTag(sentence_for_get_tag):
    category_dictionary = km.loadDictionary("categoryTW.txt")
    category_keyword_front = km.loadList("category_keyword_front.txt")
    special_terms = km.loadList("special_terms.txt")

    tag_front = 0
    search_sen = ""
    for term in category_keyword_front:   # find front keyword (maybe find nothing)
        if term in sentence_for_get_tag:
            front_candidate = int( sentence_for_get_tag.find(term) + len(term) )
            if tag_front < front_candidate:
                tag_front = front_candidate
                search_sen = sentence_for_get_tag[ sentence_for_get_tag.find(term)+1 : ]
    if tag_front == 0: search_sen = sentence_for_get_tag   # if find no front keywork, use original sentence

    find_category = [""]
    find_term = [""]
    for category in category_dictionary:    # find category
        for term in category_dictionary[ category ]:
            if term in search_sen:
                if len(find_term[0]) < len(term):   # once we found a longer term, replace the older ones
                    find_category = [ category ]
                    find_term = [ term ]
                elif len(find_term[0]) == len(term):     # same length term, check then join
                    find_category += [ category ]
                    if term not in find_term: find_term += [ term ]

    if len( find_term[0] ) == 0: # find no term, check special term ### DANGER, THIS PART SHOULD BE REWRITED ###
        for term in special_terms:
            if term in search_sen:
                if len(find_term[0]) < len(term):
                    find_term = [ term ]
                elif len(find_term[0]) == len(term):
                    if term not in find_term: find_term += [ term ]

    print "category: ", find_category
    print "term:     ", find_term

    if len(find_category[0]) == 0: return [ find_category, find_term, 0 ]   # find no category
    else: return [ find_category, find_term, 1 ]


def getLocation(sentence_for_get_location):  # here we use template sentence for getting location
    location_dictionary = km.loadDictionary("location_dictionary.txt")
    location_keyword_front = km.loadList("location_keyword_front.txt")
    location_keyword_back = km.loadList("location_keyword_back.txt")

    location_front = 0
    location_back = 0
    for term_front in location_keyword_front: # find front keyword (maybe find nothing)
        if term_front in sentence_for_get_location:
            front_candidate = int( sentence_for_get_location.find(term_front) + len(term_front) )
            if location_front < front_candidate: location_front = front_candidate
    for term_back in location_keyword_back:  # find back keyword (there must be one)
        if term_back in sentence_for_get_location:
            location_back = int( sentence_for_get_location.find(term_back) )

    location = sentence_for_get_location[ location_front:location_back ]

    if len(location) == 0:  # Return with Error: Can not find a location, use default location: "NTU backdoor"
        print "location: 未偵測到地點，預設為台大後門 25.0209219, 121.5403804"
        return [ 25.0209219, 121.5403804, 1 ]
    else:           # Return normally
        print "location: ", location
        for coordinates_candidate in location_dictionary:   # try to find the location in location_dict
            for term in location_dictionary[ coordinates_candidate ]:
                if location == term:
                    coordinates = [ float( coordinates_candidate.split(u',')[0] ),
                                    float( coordinates_candidate.split(u',')[1] ), ]
                    print "coordinates: ", coordinates
                    return coordinates + [0]

        coordinates = getGeocodeByGoogleMap( location.encode("utf8") ) # go GoogleMap for getting help
        print "coordinates: ", coordinates
        return coordinates + [0]  # go GoogleMap for getting help


def getGeocodeByGoogleMap(location_for_get_geocode):    # notice that it can only eat str format, do encode("utf8") pls
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    key = "&key=AIzaSyDU0SvmkoV9K_hm5xqDM39_-acX5HF7IW4"

    googleapi_loca = url + "台灣+" + location_for_get_geocode + key
    rf = urllib.urlopen(googleapi_loca)
    json_from_GoogleMap = json.loads(rf.read())
    coordinates = [ json_from_GoogleMap["results"][0]["geometry"]["location"]["lat"],
                    json_from_GoogleMap["results"][0]["geometry"]["location"]["lng"] ]

    print 'Get GeoCode by Google Map! ' + str(coordinates[0]) + ' ' + str(coordinates[1])
    return coordinates


def getYelpResult(coordinates, params): # obtain these from Yelp's manage access page
    auth = Oauth1Authenticator(
        consumer_key = "zL6GUBjcMjK8xFsGhmirmg",
        consumer_secret = "LGix0hLov03PZ7z16svTs1dnMdc",
        token = "7xp93HFfj9gPddJud46SoFEphYObk9Oe",
        token_secret = "2U1XaBB3L8BRl4cbT1Ur9_h4bXM")
    
    client = Client(auth)

    return client.search_by_coordinates(coordinates[0], coordinates[1], **params)


def getSearchParameters(inCate, inTerm):   # see the Yelp API for more details
    params = {}
    params["term"] = inTerm.encode("utf8")
    params["limit"] = 5
    #params["offset"] = 100
    params["sort"] = 1
    params["category_filter"] = inCate.encode("utf8")
    params["radius_filter"] = 1000
    #params["actionlinks"] = True

    params["cc"] = "TW"

    return params


if __name__ == '__main__':
    print ""
    root = Tk()
    iKnow_Tk = iKnowMainWindow(master=root)
    iKnow_Tk.mainloop()
