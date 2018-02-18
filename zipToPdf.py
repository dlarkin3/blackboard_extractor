#!/usr/bin/python2 

import zipfile
import os

def zip2Pdf(sourcePath):
    source = os.listdir(sourcePath)
    for sfile in source:
        if (".zip" in sfile):
            zip_ref = zipfile.ZipFile("deleteme.zip", 'r')
            zip_list = zip_ref.namelist()
            for item in zip_list:
                if (item.endswith(".pdf")):
                    if("Example_Lab" in item) or ("Cover" in item):
                        pass
                    else: 
                        zip_ref.extract(item,"tmp")
                        print(item)

if __name__ == "__main__":  
    zip2Pdf("Downloads")
