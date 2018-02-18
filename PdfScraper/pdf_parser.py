#!/usr/bin/env python

import subprocess
import re
import os
import pypandoc


if __name__ == '__main__':

    words1 = []
    with open('blooms_verbs.txt')as f:
        words1 = f.read().lower().splitlines()
    #print words1

    #words2 = []
    #with open('blooms_verbs_n.txt')as f:
    #    words2 = f.read().lower().splitlines()
    #print words2

    #word_dict = {}
    byfileID = {}
    dataDir = "Downloads"
    for fileName in os.listdir(dataDir):
        if fileName.endswith(".pdf"):
            fileID=fileName[:4]
            if fileID not in byfileID:
                byfileID[fileID]={}              
            pdfData = subprocess.check_output(["less",os.path.join(dataDir,fileName)])#os.path.join(directory, filename)
            #print(re.sub( '\s+', ' ', pdfData ).strip())
            pfdDataLower = pdfData.lower().split()
            #print(pdfData)
            for item in pfdDataLower:
                item = ''.join(e for e in item if e.isalnum())
                if item in words1:
                    if item in byfileID[fileID]:
                        byfileID[fileID][item] += 1
                    else:
                        byfileID[fileID][item] = 1
            
    with open('outputTable.csv','w') as o:
        colHeaders=[]
        rowHeaders=[]
        # Build Table row and col headers
        for okey, oval in byfileID.iteritems():
            colHeaders.append(okey)
            for key, val in oval.iteritems():
                if key not in rowHeaders:
                    rowHeaders.append(key)
        dataTable = [ [0] * len(colHeaders) for _ in range(len(rowHeaders))]
        print colHeaders
        print rowHeaders
        for okey, oval in byfileID.iteritems():
            for key, val in oval.iteritems():
                    col=colHeaders.index(okey)
                    row=rowHeaders.index(key)
                    dataTable[row][col]=val
        o.write(str(colHeaders))
        i = 0
        for row in dataTable:
            output = (rowHeaders[i] + ","+str(row))
            print output
            o.write(output+"\n")
            i+=1
            
                

                
'''
    for key, val in word_dict.iteritems():
        #print key,val
        if key in words2:
            print key,word_dict[key]
'''
