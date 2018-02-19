#!/usr/bin/env python

import subprocess
import re
import os
import pypandoc


if __name__ == '__main__':

    words1 = []
    with open('blooms_verbs.txt')as f:
        words1 = f.read().lower().splitlines()

    dataDir = "../Data/PDF"
    lastEvent = ""
    charCounts=[]
    colIDs = {}
    avgChars=0
    
    for fileName in os.listdir(dataDir):
        if fileName.endswith(".pdf"):
            event=fileName[:4]
            if (event != lastEvent): # if switching events
                colIDs[event]={}
                if (len(charCounts)>0): # new event / new column
                    avgChars=int(float(sum(charCounts))/len(charCounts)) # calculate average chars for last event
                    colIDs[lastEvent]['_avgChars']=avgChars # add a dict entry with average chars per file
                    charCounts=[] # reset charCounts for new event             

            pdfData = subprocess.check_output(["less",os.path.join(dataDir,fileName)])#os.path.join(directory, filename)
            charCounts.append(len(pdfData))
            pfdDataLower = pdfData.lower().split()
            for item in pfdDataLower:
                item = ''.join(e for e in item if e.isalnum())
                if item in words1:
                    if item in colIDs[event]:
                        colIDs[event][item] += 1
                    else:
                        colIDs[event][item] = 1
        lastEvent = event
    colIDs[lastEvent]['_avgChars']=avgChars # add last average to dictionary
    print "colIDs =",colIDs
            
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
    
    with open('pdf_summary.csv','w') as o:
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

                

                
'''
    for key, val in word_dict.iteritems():
        #print key,val
        if key in words2:
            print key,word_dict[key]
'''
