
# -*- coding: utf8 -*-
def loadDictionary(dictName):
    loadDict = {}
    rf = open("./knowledge/" + dictName, 'r')
    rdata = rf.read()
    rf.close()
    for term in rdata.split(','):
        loadDict[ term ] = 1
    return loadDict

if __name__ == '__main__':
    print "This is a supporting module for dictionary manipulating."