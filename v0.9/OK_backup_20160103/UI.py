from Tkinter import *
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
        self.outputText.grid(row=1, column=0)
        self.outputField = Entry(self)
        self.outputField["width"] = 50
        self.outputField.grid(row=1, column=1, columnspan=6)
         
        self.new = Button(self)
        self.new["text"] = "Enter"
        self.new.grid(row=2, column=3)
        self.new["command"] = self.inputWord
        
        self.displayText = Label(self)
        self.displayText["text"] = "Please input sentence"
        self.displayText.grid(row=3, column=0, columnspan=7)

    def inputWord(self):
        self.userinput = self.inputField.get()
        #if self.userinput == "":
        #    self.displayText["text"] = "no input string"
        #else:
        #    self.word = word_tokenize(self.userinput)
        #    filtered_sentence = [w for w in self.word if not w in self.stop_words]
        #    self.result = filtered_sentence
        #    self.outputField.insert(0, self.result)
        #    self.displayText["text"] = "Get your string"
        
 
if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop()
