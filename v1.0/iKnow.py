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

        self.systemState = 1    # [variable] store the state of the system. Default is 1 (1st result)
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
        self.shutDownKeyword = km.loadList("shutDownKeyword.txt")
        self.randomKeyword = km.loadList("randomKeyword.txt")

        self.category = km.loadDictionary("categoryTW.txt")

        self.positionKeywordFront = km.loadList("positionKeywordFront.txt")
        self.positionKeywordBack = km.loadList("positionKeywordBack.txt")
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

        for shutDownterm in self.shutDownKeyword:   # Shut down detected
            if shutDownterm in self.user_say:
                systemState = -1
                return

        

        self.systemState = 11   # Anyway, put to state 1-1 for testing

        return 0 

    def readyForAction(self):
        if self.systemState == -1:   # -1: shut down
            sys.exit()

        elif self.systemState == 11: # 11:
            self.resultOutput = getTag_Location(self.user_say, self.category)

            self.outputField.insert(0, self.resultOutput[0])
            self.displayText["text"] = self.resultOutput[1]
            return 0

        elif self.systemState == 12: # 12:
            pass
            return 0

        else:
            print "異常狀況：請檢查 systemState 是否有遺漏"
            return -1


def getSpeechThenToTextDev(): # for silent testing while developing (kill this function when it's no use)
    dev_test_utt = "測試句：請幫我找台大附近的義大利麵"
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

def getTag_Location(sentence, categoryDict):
    tags = {}   # tags is a dictionary for storing tag
    #infile = open('yelp_tags_data.txt', 'r')    # input
    #for line in infile: # read
        #if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue # if # or nothing --> skip
        #linearr = line.strip('\n').strip('\r\n').split(':') # split tag and synonyms by ':'
        #linearr[1] = linearr[1].split(',')  # the synonyms are split into a list by ','
        #if linearr[1][0] == '': linearr[1] = [] # if the there is nothing bu '' in the synonym list, replace it by a null list
        #tags.update({linearr[0]:linearr[1]})    # add an object into tags dictionary: key = tag, and value = the synonym list
    #infile.close()

    position_detected_keywords_front = []   # a list for storing front keywords
    position_detected_keywords_back = []    # a list for storing back keywords
    infile = open('position_detected_keywords.txt', 'r')
    while 1:
        line = infile.readline()
        if line[0] == '#' or not line: break    # change to back
        position_detected_keywords_front.append(line.strip('\n').strip('\r\n'))
    while 1:
        line = infile.readline()
        if not line: break
        position_detected_keywords_back.append(line.strip('\n').strip('\r\n'))
    infile.close()
 
    position_keywords = {} #location dictionary, seems not work
    infile = open('taipeiLocationDict.txt', 'r')
    for line in infile:
        if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue
        linearr = line.strip('\n').strip('\r\n').split(':')
        linearr[1] = linearr[1].split(',')
        if linearr[1][0] == '': linearr[1] = []
        position_keywords.update({linearr[0]:linearr[1]})
    infile.close()

    collected_tags = []

    # find yelp tag in sentence
    denyDict = {}   # ready to remove
    for tag, keywords in categoryDict.items():
        for keyword in keywords:
            if keyword in sentence: # get only the first one keyword
                keyword_pos = sentence.index(keyword)
                # if chinese 'no' in sentence no far before the keyword
                if '不' in sentence[keyword_pos-9:keyword_pos]:
                    denyDict[tag] = 1.0
                    print ('Detect 不 + ' + keyword).decode('utf8')
                else:
                    collected_tags.append(tag)
                break

    collected_tags.append('餐廳')
    print "getTag_Location 檢查點"
    print collected_tags

    # find position base on keyword
    position = ''
    for p, keywords in position_keywords.items():
        for keyword in keywords:
            if keyword in sentence:
                position = p
                break
    if position == '':
        # find position in sentence. detect keyword, and posseg sentence before the keyword, using nearest n or ns as position
        for keyword in position_detected_keywords_front:
            if keyword in sentence:
                sub_sentence = sentence[:sentence.index(keyword)]
                words = pseg.cut(sub_sentence)
                for word, tag in list(reversed(list(words))):
                    word = word.encode('utf8')
                    tag = tag.encode('utf8')    # the word tag given from jieba
                    print word.decode('utf-8'), tag.decode('utf-8')
                    if tag != 'n' and tag != 'ns' and tag != 'a' and tag != 'j':
                        break
                    position = word + position
        if position == '':
            # from back
            for keyword in position_detected_keywords_back:
                if keyword in sentence:
                    sub_sentence = sentence[sentence.index(keyword)+len(keyword):]
                    words = pseg.cut(sub_sentence)
                    for word, tag in list(words):
                        word = word.encode('utf8')
                        tag = tag.encode('utf8')
                        print word.decode('utf-8').encode('big5'), tag.decode('utf-8')
                        if tag != 'n' and tag != 'ns' and tag != 'a' and tag != 'j':
                            break
                        position = position + word

    print position.decode('utf8')

    collected_tags.append(position)

    for item in collected_tags:
        print item

    print ('Tag: ' + collected_tags[0])
    print ('Location: ' + collected_tags[1])

    api_calls = []
    print ('Try to get the position of ' + position)
    geo = GetGeocode(position)
#==================================================
#    geo = [25.019477, 121.541257]   # NTU backdoor
#==================================================
    print 'Get GeoCode: ' + str(geo[0]) + ' ' + str(geo[1])
    param = get_search_parameters(geo[0], geo[1], collected_tags[0])
    api_calls.append( getYelpResults(param) )
    jsonFromYelp = json.dumps(api_calls)
    time.sleep(1.0)
    restaurantData = json.loads(jsonFromYelp)
    print len(restaurantData[0]["businesses"])
    outputRestaurant = []

    for oneData in restaurantData[0]["businesses"]:     # output (10) result from yelp on console
        print oneData["name"]
        print oneData["location"]["address"]
        #print oneData["categories"]
        print oneData["distance"]
        #outputRestaurant.append(oneData["name"])

    responseSentence = ( '最高分回傳：'.decode('utf-8') + restaurantData[0]["businesses"][0]["name"] )
    address = restaurantData[0]["businesses"][0]["location"]["address"]

    return responseSentence, address

def GetGeocode(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    key = "&key=AIzaSyDU0SvmkoV9K_hm5xqDM39_-acX5HF7IW4"
    location = "台灣 " + location
    googleapi_loca = url+location+key
    f = urllib.urlopen(googleapi_loca)
    items2 = json.loads(f.read())
    name_item = items2["results"][0]
    k =[]
    k.append(name_item["geometry"]["location"]["lat"])
    k.append(name_item["geometry"]["location"]["lng"])
    return k
 
def getYelpResults(params):

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

def get_search_parameters(inLat, inLong, inTerm):

    #See the Yelp API for more details
    params = {}
    params["term"] = inTerm
    #params["limit"] = 1
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
