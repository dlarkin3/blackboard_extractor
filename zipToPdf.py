#!/usr/bin/python2 

import zipfile
import os

def zip2Pdf(sourcePath):
    source = os.listdir(sourcePath)
    for sfile in source:
        if (".zip" in sfile):          
            directory = "tmp/"+sfile[:-4]      
            zip_ref = zipfile.ZipFile(os.path.join(sourcePath,sfile), 'r')
            zip_list = zip_ref.namelist()
            for item in zip_list:
                if (item.endswith(".pdf")):
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    if("Example_Lab" in item) or ("Cover" in item):
                        pass
                    else: 
                        zip_ref.extract(item,directory)
                        print("Extracted:",item)

if __name__ == "__main__":  
    zip2Pdf("Downloads")
