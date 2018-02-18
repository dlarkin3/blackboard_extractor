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
    print ignoreLineStrings

    byfileID = {}
    dataDir = "Downloads"
    for fileName in os.listdir(dataDir):
        if fileName.endswith(".txt"):
            with open(os.path.join(dataDir,fileName)) as f:
                print ("========== Parsing: %s" %os.path.join(dataDir,fileName))
                for line in f:
                    line=line.strip()
                    if not line.startswith(tuple(ignoreLineStrings)) and (len(line) > 5):
                        print line
                        print ("----------")
                    
                  
