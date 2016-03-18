# -*- coding: utf8 -*-
import knowledge_manipulate as km

from Tkinter import *
import speech_recognition as sr
import jieba.posseg as pseg
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
        self.randomkeyword = km.loadList("random_keyword.txt")
        return 0

    def pushButtonAndGetToWork(self):
        print "push button!"
        self.inputField.delete(0, 'end')    # clear inputField
        self.outputField.delete(0, 'end')   # clear outputField

        self.user_say = getSpeechThenToTextDev()    # Get speech and also do speech to text
        self.understanding()                        # Do natural language understanding
        self.readyForAction()                       # Ready for action
        return 0

    def understanding(self):
        self.inputField.insert(0, self.user_say)    # Show what user say

        for shutdown_term in self.shutdown_keyword:   # Shut down detected
            if shutdown_term in self.user_say:
                system_state = -1
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
            pass
            return 0

        else:
            print u"異常狀況：請檢查 system_state 是否有遺漏"
            return -1


def getSpeechThenToTextDev(): # for silent testing while developing (kill this function when it's no use)
    dev_test_utt = u"開發測試：請幫我找台大附近的義大利麵"
    #dev_test_utt = u"開發測試：請幫我找台大附近的義大利麵"  # normal test 
    #dev_test_utt = u"開發測試：請幫我找一下台大後門附近的義大利麵"  # test loca_dict
    #dev_test_utt = u"開發測試：台大附近的義大利麵"  # test no location_front
    #dev_test_utt = u"開發測試：我想吃義大利麵"    # test no location
    #dev_test_utt = u"開發測試：台大附近的咖哩店"  # test no front
    #dev_test_utt = u"開發測試：台大附近義大利麵"  # test no front
    #dev_test_utt = u"開發測試：我想吃迴轉壽司" # test a no-use category
    #dev_test_utt = u"開發測試：台大附近奶凍捲"   # test no category and tag_front: CATASTROPHE
    print dev_test_utt
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
                print("Oops! Didn't catch that")
            except sr.RequestError as e:    # service unavailable
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass

def getTag_Location(sentence):
    #tags = {}   # tags is a dictionary for storing tag
    #infile = open('yelp_tags_data.txt', 'r')    # input
    #for line in infile: # read
        #if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue # if # or nothing --> skip
        #linearr = line.strip('\n').strip('\r\n').split(':') # split tag and synonyms by ':'
        #linearr[1] = linearr[1].split(',')  # the synonyms are split into a list by ','
        #if linearr[1][0] == '': linearr[1] = [] # if the there is nothing bu '' in the synonym list, replace it by a null list
        #tags.update({linearr[0]:linearr[1]})    # add an object into tags dictionary: key = tag, and value = the synonym list
    #infile.close()

    #position_detected_keywords_front = []   # a list for storing front keywords
    #position_detected_keywords_back = []    # a list for storing back keywords
    #infile = open('position_detected_keywords.txt', 'r')
    #while 1:
        #line = infile.readline()
        #if line[0] == '#' or not line: break    # change to back
        #position_detected_keywords_front.append(line.strip('\n').strip('\r\n'))
    #while 1:
        #line = infile.readline()
        #if not line: break
        #position_detected_keywords_back.append(line.strip('\n').strip('\r\n'))
    #infile.close()
# 
    #position_keywords = {} #location dictionary, seems not work
    #infile = open('taipeiLocationDict.txt', 'r')
    #for line in infile:
        #if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue
        #linearr = line.strip('\n').strip('\r\n').split(':')
        #linearr[1] = linearr[1].split(',')
        #if linearr[1][0] == '': linearr[1] = []
        #position_keywords.update({linearr[0]:linearr[1]})
    #infile.close()
#
    #collected_tags = []
#
    ## find yelp tag in sentence
    #denyDict = {}   # I'm going to remove this one
    #for tag, keywords in categoryDict.items():
        #for keyword in keywords:
            #if keyword in sentence: # get only the first one keyword
                #keyword_pos = sentence.index(keyword)
                ## if chinese 'no' in sentence no far before the keyword
                #if u'不' in sentence[keyword_pos-9:keyword_pos]:
                    #denyDict[tag] = 1.0
                    #print (u'Detect 不 + ' + keyword).decode('utf8')
                #else:
                    #collected_tags.append(tag)
                #break
#
    #print u"getTag_Location 檢查點 ", collected_tags
#    
#
    ## find position base on keyword (but it directly do patteren matching to original sentence, dangerous)
    #position = ''
    ##for p, keywords in position_keywords.items():
        ##for keyword in keywords:
            ##if keyword in sentence:
                ##position = p
                ##break
    #if position == '':
        ## find position in sentence. detect keyword, and posseg sentence before the keyword, using nearest n or ns as position
        #for keyword in position_detected_keywords_front:
            #if keyword in sentence:
                #sub_sentence = sentence[:sentence.index(keyword)]
                #words = pseg.cut(sub_sentence)
                #for word, tag in list(reversed(list(words))):
                    #word = word.encode('utf8')
                    #tag = tag.encode('utf8')    # the word tag given from jieba
                    #print word.decode('utf-8'), tag.decode('utf-8')
                    #if tag != 'n' and tag != 'ns' and tag != 'a' and tag != 'j':
                        #break
                    #position = word + position
        #if position == '':
            ## from back
            #for keyword in position_detected_keywords_back:
                #if keyword in sentence:
                    #sub_sentence = sentence[sentence.index(keyword)+len(keyword):]
                    #words = pseg.cut(sub_sentence)
                    #for word, tag in list(words):
                        #word = word.encode('utf8')
                        #tag = tag.encode('utf8')
                        #print word.decode('utf-8').encode('big5'), tag.decode('utf-8')
                        #if tag != 'n' and tag != 'ns' and tag != 'a' and tag != 'j':
                            #break
                        #position = position + word
#
    #print position.decode('utf8')
#
    #collected_tags.append(position)
#
    #for item in collected_tags:
        #print item

    collected_tags = getTag(sentence)[0]
    geo = getLocation(sentence)

    #print ('Tag: ' + collected_tags[0])
    #print ('Location: ' + collected_tags[1])

    #print ('Try to get the position of ' + position)
    #geo = getGeocodeByGoogleMap(position)

    api_calls = []    
    param = get_search_parameters(geo[0], geo[1], collected_tags[0])
    api_calls.append( getYelpResults(param) )
    jsonFromYelp = json.dumps(api_calls)
    time.sleep(1.0)
    restaurantData = json.loads(jsonFromYelp)
    print len(restaurantData[0]["businesses"])
    outputRestaurant = []

    for oneData in restaurantData[0]["businesses"]:
        print oneData["name"]
        print oneData["location"]["address"]
        #print oneData["categories"]
        print oneData["distance"]
        #outputRestaurant.append(oneData["name"])

    responseSentence = ( '最高分回傳：'.decode('utf-8') + restaurantData[0]["businesses"][0]["name"] )
    address = restaurantData[0]["businesses"][0]["location"]["address"]

    return responseSentence, address


def getTag(sentence_for_get_tag):
    category_dictionary = km.loadDictionary("categoryTW.txt")
    category_keyword_front = km.loadList("category_keyword_front.txt")

    print u"==== 開始測試類型擷取 ====: ", sentence_for_get_tag

    tag_front = 0
    search_sen = ""
    for term in category_keyword_front:   # find front keyword (maybe find nothing)
        if term in sentence_for_get_tag:
            front_candidate = int( sentence_for_get_tag.find(term) + len(term) )
            print term, front_candidate
            if tag_front < front_candidate:
                tag_front = front_candidate
                search_sen = sentence_for_get_tag[ sentence_for_get_tag.find(term)+1 : ]
    if tag_front == 0: search_sen = sentence_for_get_tag   # if find no front keywork, use original sentence
    print "Search_sentence will be: ", search_sen

    find_category = [""]
    find_term = [""]
    for category in category_dictionary:    # find category
        for term in category_dictionary[ category ]:
            if term in search_sen:
                print category, term
                if len(find_term[0]) < len(term):   # once we found a longer term, replace the older ones
                    print "不要殺我QQ", "1.", find_term[0], "2.", term, category
                    find_category = [ category ]
                    find_term = [ term ]
                elif len(find_term[0]) == len(term):    # find a term with the same length, join it
                    print "怎麼沒有!!?"
                    find_category += [ category ]
                    if term not in find_term:
                        find_term += [ term ]
    print "We've found category: ", find_category
    print "We've found term: ", find_term

    if len(find_category[0]) == 0: return [ find_category, find_term, 0 ]   # find no category
    else: return [ find_category, find_term, 1 ]


def getLocation(sentence_for_get_location):  # here we use template sentence for getting location
    location_dictionary = km.loadDictionary("location_dictionary.txt")
    location_keyword_front = km.loadList("location_keyword_front.txt")
    location_keyword_back = km.loadList("location_keyword_back.txt")

    print u"==== 開始測試地點擷取 ====: ", sentence_for_get_location

    location_front = 0
    location_back = 0

    for term_front in location_keyword_front: # find front keyword (maybe find nothing)
        if term_front in sentence_for_get_location:
            front_candidate = int( sentence_for_get_location.find(term_front) + len(term_front) )
            print "front, ", term_front, front_candidate
            if location_front < front_candidate: location_front = front_candidate
    for term_back in location_keyword_back:  # find back keyword (there must be one)
        if term_back in sentence_for_get_location:
            location_back = int( sentence_for_get_location.find(term_back) )
            print "back, ", term_back, location_back

    location = sentence_for_get_location[ location_front:location_back ]
    print len(location)
    print location_front, location_back, sentence_for_get_location[ location_front:location_back ]

    if location_back == 0:   # Return with Error: Can not find a location, use default location: "NTU backdoor"
        return [ 1, 25.0209219, 121.5403804 ]
    else:           # Return normally
        for coordinates_candidate in location_dictionary:    # try to find the location in location_dict
            for term in location_dictionary[ coordinates_candidate ]:
                if location == term:
                    coordinates_from_dict = [ float( coordinates_candidate.split(u',')[0] ),
                                              float( coordinates_candidate.split(u',')[1] ), ]
                    print "Get GeoCode by loca_dict! " + str(coordinates_from_dict[0]) + ' ' + str(coordinates_from_dict[1])
                    return coordinates + [0]
        return getGeocodeByGoogleMap( location.encode("utf8") ) + [0]  # go GoogleMap for getting help


def getGeocodeByGoogleMap(location_for_get_Geocode):    # notice that it can only eat str format, do encode("utf8") pls
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    key = "&key=AIzaSyDU0SvmkoV9K_hm5xqDM39_-acX5HF7IW4"

    googleapi_loca = url + "台灣+" + location_for_get_Geocode + key
    rf = urllib.urlopen(googleapi_loca)
    json_from_GoogleMap = json.loads(rf.read())
    coordinates = [ json_from_GoogleMap["results"][0]["geometry"]["location"]["lat"],
                    json_from_GoogleMap["results"][0]["geometry"]["location"]["lng"] ]

    print 'Get GeoCode by Google Map! ' + str(coordinates[0]) + ' ' + str(coordinates[1])
    return coordinates


def getYelpResults(params): # btain these from Yelp's manage access page
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


def get_search_parameters(inLat, inLong, inTerm):   # see the Yelp API for more details
    params = {}
    params["term"] = inTerm
    params["limit"] = 3
    #params["offset"] = 100
    #params["sort"] = 1
    params["category_filter"] = "italian,japanese"
    params["radius_filter"] = 1000
    params["actionlinks"] = True

    coordinateToYelp = str(inLat) + ',' + str(inLong)
    params["ll"] = coordinateToYelp

    params["cc"] = "TW"

    return params


if __name__ == '__main__':
    root = Tk()
    iKnow_Tk = iKnowMainWindow(master=root)
    iKnow_Tk.mainloop()
