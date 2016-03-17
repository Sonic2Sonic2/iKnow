
# -*- coding: utf8 -*-
def loadList(dictName):
    loadDict = {}   # in fact I use dictionary
    rf = open("./knowledge/" + dictName, 'r')
    rdata = rf.read()
    rf.close()
    for term in rdata.split(','):
        loadDict[ term ] = 1
    return loadDict

def loadDictionary(dictName):
    loadDict = {}   # use dictionary
    rf = open("./knowledge/" + dictName, 'r')
    rlines = rf.readlines()
    rf.close()
    for line in rlines:
        data = line.split(':')
        loadDict[ data[0] ] = data[1].split(',')
    return loadDict

if __name__ == '__main__':
    print "This is a supporting module for knowledge manipulating."