#!/usr/bin/env python

import subprocess
import re
import os
import pypandoc

if __name__ == '__main__':
    questions=("Briefly state what","Briefly state any","Provide your opinion","Too difficult or time",
    "Given the learning objectives of this lab","Upload a .","If applicable, provide","Grade Test",
    "FileName is","Enter the name of","Paste a link to","How would you rate your","How would you briefly describe")

    words1 = []
    with open('blooms_verbs.txt')as f:
        words1 = f.read().lower().splitlines()
    #print words1    
    
    ignoreLineStrings = []
    with open('ignoreLineList.txt')as f:
        ignoreLineStrings = f.read().splitlines()
    #print ignoreLineStrings

    byfileID = {}
    dataDir = "../Data/TXT"
    lastEvent = ""
    charCounts=[]
    colIDs = {}
    for fileName in sorted(os.listdir(dataDir)):
        if fileName.endswith(".txt"):
            event = fileName[:4]
            if (event != lastEvent): # if switching events
                colIDs[event]={}
                if (len(charCounts)>0): # new event / new column
                    avgChars=int(float(sum(charCounts))/len(charCounts)) # calculate average chars for last event
                    colIDs[lastEvent]['_avgChars']=avgChars # add a dict entry with average chars per file
                    charCounts=[] # reset charCounts for new event                         
            with open(os.path.join(dataDir,fileName)) as f:
                #print ("========== Parsing: %s" %os.path.join(dataDir,fileName))
                charCount=0
                for line in f:
                    line=line.strip()
                    if not line.startswith(tuple(ignoreLineStrings)) and (len(line) > 5):
                        charCount+=len(line)
                        words = line.lower().split()
                        for word in words:
                            word = ''.join(e for e in word if e.isalnum())
                            if word in words1: # if it is a word of interest
                                if word in colIDs[event]: # is it in this column
                                    colIDs[event][word] += 1
                                else:
                                    colIDs[event][word] = 1                            
                charCounts.append(charCount)
            lastEvent = event # update event 
    print("VVVVVVVVVVVVVVVVVVVVVVVVVV")
    #print 'colIDs =',colIDs    
            
    colHeaders=[]
    rowHeaders=[]
    # Build Table row and col headers
    for event, values in colIDs.iteritems():
        colHeaders.append(event)
        for word, val in values.iteritems():
            if word not in rowHeaders:
                rowHeaders.append(word)
    rowHeaders.sort()
    #print colHeaders
    #print rowHeaders
    dataTable = [ [0] * len(colHeaders) for _ in range(len(rowHeaders))]
    
    with open('txt_summary.csv','w') as o:
        output=","
        for item in colHeaders:
            output+=item+","
        o.write(output+"\n")        
        
        for okey, oval in colIDs.iteritems():
            for key, val in oval.iteritems():
                    print okey,colHeaders
                    col=colHeaders.index(okey)
                    row=rowHeaders.index(key)
                    dataTable[row][col]=val
        i = 0
        for row in dataTable:
            output = (rowHeaders[i] + ",")
            for item in row:
                output += (str(item) + ",")
            print output
            o.write(output+"\n")
            i+=1


    
    

