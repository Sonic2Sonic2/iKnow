# -*- coding: utf-8 -*-
from Tkinter import *
import speech_recognition as sr
import jieba.posseg as pseg
import uniout
import sys
import rauth
import time
import json
import urllib
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
 
class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.userinput = ""
        self.result = ""
        self.word = ""
       # self.stop_words = set(stopwords.words("english"))
 
    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText["text"] = "Input:"
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=6)
 
        self.outputText = Label(self)
        self.outputText["text"] = "Output:"
        self.outputText.grid(row=2, column=0)
        self.outputField = Entry(self)
        self.outputField["width"] = 50
        self.outputField.grid(row=2, column=1, columnspan=6)
         
        self.new = Button(self)
        self.new["text"] = "Start"
        self.new.grid(row=4, column=3)
        self.new["command"] = self.inputWord
        
        self.displayText = Label(self)
        self.displayText["text"] = "iKnow: a Context-Aware Recommender System"
        self.displayText.grid(row=5, column=0, columnspan=7)

    def inputWord(self):
        self.displayText["text"] = "Listening, please speak."
        self.userinput = getSpeech()#self.inputField.get()
        if self.userinput == "":
            self.displayText["text"] = "Please speak again"
        else:
            self.result = getTag_Location(self.userinput)
            self.inputField.insert(0, self.userinput)
            self.outputField.insert(0, self.result)
            self.displayText["text"] = "Get your sentence"



def getSpeech():
    f = open("speech.txt", "w")

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
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio, language = "zh-TW")

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes: # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(value).encode("big5"))  # encode big5 for show on Windows Console
                    c = value.encode("utf-8")
                    f.write(c)  # write in a file
                    return c
                else: # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
                    c = ""
                    return c
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass
        
def getTag_Location(sentence):
    tags = {}
    infile = open('yelp_tags_data', 'r')
    for line in infile:
        if line[0] == '#' or line[0] == '\r' or line[0] == '\n': continue
        linearr = line.strip('\n').strip('\r\n').split(':')
        linearr[1] = linearr[1].split(',')
        if linearr[1][0] == '': linearr[1] = []
        tags.update({linearr[0]:linearr[1]})
    infile.close()

    position_detected_keywords = []
    infile = open('position_detected_keywords', 'r')
    for line in infile:
        position_detected_keywords.append(line.strip('\n').strip('\r\n'))
    infile.close()

    collected_tags = []

    #sentence = raw_input("Input a sentence: ").decode(sys.stdin.encoding).encode('utf8')
    #sentence = sentence2.decode('utf8').encode(sys.stdin.encoding)

    # find yelp tag in sentence
    for tag, keywords in tags.items():
        for keyword in keywords:
            if keyword in sentence:
                keyword_pos = sentence.index(keyword)
                # if chinese 'no' in sentence no far before the keyword
                if '\xe4\xb8\x8d' in sentence[keyword_pos-9:keyword_pos]:
                    sign = '-'
                else:
                    sign = '+'
                collected_tags.append({tag:sign})
                break

    for item in collected_tags:
        for item2 in item:
            print item2.decode('utf-8').encode('big5')

    position = ''
    # find position in sentence. detect keyword, and posseg sentence before the keyword, using nearest n or ns as position
    for keyword in position_detected_keywords:
        if keyword in sentence:
            sub_sentence = sentence[:sentence.index(keyword)]
            words = pseg.cut(sub_sentence)
            for word, tag in list(reversed(list(words))):
                word = word.encode('utf8')
                tag = tag.encode('utf8')
                if tag != 'n' and tag != 'ns':
                    break
                position = word + position
                collected_tags.append(position)
                api_calls = [] 
                param = get_search_parameters(GetGeocode(position)[0], GetGeocode(position)[1], collected_tags[0])
                api_calls.append(get_results(param))
                d = json.dumps(api_calls)
                time.sleep(1.0)
                items = json.loads(d)
                final_name = []
                for name_item in items:
                    for name2 in name_item["businesses"]:
                        print name2["name"]
                        final_name.append(name2["name"]) 

    return final_name


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

def get_search_parameters(lat,long, iterm):
    #See the Yelp API for more details
    #print iterm.encode('big5')
    params = {}
    params["term"] = iterm 
    params["ll"] = "{},{}".format(str(lat),str(long))
    params["location"] = "羅斯福路"
    params["radius_filter"] = "3000"
    params["limit"] = "5"
    params["category_filter"] = "italian"

    return params

 
if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop()
